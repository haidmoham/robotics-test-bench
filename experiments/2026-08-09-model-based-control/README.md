# PD and gravity compensation

Question: With the existing two-link arm, pose, target, and PD gains held fixed, how does adding gravity compensation change steady-state tracking error and control effort?

## Iteration 0 — make a prediction first

Before either run, write down:

- What difference, if any, will you expect in the arm's visual motion?
- What difference, if any, will you expect in steady-state error?
- What difference, if any, will you expect in the control command?

Do not run the comparison until this prediction is recorded.

## Smallest useful experiment

`model_based_control.py` has exactly two modes:

1. `pd` — the existing joint-space PD controller.
2. `gravity-comp` — the same target and PD gains with an added gravity-torque term.

Run both visually, one at a time:

```powershell
pythonw model_based_control.py --controller pd
pythonw model_based_control.py --controller gravity-comp
```

`pythonw` keeps the terminal hidden while leaving the MuJoCo viewer open.

Every 0.25 seconds, the script prints target position, actual position, per-joint error, torque command, total error magnitude, and total control-effort magnitude. Use the late-run samples for the steady-state comparison.

## Boundaries

Do not change the arm, initial pose, target, PD gains, or any other model parameter between conditions. Do not add computed torque or retune the gains.

Related: #4
