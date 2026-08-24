# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item is `NEXT`.
- GitHub issues are active experiment lanes, not a fixed syllabus.
- Closed legacy issues remain historical provenance only.
- Do not route new work through a closed issue unless a current failure revives its mechanism.
- Re-evaluate the queue after each resolved experiment or integrated C-1N failure.
- Do not create the next experiment directory until its Iteration 0 prediction exists.
- `docs/research-platform.md` records long-range design. It does not select current work.

## Current C-1N state

`C-1N // 02 · STAND` is earned. Treat the standing controller, support telemetry,
proximal hinge, deterministic baseline, and known disturbance failures as frozen
evidence. Do not make ROBUST_STAND, contact geometry, or additional standing work
a planned gate before locomotion.

Revisit standing, contact, actuator, estimation, or morphology questions only
when learned locomotion exposes a concrete failure that requires them.

## NEXT

### #25 Learn — first learned locomotion

**Status:** NEXT

Move directly into the smallest useful policy-learning loop from issue #25.
The first learned gait can be ugly. Its job is to make

`objective -> policy -> physical behavior -> failure`

inspectable.

Before training, record the Iteration 0 prediction required by #25, including at
least one way the objective could be exploited without producing the intended
motion.

The first C-1N locomotion policy should preserve rollout state, actions, objective
terms, seeds, policy checkpoints, and fixed evaluation scenarios. Do not promote
`C-1N // 03 · STRIDE` from one attractive rollout. STRIDE requires materially
better sustained locomotion under fixed evaluation.

## After first learned locomotion

Let the first understandable learned failure select the next lane.

Primary lanes:

- #25 Learn — objective -> policy -> behavior.
- #26 Evaluate — treat behavior as a distribution.
- #27 Model — identify and calibrate simulator parameters from rollouts.
- #28 Uncertainty — train and test across distributions and shift.
- #29 Differentiate — backpropagate through simulated dynamics.
- #30 Scale — make simulation experiments reproducible, observable, and fast.

Controls, contact mechanics, actuator limits, state estimation, numerical methods,
and other robotics concepts are supporting mechanisms. Pull one back in only
when a concrete simulation failure makes it necessary.

The intended direction is:

`physical intuition -> support mechanics -> leg reachability -> STAND -> learned locomotion -> distributional evaluation -> system identification and calibration -> uncertainty and randomization -> scalable simulation`

## Long-range design

`docs/research-platform.md` owns the design for procedural validated worlds,
reproducible rollout populations, and scientifically constrained agentic
experimentation.

Keep that design inactive until both conditions exist:

1. A learned locomotion loop can produce rollout populations.
2. A concrete failure requires more scale, reproducibility, validation, or structured analysis.

Use current experiment failures to select the next learning or engineering block.
Do not build platform infrastructure only because it appears in the long-range design.
