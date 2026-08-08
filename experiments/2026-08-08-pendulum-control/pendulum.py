import time

import mujoco
import mujoco.viewer

XML = """
<mujoco model="pendulum">
    <option timestep="0.002" gravity="3 0 -5000"/>

    <worldbody>
        <light pos="0 0 3"/>

        <geom
            name="floor"
            type="plane"
            size="3 3 0.1"
        />

        <body name="pendulum" pos="0 0 1.5">
            <joint
                name="hinge"
                type="hinge"
                axis="0 1 0"
            />

            <geom
                name="arm"
                type="capsule"
                fromto="0 0 0  0 0 -1"
                size="0.05"
                mass="1"
            />
        </body>
    </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(XML)
data = mujoco.MjData(model)

data.qpos[0] = 1.0

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        start = time.time()

        mujoco.mj_step(model, data)
        viewer.sync()

        remaining = model.opt.timestep - (time.time() - start)
        if remaining > 0:
            time.sleep(remaining)
