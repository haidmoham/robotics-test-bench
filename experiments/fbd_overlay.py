"""Portable viewer-only free-body-diagram arrows for MuJoCo scenes."""

from __future__ import annotations

import mujoco
import numpy as np


def add_force_arrow(
    scene: mujoco.MjvScene,
    point: np.ndarray,
    force: np.ndarray,
    scale: float,
    color: np.ndarray,
    label: str,
    base_width: float = 0.0015,
    force_width_scale: float = 0.00004,
) -> None:
    """Draw one force arrow with force-proportional thickness."""
    if scene.ngeom >= len(scene.geoms):
        return
    arrow = scene.geoms[scene.ngeom]
    width = base_width + force_width_scale * np.linalg.norm(force)
    mujoco.mjv_connector(
        arrow,
        mujoco.mjtGeom.mjGEOM_ARROW,
        width,
        point,
        point + scale * force,
    )
    arrow.rgba = color
    arrow.label = label
    scene.ngeom += 1


def draw_force_diagram(
    scene: mujoco.MjvScene,
    gravity_point: np.ndarray,
    gravity_force: np.ndarray,
    support_points: list[np.ndarray],
    support_force: np.ndarray | list[np.ndarray],
    force_scale: float = 0.04,
) -> None:
    """Draw gravity and ordered support arrows as a semi-transparent FBD overlay."""
    scene.ngeom = 0
    add_force_arrow(
        scene,
        gravity_point,
        gravity_force,
        force_scale,
        np.array([0.71, 0.263, 0.247, 0.5]),
        "gravity",
    )
    if isinstance(support_force, np.ndarray) and support_force.ndim == 1:
        support_forces = [support_force] * len(support_points)
    else:
        support_forces = support_force
    for index, (point, force) in enumerate(zip(support_points, support_forces)):
        add_force_arrow(
            scene,
            point,
            force,
            force_scale,
            np.array([0.25, 0.80, 0.40, 0.5]),
            f"support {index + 1}",
        )
