"""Measure centered-ballast support on the bench's existing articulated tripod."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import mujoco
import mujoco.viewer
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from artifacts import write_telemetry_artifact
from fbd_overlay import add_force_arrow, draw_force_diagram
from telemetry import (
    SIGNAL_BLUE,
    SIGNAL_GREEN,
    WARM_ORANGE,
    WARM_RED,
    TelemetryPager,
    add_ghost_model_geoms,
    make_figure,
    rolling_samples,
    update_stack,
)
from viewer_runtime import WallClockPlayback, WallClockRateGate, launch_experiment_viewer


BODY_MASS = 1.5
EXPERIMENT_ID = "2026-08-11-static-support-centered-ballast"
TREATMENT_BALLAST_MASS = 1.0
# This position is chassis-relative: z=0.14 places the 0.06 m-radius sphere
# directly on the 0.08 m half-height chassis box rather than above the world.
TREATMENT_BALLAST_POSITION = np.array((0.2, 0.0, 0.14))  # metres
LINK_LENGTH = 0.45
LEG_Q = np.array([0.40, -0.80])
LEG_YAWS = (0.0, 120.0, 240.0)
HIP_RADIUS = 0.18
BODY_HEIGHT = 0.884
POSTURE_KP = 45.0
POSTURE_KD = 4.0
BODY_X_KP = 70.0
BODY_X_KD = 12.0
BODY_Z_KP = 90.0
BODY_Z_KD = 16.0
DEFAULT_PLAYBACK_SPEED = 1.0
TELEMETRY_REFRESH_RATE = 10.0
TELEMETRY_SAMPLE_INTERVAL = 0.1


def leg_xml(index: int, yaw: float) -> str:
    yaw_radians = math.radians(yaw)
    hip_x = HIP_RADIUS * math.cos(yaw_radians)
    hip_y = HIP_RADIUS * math.sin(yaw_radians)
    return f"""
      <body name="hip{index}" pos="{hip_x} {hip_y} 0" euler="0 0 {yaw}">
        <joint name="hip{index}" type="hinge" axis="0 1 0"/>
        <geom type="capsule" fromto="0 0 0 0 0 -{LINK_LENGTH}" size="0.04" mass="0.18" contype="0" conaffinity="0"/>
        <body name="knee{index}" pos="0 0 -{LINK_LENGTH}">
          <joint name="knee{index}" type="hinge" axis="0 1 0"/>
          <geom type="capsule" fromto="0 0 0 0 0 -{LINK_LENGTH}" size="0.035" mass="0.14" contype="0" conaffinity="0"/>
          <geom name="foot{index}_contact" type="sphere" pos="0 0 -{LINK_LENGTH}" size="0.055" mass="0.02" rgba="0.71 0.263 0.247 1"/>
          <site name="foot{index}" pos="0 0 -{LINK_LENGTH}" size="0.055" rgba="0.71 0.263 0.247 1"/>
        </body>
      </body>
    """


def make_model(
    ballast_mass: float = 0.0,
    ballast_position: np.ndarray = TREATMENT_BALLAST_POSITION,
) -> mujoco.MjModel:
    legs = "".join(leg_xml(index, yaw) for index, yaw in enumerate(LEG_YAWS))
    motors = "".join(
        f'<motor name="{joint}{index}_motor" joint="{joint}{index}" gear="1" ctrllimited="true" ctrlrange="-20 20"/>'
        for index in range(3)
        for joint in ("hip", "knee")
    )
    ballast = (
        f'<geom name="ballast" type="sphere" pos="{ballast_position[0]} {ballast_position[1]} {ballast_position[2]}" size="0.06" mass="{ballast_mass}" rgba="0.95 0.55 0.10 1"/>'
        if ballast_mass > 0.0
        else ""
    )
    return mujoco.MjModel.from_xml_string(
        f"""
        <mujoco model="static_support_centered_ballast">
          <option timestep="0.002" gravity="0 0 -9.81" integrator="implicitfast"/>
          <default>
            <joint damping="0.8" armature="0.02"/>
            <geom friction="1 0.01 0.001" condim="3" rgba="0.01 0.01 0.015 1"/>
          </default>
          <worldbody>
            <light pos="0 0 3"/>
            <geom name="ground" type="plane" size="3 3 0.1" rgba="0.91 0.925 0.945 1"/>
            <body name="body" pos="0 0 {BODY_HEIGHT}">
              <freejoint/>
              <geom type="box" size="0.25 0.18 0.08" mass="{BODY_MASS}" rgba="0.01 0.01 0.015 1"/>
              {ballast}
              {legs}
            </body>
          </worldbody>
          <actuator>{motors}</actuator>
        </mujoco>
        """
    )


def initialize(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    data.qpos[:7] = (0.0, 0.0, BODY_HEIGHT, 1.0, 0.0, 0.0, 0.0)
    data.qpos[7:] = np.tile(LEG_Q, 3)
    mujoco.mj_forward(model, data)


def support_forces(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    foot_site_ids: list[int],
    body_id: int,
    total_vertical_force: float,
) -> tuple[np.ndarray, np.ndarray]:
    feet = np.array([data.site_xpos[site_id] for site_id in foot_site_ids])
    support_point = data.subtree_com[body_id, :2]
    system = np.vstack((np.ones(3), feet[:, 0], feet[:, 1]))
    target = np.array((total_vertical_force, total_vertical_force * support_point[0], total_vertical_force * support_point[1]))
    return np.linalg.solve(system, target), feet


def apply_hold_torques(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    foot_site_ids: list[int],
    joint_dof_adrs: list[tuple[int, int]],
    body_id: int,
    reference_com: np.ndarray,
) -> None:
    """Reuse the existing tripod's hold; this experiment changes only ballast mass."""
    com = data.subtree_com[body_id]
    body_force_x = BODY_X_KP * (reference_com[0] - com[0]) - BODY_X_KD * data.qvel[0]
    body_force_z = BODY_Z_KP * (reference_com[2] - com[2]) - BODY_Z_KD * data.qvel[2]
    weight = -model.opt.gravity[2] * model.body_mass.sum()
    vertical_forces, _ = support_forces(model, data, foot_site_ids, body_id, max(0.0, weight + body_force_z))
    data.ctrl[:] = 0.0
    for index, (site_id, dof_adrs, vertical_force) in enumerate(zip(foot_site_ids, joint_dof_adrs, vertical_forces)):
        jacobian_position = np.zeros((3, model.nv))
        jacobian_rotation = np.zeros((3, model.nv))
        mujoco.mj_jacSite(model, data, jacobian_position, jacobian_rotation, site_id)
        foot_force = np.array((body_force_x / 3.0, 0.0, vertical_force))
        support_torque = -(jacobian_position[:, dof_adrs].T @ foot_force)
        joint_qpos = data.qpos[[7 + 2 * index, 8 + 2 * index]]
        joint_qvel = data.qvel[[6 + 2 * index, 7 + 2 * index]]
        posture_torque = POSTURE_KP * (LEG_Q - joint_qpos) - POSTURE_KD * joint_qvel
        data.ctrl[2 * index : 2 * index + 2] = support_torque + posture_torque


def roll_pitch_degrees(quaternion: tuple[float, float, float, float]) -> tuple[float, float]:
    w, x, y, z = quaternion
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = math.asin(max(-1.0, min(1.0, 2 * (w * y - z * x))))
    return math.degrees(roll), math.degrees(pitch)


def inside_triangle(point: tuple[float, float], vertices: list[tuple[float, float]]) -> bool:
    signs = [(end[0] - start[0]) * (point[1] - start[1]) - (end[1] - start[1]) * (point[0] - start[0]) for start, end in zip(vertices, vertices[1:] + vertices[:1])]
    return all(value >= -1e-9 for value in signs) or all(value <= 1e-9 for value in signs)


def support_margin(point: tuple[float, float], vertices: list[tuple[float, float]]) -> float | None:
    """Return the nearest signed COM-to-edge distance in metres."""
    if len(vertices) != 3:
        return None
    signs = []
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        edge_x = end[0] - start[0]
        edge_y = end[1] - start[1]
        length = math.hypot(edge_x, edge_y)
        signs.append((edge_x * (point[1] - start[1]) - edge_y * (point[0] - start[0])) / length)
    direction = 1.0 if all(value >= 0.0 for value in signs) else -1.0
    return direction * min(abs(value) for value in signs)


def observe(model: mujoco.MjModel, data: mujoco.MjData) -> dict:
    body_id = model.body("body").id
    ground_id = model.geom("ground").id
    feet = {model.geom(f"foot{index}_contact").id: f"foot{index}" for index in range(3)}
    loads = {name: 0.0 for name in feet.values()}
    active: dict[str, list[float]] = {}
    for index in range(data.ncon):
        contact = data.contact[index]
        foot_id = contact.geom2 if contact.geom1 == ground_id else contact.geom1 if contact.geom2 == ground_id else None
        if foot_id not in feet:
            continue
        wrench = np.zeros(6)
        mujoco.mj_contactForce(model, data, index, wrench)
        name = feet[foot_id]
        loads[name] += abs(float(wrench[0]))
        active[name] = [float(value) for value in data.geom_xpos[foot_id]]
    com = [float(value) for value in data.subtree_com[body_id]]
    roll, pitch = roll_pitch_degrees(tuple(float(value) for value in data.qpos[3:7]))
    vertices = [(position[0], position[1]) for position in active.values()]
    projection = (com[0], com[1])
    return {
        "time": float(data.time),
        "qpos": [float(value) for value in data.qpos],
        "qvel": [float(value) for value in data.qvel],
        "qacc": [float(value) for value in data.qacc],
        "actuator_controls": [float(value) for value in data.ctrl],
        "actuator_forces": [float(value) for value in data.qfrc_actuator],
        "com": com,
        "com_ground_projection": [com[0], com[1], 0.0],
        "active_contact_positions": active,
        "normal_loads": loads,
        "com_projection_inside_support": len(vertices) == 3 and inside_triangle(projection, vertices),
        "support_margin_metres": support_margin(projection, vertices),
        "roll_degrees": roll,
        "pitch_degrees": pitch,
        "angular_velocity": [float(value) for value in data.qvel[3:6]],
        "body_height": float(data.qpos[2]),
    }


def telemetry_sample(state: dict, applied_push: np.ndarray) -> dict:
    """Add the external input to the state observed at one telemetry instant."""
    return {
        **state,
        "applied_push_newtons": [float(value) for value in applied_push],
    }


def draw_overlay(
    model: mujoco.MjModel,
    state: dict,
    baseline_model: mujoco.MjModel,
    baseline_data: mujoco.MjData,
    baseline_state: dict,
    applied_push: np.ndarray,
    viewer: mujoco.viewer.Handle,
) -> None:
    """Render the static no-ballast model beneath the live treatment."""
    support_points = [np.array(position) for position in state["active_contact_positions"].values()]
    support_forces = [
        np.array((0.0, 0.0, state["normal_loads"][name]))
        for name in state["active_contact_positions"]
    ]
    draw_force_diagram(
        viewer.user_scn,
        np.array(state["com"]),
        np.array((0.0, 0.0, model.body_mass.sum() * model.opt.gravity[2])),
        support_points,
        support_forces,
        force_scale=0.0001,
    )
    add_ghost_model_geoms(
        viewer.user_scn,
        baseline_model,
        baseline_data,
        np.array([0.184, 0.412, 0.678, 0.22]),
        "static baseline",
    )
    baseline_points = [np.array(position) for position in baseline_state["active_contact_positions"].values()]
    baseline_support = [
        np.array((0.0, 0.0, baseline_state["normal_loads"][name]))
        for name in baseline_state["active_contact_positions"]
    ]
    baseline_gravity = np.array((0.0, 0.0, baseline_model.body_mass.sum() * baseline_model.opt.gravity[2]))
    add_force_arrow(
        viewer.user_scn,
        np.array(baseline_state["com"]),
        baseline_gravity,
        0.04,
        np.array([0.184, 0.412, 0.678, 0.23]),
        "static reference gravity",
    )
    for index, (point, force) in enumerate(zip(baseline_points, baseline_support)):
        add_force_arrow(
            viewer.user_scn,
            point,
            force,
            0.04,
            np.array([0.184, 0.412, 0.678, 0.23]),
            f"static reference support {index + 1}",
        )
    if np.any(applied_push):
        add_force_arrow(
            viewer.user_scn,
            np.array(state["com"]),
            applied_push,
            0.04,
            np.array([0.95, 0.55, 0.10, 0.7]),
            "applied push",
        )


def make_telemetry_figures() -> tuple[tuple[mujoco.MjvFigure, ...], tuple[mujoco.MjvFigure, ...]]:
    return (
        (
            make_figure("Normal load (N)", (("front", SIGNAL_BLUE), ("rear left", WARM_ORANGE), ("rear right", SIGNAL_GREEN))),
            make_figure("COM projection (m)", (("x", SIGNAL_BLUE), ("y", WARM_ORANGE))),
            make_figure("COM support margin (m)", (("margin", SIGNAL_GREEN),)),
        ),
        (
            make_figure("Body attitude (deg)", (("roll", WARM_RED), ("pitch", SIGNAL_BLUE))),
            make_figure("Angular velocity (rad/s)", (("x", WARM_RED), ("y", SIGNAL_BLUE), ("z", SIGNAL_GREEN))),
            make_figure("Body height (m)", (("height", WARM_ORANGE),)),
        ),
    )


def settled_baseline(
    model: mujoco.MjModel,
    body_id: int,
    foot_site_ids: list[int],
    joint_dof_adrs: list[tuple[int, int]],
    reference_com: np.ndarray,
    settle_seconds: float = 0.5,
) -> tuple[mujoco.MjData, dict]:
    """Measure the no-push equilibrium used as the viewer's reference layer."""
    baseline_data = mujoco.MjData(model)
    initialize(model, baseline_data)
    while baseline_data.time < settle_seconds:
        apply_hold_torques(
            model,
            baseline_data,
            foot_site_ids,
            joint_dof_adrs,
            body_id,
            reference_com,
        )
        mujoco.mj_step(model, baseline_data)
    return baseline_data, observe(model, baseline_data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--viewer", action="store_true", help="show the fixed centered-ballast rollout")
    parser.add_argument("--push-x", type=float, default=0.0, help="world +X force in N during the push pulse; zero preserves the baseline")
    parser.add_argument("--push-start", type=float, default=0.5, help="push pulse start time in seconds")
    parser.add_argument("--push-duration", type=float, default=0.1, help="push pulse length in seconds")
    parser.add_argument("--ballast-mass", type=float, default=TREATMENT_BALLAST_MASS, help="treatment ballast mass in kg")
    parser.add_argument("--ballast-x", type=float, default=TREATMENT_BALLAST_POSITION[0], help="treatment ballast offset along chassis X in metres")
    parser.add_argument("--ballast-y", type=float, default=TREATMENT_BALLAST_POSITION[1], help="treatment ballast offset along chassis Y in metres")
    parser.add_argument("--ballast-z", type=float, default=TREATMENT_BALLAST_POSITION[2], help="treatment ballast offset along chassis Z in metres")
    parser.add_argument("--playback-speed", type=float, default=DEFAULT_PLAYBACK_SPEED, help="viewer playback multiplier; 1 is real time")
    parser.add_argument("--artifact", type=Path, help="write structured rollout telemetry to this JSON path")
    parser.add_argument("--run-id", help="optional run identifier stored in the structured artifact")
    args = parser.parse_args()
    if args.duration <= 0:
        parser.error("duration must be positive")
    if args.push_start < 0 or args.push_duration < 0:
        parser.error("--push-start and --push-duration must be non-negative")
    if args.playback_speed <= 0:
        parser.error("--playback-speed must be positive")
    treatment_ballast_position = np.array((args.ballast_x, args.ballast_y, args.ballast_z))
    model = make_model(args.ballast_mass, treatment_ballast_position)
    data = mujoco.MjData(model)
    initialize(model, data)
    body_id = model.body("body").id
    foot_site_ids = [model.site(f"foot{index}").id for index in range(3)]
    joint_dof_adrs = [(model.joint(f"hip{index}").dofadr[0], model.joint(f"knee{index}").dofadr[0]) for index in range(3)]
    reference_com = data.subtree_com[body_id].copy()
    initial = observe(model, data)
    baseline_model = make_model()
    baseline_body_id = baseline_model.body("body").id
    baseline_foot_site_ids = [baseline_model.site(f"foot{index}").id for index in range(3)]
    baseline_joint_dof_adrs = [(baseline_model.joint(f"hip{index}").dofadr[0], baseline_model.joint(f"knee{index}").dofadr[0]) for index in range(3)]
    baseline_data = mujoco.MjData(baseline_model)
    initialize(baseline_model, baseline_data)
    baseline_reference_com = baseline_data.subtree_com[baseline_body_id].copy()
    baseline_data, baseline_state = settled_baseline(
        baseline_model,
        baseline_body_id,
        baseline_foot_site_ids,
        baseline_joint_dof_adrs,
        baseline_reference_com,
    )
    max_roll = max_pitch = 0.0
    telemetry_pager = TelemetryPager(2)
    viewer = (
        launch_experiment_viewer(model, data, key_callback=telemetry_pager.handle_key)
        if args.viewer
        else None
    )
    left_figures, right_figures = make_telemetry_figures()
    samples = rolling_samples(TELEMETRY_SAMPLE_INTERVAL)
    artifact_samples = [telemetry_sample(initial, np.zeros(3))]
    next_sample = TELEMETRY_SAMPLE_INTERVAL

    def record_sample(sample_state: dict, sample_push: np.ndarray) -> None:
        support_margin = sample_state["support_margin_metres"]
        samples.append(
            (
                sample_state["time"],
                np.array(list(sample_state["normal_loads"].values())),
                np.array(sample_state["com_ground_projection"][:2]),
                np.array((np.nan if support_margin is None else support_margin,)),
                np.array((sample_state["roll_degrees"], sample_state["pitch_degrees"])),
                np.array(sample_state["angular_velocity"]),
                np.array((sample_state["body_height"],)),
            )
        )
        artifact_samples.append(telemetry_sample(sample_state, sample_push))

    def capture_due_samples(sample_state: dict, sample_push: np.ndarray) -> None:
        nonlocal next_sample
        if sample_state["time"] + 1e-9 < next_sample:
            return
        record_sample(sample_state, sample_push)
        while next_sample <= sample_state["time"] + 1e-9:
            next_sample += TELEMETRY_SAMPLE_INTERVAL

    def step_treatment() -> tuple[dict, np.ndarray]:
        pushing = args.push_start <= data.time < args.push_start + args.push_duration
        applied_push = np.array((args.push_x if pushing else 0.0, 0.0, 0.0))
        data.xfrc_applied[body_id, :] = 0.0
        data.xfrc_applied[body_id, :3] = applied_push
        apply_hold_torques(model, data, foot_site_ids, joint_dof_adrs, body_id, reference_com)
        mujoco.mj_step(model, data)
        return observe(model, data), applied_push

    state = initial
    applied_push = np.zeros(3)
    try:
        if viewer is None:
            while data.time < args.duration:
                state, applied_push = step_treatment()
                max_roll = max(max_roll, abs(state["roll_degrees"]))
                max_pitch = max(max_pitch, abs(state["pitch_degrees"]))
                capture_due_samples(state, applied_push)
        else:
            playback = WallClockPlayback(args.playback_speed, data.time)
            telemetry_refresh = WallClockRateGate(TELEMETRY_REFRESH_RATE)
            while data.time < args.duration and viewer.is_running():
                target_sim_time = playback.target_sim_time(args.duration)
                while data.time < target_sim_time:
                    state, applied_push = step_treatment()
                    max_roll = max(max_roll, abs(state["roll_degrees"]))
                    max_pitch = max(max_pitch, abs(state["pitch_degrees"]))
                    capture_due_samples(state, applied_push)

                draw_overlay(model, state, baseline_model, baseline_data, baseline_state, applied_push, viewer)
                if telemetry_refresh.ready():
                    pages = (
                        (left_figures, (1, 2, 3), ((0.0, 14.0), (-0.25, 0.25), (-0.25, 0.25))),
                        (right_figures, (4, 5, 6), ((-2.0, 2.0), (-0.5, 0.5), (0.75, 0.95))),
                    )
                    figures, fields, value_ranges = pages[telemetry_pager.page]
                    update_stack(viewer, figures, samples, fields, value_ranges)
                viewer.sync(state_only=True)
                playback.wait_for_next_frame()
    finally:
        data.xfrc_applied[body_id, :] = 0.0
        if viewer is not None:
            viewer.close()
    final = observe(model, data)
    if artifact_samples[-1]["time"] != final["time"]:
        record_sample(final, applied_push)
    report = {
        "case": "centered_ballast_tripod",
        "treatment_ballast_mass_kg": args.ballast_mass,
        "treatment_ballast_position_metres": treatment_ballast_position.tolist(),
        "push": {"x_newtons": args.push_x, "start_seconds": args.push_start, "duration_seconds": args.push_duration},
        "initial": initial,
        "final": final,
        "max_abs_roll_degrees": max_roll,
        "max_abs_pitch_degrees": max_pitch,
    }
    if args.artifact is not None:
        write_telemetry_artifact(
            args.artifact,
            experiment={
                "id": EXPERIMENT_ID,
                "source": "experiments/2026-08-11-static-support-centered-ballast/static_support.py",
            },
            model={
                "name": "static_support_centered_ballast",
                "mujoco_version": mujoco.__version__,
                "timestep_seconds": float(model.opt.timestep),
            },
            run={
                "id": args.run_id or args.artifact.stem,
                "duration_seconds": args.duration,
                "telemetry_sample_interval_seconds": TELEMETRY_SAMPLE_INTERVAL,
                "random_seed": None,
                "parameters": {
                    "ballast_mass_kg": args.ballast_mass,
                    "ballast_position_metres": treatment_ballast_position.tolist(),
                    "push_x_newtons": args.push_x,
                    "push_start_seconds": args.push_start,
                    "push_duration_seconds": args.push_duration,
                },
                "termination": {
                    "reason": "duration_reached" if data.time >= args.duration else "viewer_closed",
                    "final_time_seconds": float(data.time),
                },
            },
            samples=artifact_samples,
            summary=report,
        )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
