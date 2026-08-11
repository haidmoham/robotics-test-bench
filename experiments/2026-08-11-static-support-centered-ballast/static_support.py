"""Run one passive three-contact, centered-ballast support rollout."""

from __future__ import annotations

import argparse
import json
import math

import mujoco
import numpy as np


BODY_HEIGHT = 0.14
BALLAST_MASS = 0.45
CONTACTS = {
    "front": (0.18, 0.0, -0.10),
    "rear_left": (-0.09, 0.156, -0.10),
    "rear_right": (-0.09, -0.156, -0.10),
}


def make_model() -> mujoco.MjModel:
    feet = "".join(
        f'<geom name="{name}" type="sphere" pos="{x} {y} {z}" size="0.04" mass="0.02"/>'
        for name, (x, y, z) in CONTACTS.items()
    )
    return mujoco.MjModel.from_xml_string(
        f"""
        <mujoco model="static_support_centered_ballast">
          <option timestep="0.002" gravity="0 0 -9.81" integrator="implicitfast"/>
          <default><geom friction="1 0.01 0.001" condim="3"/></default>
          <worldbody>
            <geom name="ground" type="plane" size="3 3 0.1"/>
            <body name="platform" pos="0 0 {BODY_HEIGHT}">
              <freejoint/>
              <geom type="box" size="0.16 0.14 0.06" mass="1.0" rgba="0.12 0.16 0.24 1"/>
              <geom name="ballast" type="box" pos="0 0 0.12" size="0.05 0.05 0.04" mass="{BALLAST_MASS}" rgba="0.95 0.45 0.08 1"/>
              {feet}
            </body>
          </worldbody>
        </mujoco>
        """
    )


def roll_pitch_degrees(quaternion: tuple[float, float, float, float]) -> tuple[float, float]:
    w, x, y, z = quaternion
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = math.asin(max(-1.0, min(1.0, 2 * (w * y - z * x))))
    return math.degrees(roll), math.degrees(pitch)


def inside_triangle(point: tuple[float, float], vertices: list[tuple[float, float]]) -> bool:
    signs = []
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        signs.append((end[0] - start[0]) * (point[1] - start[1]) - (end[1] - start[1]) * (point[0] - start[0]))
    return all(value >= -1e-9 for value in signs) or all(value <= 1e-9 for value in signs)


def observe(model: mujoco.MjModel, data: mujoco.MjData) -> dict:
    platform_id = model.body("platform").id
    ground_id = model.geom("ground").id
    feet = {model.geom(name).id: name for name in CONTACTS}
    loads = {name: 0.0 for name in CONTACTS}
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
    com = [float(value) for value in data.subtree_com[platform_id]]
    roll, pitch = roll_pitch_degrees(tuple(float(value) for value in data.qpos[3:7]))
    vertices = [(position[0], position[1]) for position in active.values()]
    return {
        "time": float(data.time),
        "com": com,
        "com_ground_projection": [com[0], com[1], 0.0],
        "active_contact_positions": active,
        "normal_loads": loads,
        "com_projection_inside_support": len(vertices) == 3 and inside_triangle((com[0], com[1]), vertices),
        "roll_degrees": roll,
        "pitch_degrees": pitch,
        "angular_velocity": [float(value) for value in data.qvel[3:6]],
        "body_height": float(data.qpos[2]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=2.0)
    args = parser.parse_args()
    if args.duration <= 0:
        parser.error("duration must be positive")
    model = make_model()
    data = mujoco.MjData(model)
    data.qpos[:7] = (0.0, 0.0, BODY_HEIGHT, 1.0, 0.0, 0.0, 0.0)
    mujoco.mj_forward(model, data)
    initial = observe(model, data)
    max_roll = max_pitch = 0.0
    while data.time < args.duration:
        mujoco.mj_step(model, data)
        state = observe(model, data)
        max_roll = max(max_roll, abs(state["roll_degrees"]))
        max_pitch = max(max_pitch, abs(state["pitch_degrees"]))
    print(json.dumps({"case": "centered_ballast", "initial": initial, "final": observe(model, data), "max_abs_roll_degrees": max_roll, "max_abs_pitch_degrees": max_pitch}, indent=2))


if __name__ == "__main__":
    main()
