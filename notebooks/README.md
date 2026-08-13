# Notebooks: the test bench's scientific front end

Notebooks are the preferred surface for understanding, checking, plotting, and
comparing results. They are not a replacement for MuJoCo and they do not own
robot behavior: experiments produce measurements, notebooks interrogate them,
and reusable implementation belongs in normal Python source.

## Choose the lightest valid path

- **Notebook-native inquiry:** use a notebook for a derivation, toy model,
  finite-difference check, parameter sweep, or visualization that does not need
  embodiment.
- **Headless MuJoCo + notebook analysis:** use the simulator for contacts,
  dynamics, controller behavior, or other embodied questions. Save telemetry,
  then inspect it repeatedly without rerunning the simulator.

Do not promote a notebook observation into a robot claim unless the input
artifact is traceable to a reproducible experiment and the claim is preserved
in the experiment's own evidence.

## Run artifacts

Headless telemetry lives under `results/`, which is intentionally ignored by
Git. The shared writer in [`experiments/artifacts.py`](../experiments/artifacts.py)
uses this JSON structure:

```text
schema_version
artifact_type
experiment          # stable experiment ID and source path
model               # model name, MuJoCo version, timestep
run                 # run ID, parameters, termination
samples[]           # timestamped observed state and inputs
summary             # experiment-defined rollout summary
```

`samples` preserve measurements such as state, COM, contacts, normal loads,
forces, pose, and rollout-specific observables. Experiments choose the exact
fields, but should keep their names and units explicit.

## First runnable analysis

The current notebook needs the same MuJoCo and NumPy environment as the
experiment plus Matplotlib and Jupyter:

```bash
python3 -m pip install mujoco numpy matplotlib jupyter nbclient
```

Generate a saved static-support trace from the repository root:

```bash
python3 experiments/2026-08-11-static-support-centered-ballast/static_support.py \
  --duration 2 \
  --artifact results/static-support/default.json \
  --run-id static-support-default
```

Then execute the analysis end-to-end:

```bash
python3 -m jupyter nbconvert --execute --to notebook --inplace \
  notebooks/static_support_telemetry.ipynb
```

The notebook reads `results/static-support/default.json`; it never launches a
viewer or re-runs MuJoCo. To explore a different rollout, generate a distinct
artifact and change the visible `ARTIFACT_PATH` parameter near the notebook's
top.

## Promotion and publishing

Use notebooks for compact technical artifacts when the executable analysis is
the natural record. Promote repeated utilities into `experiments/` or another
normal source module, and write a longer article only when several experiments
support a coherent argument.
