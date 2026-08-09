# PD and gravity compensation

Question: With the existing two-link arm, pose, target, and PD gains held fixed, how does adding gravity compensation change periodic steady-state tracking error and the burden on PD feedback?

## Iteration 0 — make a prediction first

Before either run, write down:

- What difference, if any, will you expect in the arm's visual motion?
- What difference, if any, will you expect in tracking error?
- What difference, if any, will you expect in feedback torque versus total torque?

Do not run the comparison until this prediction is recorded.

## Smallest useful experiment

`model_based_control.py` has four controller modes:

1. `pd` — the existing joint-space PD controller.
2. `gravity-comp` — the same target and PD gains with an added model-predicted gravity torque.
3. `computed-torque` — the same PD controller plus inverse dynamics evaluated at the desired position, velocity, and acceleration.
4. `computed-torque-wrong-mass` — the same computed-torque controller, but its private model assumes a 0.35 kg link-2 mass. The simulated plant remains 0.7 kg.

Run both visually, one at a time:

```powershell
pythonw model_based_control.py --controller pd
pythonw model_based_control.py --controller gravity-comp
pythonw model_based_control.py --controller computed-torque
pythonw model_based_control.py --controller computed-torque-wrong-mass
```

`pythonw` keeps the terminal hidden while leaving the MuJoCo viewer open. The baseline PD arm is blue. The gravity-compensation arm is orange.

To compare their states visually without combining their physics, run:

```powershell
pythonw model_based_control.py --controller overlay
```

This viewer advances the two controllers in separate `MjData` objects. It renders the gray target arm, the blue PD arm, and the orange gravity-compensation arm in one scene. Its live right-side plots show each controller's two-joint applied torque, its first numerical derivative, and its second numerical derivative over the latest six simulated seconds. `P` is PD and `G` is gravity compensation. It is a visual aid only. Use the headless telemetry below for evidence.

For telemetry, run the same conditions headless so the target follows MuJoCo simulation time and the output is easy to capture:

```powershell
python model_based_control.py --controller pd --headless --duration 16
python model_based_control.py --controller gravity-comp --headless --duration 16
python model_based_control.py --controller computed-torque --headless --duration 16
python model_based_control.py --controller computed-torque-wrong-mass --headless --duration 16
```

Every 0.25 simulation seconds, the script reports target position, actual position, tracking error, and three torque terms:

- `tau_fb` — the PD feedback command.
- `tau_g` — the model-predicted gravity torque at the current pose.
- `tau_total` — the actuator command actually applied. For baseline PD, this equals `tau_fb`; for gravity compensation, this equals `tau_fb + tau_g`.
- `tau_ff` — the applied model-based feedforward torque. For computed torque, it includes gravity, motion-coupling, and desired-acceleration terms.

The target period is about 7.85 seconds, so a 16-second headless run covers about two cycles. Compare late-run samples rather than the startup transient. The next learning question is whether compensation reduces tracking error and/or `tau_fb`; lower `tau_total` is not required by the hypothesis.

The headless summary also reports tracking and acceleration-error RMS near target turnarounds, where desired acceleration is large, plus a signed target-frequency phase offset for each joint. These metrics operationalize the visual comparison. They do not by themselves establish a causal explanation.

## Boundaries

Do not change the plant, initial pose, target, PD gains, timestep, or any other physical parameter between conditions. In the wrong-mass condition, change only the controller's private link-2 mass.

Related: #4
