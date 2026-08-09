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
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--duration", type=float, default=16.0)
    return parser.parse_args()


def make_model(controller):
    model_name, rgba = COLORS[controller]
    return mujoco.MjModel.from_xml_string(
        XML_TEMPLATE.format(model_name=model_name, rgba=rgba)
    )


def desired_state(elapsed):
    phase = FREQUENCY * elapsed
    q_des = np.array([START[i] + AMPLITUDE[i] * math.sin(phase) for i in range(2)])
    qvel_des = np.array(
        [AMPLITUDE[i] * FREQUENCY * math.cos(phase) for i in range(2)]
    )
    qacc_des = np.array(
        [-AMPLITUDE[i] * FREQUENCY**2 * math.sin(phase) for i in range(2)]
    )
    return q_des, qvel_des, qacc_des


def gravity_torque(model, data):
    saved_qvel = data.qvel.copy()
    data.qvel[:] = 0.0
    data.qacc[:] = 0.0
    mujoco.mj_inverse(model, data)
    torque = data.qfrc_inverse.copy()
    data.qvel[:] = saved_qvel
    return torque


def step_controller(args, model, data, elapsed):
    q_des, qvel_des, _ = desired_state(elapsed)
    tau_fb = KP * (q_des - data.qpos) + KD * (
        qvel_des - data.qvel
    )
    tau_g = gravity_torque(model, data)
    tau_total = tau_fb + tau_g if args.controller == "gravity-comp" else tau_fb
    data.ctrl[:] = tau_total

    mujoco.mj_step(model, data)
    return q_des, data.qpos - q_des, tau_fb, tau_g, tau_total


def report(elapsed, data, target, error, tau_fb, tau_g, tau_total):
    print(
        f"t={elapsed:5.2f} target={target} qpos={data.qpos[:2]} "
        f"error={error[:2]} tau_fb={tau_fb[:2]} tau_g={tau_g[:2]} "
        f"tau_total={tau_total[:2]} "
        f"|error|={np.linalg.norm(error):.4f} "
        f"|tau_fb|={np.linalg.norm(tau_fb):.4f} "
        f"|tau_total|={np.linalg.norm(tau_total):.4f}"
    )


def rms(samples):
    return np.sqrt(np.mean(np.square(np.asarray(samples)), axis=0))


def projection_coefficients(feedback, gravity):
    feedback = np.asarray(feedback)
    gravity = np.asarray(gravity)
    return np.sum(feedback * gravity, axis=0) / np.sum(gravity * gravity, axis=0)


def run_headless(args):
    if args.duration < 2 * math.pi / FREQUENCY:
        raise ValueError("--duration must include at least one full target cycle")

    model = make_model(args.controller)
    data = mujoco.MjData(model)
    data.qpos[:] = START
    mujoco.mj_forward(model, data)

    period = 2 * math.pi / FREQUENCY
    cycle_start = (math.floor(args.duration / period) - 1) * period
    cycle_end = cycle_start + period
    samples = {"error": [], "tau_fb": [], "tau_g": [], "tau_total": []}

    while data.time < args.duration - 1e-12:
        elapsed = data.time
        target, error, tau_fb, tau_g, tau_total = step_controller(
            args, model, data, elapsed
        )
        if cycle_start <= data.time <= cycle_end + 1e-12:
            samples["error"].append(error)
            samples["tau_fb"].append(tau_fb)
            samples["tau_g"].append(tau_g)
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


def main():
    args = parse_args()
    if args.duration <= 0:
        raise ValueError("--duration must be positive")
    if args.headless:
        run_headless(args)
        return

    model = make_model(args.controller)
    data = mujoco.MjData(model)
    data.qpos[:] = START
    mujoco.mj_forward(model, data)

    print(f"controller={args.controller} color={COLORS[args.controller][0]}")
    next_report = 0.0

    start_time = time.time()
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            wall_start = time.time()
            elapsed = wall_start - start_time
            target, error, tau_fb, tau_g, tau_total = step_controller(
                args, model, data, elapsed
            )
            viewer.sync()

            if elapsed >= next_report:
                report(elapsed, data, target, error, tau_fb, tau_g, tau_total)
                next_report += 0.25

            remaining = model.opt.timestep - (time.time() - wall_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
