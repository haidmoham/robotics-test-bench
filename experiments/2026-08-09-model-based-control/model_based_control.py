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
    tracking = KP * (q_des - data.qpos) + KD * (
        qvel_des - data.qvel
    )

    if args.controller == "pd":
        data.ctrl[:] = tracking
    else:
        data.ctrl[:] = tracking + gravity_torque(model, data)

    mujoco.mj_step(model, data)
    return q_des, data.qpos - q_des


def report(elapsed, data, target, error):
    print(
        f"t={elapsed:5.2f} target={target} qpos={data.qpos[:2]} "
        f"error={error[:2]} ctrl={data.ctrl[:2]} "
        f"|error|={np.linalg.norm(error):.4f} |ctrl|={np.linalg.norm(data.ctrl):.4f}"
    )


def main():
    args = parse_args()

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
            target, error = step_controller(args, model, data, elapsed)
            viewer.sync()

            if elapsed >= next_report:
                report(elapsed, data, target, error)
                next_report += 0.25

            remaining = model.opt.timestep - (time.time() - wall_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
