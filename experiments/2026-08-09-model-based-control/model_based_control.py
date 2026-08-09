"""Compare joint PD with the same controller plus gravity compensation."""

import argparse
import math
import time

import mujoco
import mujoco.viewer
import numpy as np


XML_TEMPLATE = """
<mujoco model="model_based_control_{model_name}">
  <option timestep="0.002" gravity="0 0 -9.81"/>
  <worldbody>
    <light pos="0 0 4"/>
    <geom type="plane" size="3 3 0.1"/>
    <body name="shoulder" pos="0 0 2.5" euler="0 90 0">
      <joint name="joint1" type="hinge" axis="0 1 0" damping="0.02"/>
      <geom name="link1" type="capsule" fromto="0 0 0 0 0 -1" size="0.05" mass="1" rgba="{rgba}"/>
      <body name="elbow" pos="0 0 -1">
        <joint name="joint2" type="hinge" axis="0 1 0" damping="0.02"/>
        <geom name="link2" type="capsule" fromto="0 0 0 0 0 -0.8" size="0.045" mass="0.7" rgba="{rgba}"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <motor joint="joint1" gear="1"/>
    <motor joint="joint2" gear="1"/>
  </actuator>
</mujoco>
"""

START = (0.35, -0.70)
KP = 18.0
KD = 4.0
AMPLITUDE = (0.35, 0.45)
FREQUENCY = 0.8
REPORT_INTERVAL = 0.25
COLORS = {
    "pd": ("pd_blue", "0.15 0.40 0.95 1"),
    "gravity-comp": ("gravity_orange", "0.95 0.45 0.08 1"),
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--controller",
        choices=("pd", "gravity-comp"),
        default="pd",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without the viewer for deterministic telemetry collection.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=16.0,
        help="Headless simulation duration in seconds.",
    )
    args = parser.parse_args()
    if args.duration <= 0:
        parser.error("--duration must be positive")
    return args


def make_model(controller):
    model_name, rgba = COLORS[controller]
    return mujoco.MjModel.from_xml_string(
        XML_TEMPLATE.format(model_name=model_name, rgba=rgba)
    )


def desired_state(sim_time):
    phase = FREQUENCY * sim_time
    q_des = np.array([START[i] + AMPLITUDE[i] * math.sin(phase) for i in range(2)])
    qvel_des = np.array(
        [AMPLITUDE[i] * FREQUENCY * math.cos(phase) for i in range(2)]
    )
    qacc_des = np.array(
        [-AMPLITUDE[i] * FREQUENCY**2 * math.sin(phase) for i in range(2)]
    )
    return q_des, qvel_des, qacc_des


def gravity_torque(model, gravity_data, qpos):
    gravity_data.qpos[:] = qpos
    gravity_data.qvel[:] = 0.0
    gravity_data.qacc[:] = 0.0
    mujoco.mj_inverse(model, gravity_data)
    return gravity_data.qfrc_inverse.copy()


def step_controller(args, model, data, gravity_data, sim_time):
    q_des, qvel_des, _ = desired_state(sim_time)
    tau_feedback = KP * (q_des - data.qpos) + KD * (
        qvel_des - data.qvel
    )
    tau_gravity = gravity_torque(model, gravity_data, data.qpos)
    tau_total = (
        tau_feedback + tau_gravity
        if args.controller == "gravity-comp"
        else tau_feedback
    )
    data.ctrl[:] = tau_total
    mujoco.mj_step(model, data)
    error = data.qpos - q_des
    return q_des, error, tau_feedback, tau_gravity, tau_total


def report(sim_time, data, target, error, tau_feedback, tau_gravity, tau_total):
    print(
        f"t={sim_time:5.2f} target={target} qpos={data.qpos[:2]} "
        f"error={error[:2]} tau_fb={tau_feedback[:2]} "
        f"tau_g={tau_gravity[:2]} tau_total={tau_total[:2]} "
        f"|error|={np.linalg.norm(error):.4f} "
        f"|tau_fb|={np.linalg.norm(tau_feedback):.4f} "
        f"|tau_g|={np.linalg.norm(tau_gravity):.4f} "
        f"|tau_total|={np.linalg.norm(tau_total):.4f}"
    )


def rms(samples):
    return np.sqrt(np.mean(np.square(np.asarray(samples)), axis=0))


def projection_coefficients(feedback, gravity):
    feedback = np.asarray(feedback)
    gravity = np.asarray(gravity)
    return np.sum(feedback * gravity, axis=0) / np.sum(gravity * gravity, axis=0)


def run_headless(args, model, data, gravity_data):
    period = 2 * math.pi / FREQUENCY
    if args.duration < period:
        raise ValueError("--duration must include at least one full target cycle")
    cycle_start = (math.floor(args.duration / period) - 1) * period
    cycle_end = cycle_start + period
    samples = {"error": [], "tau_fb": [], "tau_g": [], "tau_total": []}

    while data.time < args.duration:
        sim_time = data.time
        metrics = step_controller(args, model, data, gravity_data, sim_time)
        if cycle_start <= data.time <= cycle_end + 1e-12:
            _, error, tau_feedback, tau_gravity, tau_total = metrics
            samples["error"].append(error)
            samples["tau_fb"].append(tau_feedback)
            samples["tau_g"].append(tau_gravity)
            samples["tau_total"].append(tau_total)

    print(
        f"controller={args.controller} duration={args.duration:g} "
        f"final_cycle=[{cycle_start:.6f}, {cycle_end:.6f}]"
    )
    for name in ("error", "tau_fb", "tau_g", "tau_total"):
        print(f"{name}_rms={rms(samples[name])}")
    if args.controller == "pd":
        print(
            "tau_fb_projection_onto_tau_g="
            f"{projection_coefficients(samples['tau_fb'], samples['tau_g'])}"
        )


def run_viewer(args, model, data, gravity_data):
    next_report = 0.0
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            wall_start = time.time()
            sim_time = data.time
            metrics = step_controller(args, model, data, gravity_data, sim_time)
            viewer.sync()

            if sim_time >= next_report:
                report(sim_time, data, *metrics)
                next_report += REPORT_INTERVAL

            remaining = model.opt.timestep - (time.time() - wall_start)
            if remaining > 0:
                time.sleep(remaining)


def main():
    args = parse_args()
    model = make_model(args.controller)
    data = mujoco.MjData(model)
    gravity_data = mujoco.MjData(model)
    data.qpos[:] = START
    mujoco.mj_forward(model, data)

    print(f"controller={args.controller} color={COLORS[args.controller][0]}")
    if args.headless:
        run_headless(args, model, data, gravity_data)
    else:
        run_viewer(args, model, data, gravity_data)


if __name__ == "__main__":
    main()
