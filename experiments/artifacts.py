"""Stable, machine-readable artifacts for headless robotics experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence


TELEMETRY_ARTIFACT_SCHEMA_VERSION = 1


def write_telemetry_artifact(
    path: Path,
    *,
    experiment: Mapping[str, Any],
    model: Mapping[str, Any],
    run: Mapping[str, Any],
    samples: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> None:
    """Write one completed rollout as an atomic JSON telemetry artifact.

    Experiments remain the authority for physical behavior. This artifact is a
    durable interface for notebooks and other downstream analysis surfaces.
    """
    artifact = {
        "schema_version": TELEMETRY_ARTIFACT_SCHEMA_VERSION,
        "artifact_type": "robotics-test-bench.telemetry",
        "experiment": dict(experiment),
        "model": dict(model),
        "run": dict(run),
        "samples": [dict(sample) for sample in samples],
        "summary": dict(summary),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    temporary_path.replace(path)
