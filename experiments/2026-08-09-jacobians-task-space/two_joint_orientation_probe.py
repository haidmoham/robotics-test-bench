"""Complete the remaining #6 static two-DOF orientation check."""

import mujoco
import numpy as np


XML_TEMPLATE = """
<mujoco model="two_joint_orientation_probe">
  <option timestep="0.002" gravity="0 0 0"/>
  <worldbody>
    <body name="base" pos="0 0 1.5" euler="0 {base_degrees} 0">
      <body name="hip_frame">
        <joint name="hip" type="hinge" axis="0 1 0"/>
        <geom type="capsule" fromto="0 0 0 0 0 -0.75" size="0.05" mass="1"/>
        <body name="knee" pos="0 0 -0.75">
          <joint name="knee" type="hinge" axis="0 1 0"/>
          <geom type="capsule" fromto="0 0 0 0 0 -0.65" size="0.045" mass="0.7"/>
          <site name="foot" pos="0 0 -0.65" size="0.04"/>
        </body>
      </body>
    </body>
  </worldbody>
</mujoco>
"""

ORIENTATIONS = (0.0, 90.0, 180.0)
START_Q = np.array([0.30, -0.60])
HIP_PERTURBATION = 0.02


def make_model(base_degrees):
    return mujoco.MjModel.from_xml_string(
        XML_TEMPLATE.format(base_degrees=base_degrees)
    )


def foot_positions(model, data, base_body_id, foot_site_id):
    """Return the same foot point in world and base-local coordinates."""
    world = data.site_xpos[foot_site_id].copy()
    base_origin_world = data.xpos[base_body_id].copy()
    base_rotation_world = data.xmat[base_body_id].reshape(3, 3)
    local = base_rotation_world.T @ (world - base_origin_world)
    return world, local, base_rotation_world


def first_joint_jacobian(model, data, base_rotation_world, foot_site_id):
    """Return the hip Jacobian column in world and base-local frames."""
    jacp = np.zeros((3, model.nv))
    jacr = np.zeros((3, model.nv))
    mujoco.mj_jacSite(model, data, jacp, jacr, foot_site_id)
    world_column = jacp[:, 0].copy()
    local_column = base_rotation_world.T @ world_column
    return world_column, local_column


def probe_orientation(base_degrees):
    model = make_model(base_degrees)
    data = mujoco.MjData(model)
    base_body_id = model.body("base").id
    foot_site_id = model.site("foot").id

    data.qpos[:] = START_Q
    data.qvel[:] = 0.0
    mujoco.mj_forward(model, data)
    world_before, local_before, base_rotation_world = foot_positions(
        model, data, base_body_id, foot_site_id
    )
    jacobian_world, jacobian_local = first_joint_jacobian(
        model, data, base_rotation_world, foot_site_id
    )

    data.qpos[0] += HIP_PERTURBATION
    mujoco.mj_forward(model, data)
    world_after, local_after, _ = foot_positions(
        model, data, base_body_id, foot_site_id
    )

    return {
        "degrees": base_degrees,
        "world_before": world_before,
        "world_after": world_after,
        "world_delta": world_after - world_before,
        "local_before": local_before,
        "local_after": local_after,
        "local_delta": local_after - local_before,
        "jacobian_world": jacobian_world,
        "jacobian_local": jacobian_local,
    }


def planar(vector):
    return vector[[0, 2]]


def fmt(vector):
    return np.array2string(planar(vector), precision=6, suppress_small=True)


def main():
    print(f"q0 = {START_Q} rad")
    print(f"hip perturbation = {HIP_PERTURBATION:+.3f} rad")
    print("planar components are [X, Z]")

    results = [probe_orientation(degrees) for degrees in ORIENTATIONS]
    for result in results:
        print(f"\nbase = {result['degrees']:.0f} deg")
        print(f"  foot base before  = {fmt(result['local_before'])} m")
        print(f"  foot base after   = {fmt(result['local_after'])} m")
        print(f"  delta base        = {fmt(result['local_delta'])} m")
        print(f"  foot world before = {fmt(result['world_before'])} m")
        print(f"  foot world after  = {fmt(result['world_after'])} m")
        print(f"  delta world       = {fmt(result['world_delta'])} m")
        print(f"  J_hip base        = {fmt(result['jacobian_local'])} m/rad")
        print(f"  J_hip world       = {fmt(result['jacobian_world'])} m/rad")

    reference_delta = results[0]["local_delta"]
    max_local_delta_error = max(
        np.linalg.norm(result["local_delta"] - reference_delta)
        for result in results[1:]
    )
    print(
        "\nmax base-frame delta difference across orientations = "
        f"{max_local_delta_error:.3e} m"
    )
    print(
        "Same q and same hip perturbation -> same base-frame foot motion; "
        "base orientation changes only its shared-frame components."
    )


if __name__ == "__main__":
    main()
