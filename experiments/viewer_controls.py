"""Small reusable viewer controls for MuJoCo passive-viewer applications."""

from __future__ import annotations


class ManualOverride:
    """Toggle whether a scripted controller may write actuator targets."""

    def __init__(self, key: str = "M") -> None:
        self.key = key.upper()
        self.enabled = False

    def handle_key(self, keycode: int) -> None:
        """Use as ``mujoco.viewer.launch_passive(key_callback=...)``."""
        if keycode in (ord(self.key), ord(self.key.lower())):
            self.enabled = not self.enabled

    def status_text(self) -> str:
        state = "ON" if self.enabled else "OFF"
        return f"Manual override [{self.key}]: {state}"
