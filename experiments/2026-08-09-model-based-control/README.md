# PD and gravity compensation

Question: With the existing two-link arm, pose, target, and PD gains held fixed, how does adding gravity compensation change periodic steady-state tracking error and the burden on PD feedback?

## Iteration 0 — make a prediction first

Before either run, write down:

- What difference, if any, will you expect in the arm's visual motion?
- What difference, if any, will you expect in tracking error?
- What difference, if any, will you expect in feedback torque versus total torque?

Do not run the comparison until this prediction is recorded.

## Smallest useful experiment

`model_based_control.py` has exactly two controller modes:

1. `pd` — the existing joint-space PD controller.
2. `gravity-comp` — the same target and PD gains with an added model-predicted gravity torque.

Run both visually, one at a time:

```powershell
pythonw model_based_control.py --controller pd
pythonw model_based_control.py --controller gravity-comp
```

`pythonw` keeps the terminal hidden while leaving the MuJoCo viewer open. The baseline PD arm is blue. The gravity-compensation arm is orange.

For telemetry, run the same conditions headless so the target follows MuJoCo simulation time and the output is easy to capture:

```powershell
python model_based_control.py --controller pd --headless --duration 16
python model_based_control.py --controller gravity-comp --headless --duration 16
```

Every 0.25 simulation seconds, the script reports target position, actual position, tracking error, and three torque terms:

- `tau_fb` — the PD feedback command.
- `tau_g` — the model-predicted gravity torque at the current pose.
- `tau_total` — the actuator command actually applied. For baseline PD, this equals `tau_fb`; for gravity compensation, this equals `tau_fb + tau_g`.

The target period is about 7.85 seconds, so a 16-second headless run covers about two cycles. Compare late-run samples rather than the startup transient. The next learning question is whether compensation reduces tracking error and/or `tau_fb`; lower `tau_total` is not required by the hypothesis.

## Boundaries

Do not change the arm, initial pose, target, PD gains, or any other model parameter between conditions. Do not add computed torque or retune the gains yet. First connect the existing gravity-compensation explanation to the telemetry.

Related: #4
