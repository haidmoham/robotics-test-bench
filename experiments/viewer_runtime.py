"""Shared wall-clock pacing for smooth MuJoCo experiment viewers."""

from __future__ import annotations

import time

import mujoco.viewer


def launch_experiment_viewer(model, data, *, key_callback=None):
    """Launch a passive viewer with MuJoCo's informative built-in UI."""
    return mujoco.viewer.launch_passive(
        model,
        data,
        key_callback=key_callback,
    )


class WallClockPlayback:
    """Map elapsed wall time to a simulation-time target.

    Viewer loops should batch fixed-timestep physics until ``target_sim_time``
    is reached, then update overlays and call ``viewer.sync()`` once.
    """

    def __init__(
        self,
        speed: float = 1.0,
        initial_sim_time: float = 0.0,
        frame_rate: float = 60.0,
    ) -> None:
        if speed <= 0.0:
            raise ValueError("playback speed must be positive")
        if frame_rate <= 0.0:
            raise ValueError("frame rate must be positive")
        self.speed = speed
        self.initial_sim_time = initial_sim_time
        self.frame_interval = 1.0 / frame_rate
        self.wall_origin = time.perf_counter()
        self.next_frame_wall_time = self.wall_origin

    def target_sim_time(self, limit: float) -> float:
        elapsed_wall_time = time.perf_counter() - self.wall_origin
        return min(limit, self.initial_sim_time + elapsed_wall_time * self.speed)

    def wait_for_next_frame(self) -> None:
        """Hold a stable frame cadence without changing the physics timestep."""
        self.next_frame_wall_time += self.frame_interval
        now = time.perf_counter()
        remaining = self.next_frame_wall_time - now
        if remaining > 0.0:
            time.sleep(remaining)
        else:
            self.next_frame_wall_time = now


class WallClockRateGate:
    """Limit expensive viewer work without reducing scene frame rate."""

    def __init__(self, rate: float) -> None:
        if rate <= 0.0:
            raise ValueError("refresh rate must be positive")
        self.interval = 1.0 / rate
        self.next_wall_time = time.perf_counter()

    def ready(self) -> bool:
        now = time.perf_counter()
        if now < self.next_wall_time:
            return False
        self.next_wall_time += self.interval
        if self.next_wall_time < now:
            self.next_wall_time = now + self.interval
        return True
