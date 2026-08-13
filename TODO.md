# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item is `NEXT`.
- GitHub issues are active experiment lanes, not a fixed syllabus.
- Closed legacy issues remain historical provenance only.
- Do not route new work through a closed issue unless a current failure revives its mechanism.
- Re-evaluate the queue after each resolved experiment or integrated C-1N failure.
- Do not create the next experiment directory until its Iteration 0 prediction exists.
- `docs/research-platform.md` records long-range design. It does not select current work.

## NEXT

### C-1N standing integration bridge

**Status:** NEXT

#24 and #31 are resolved bench evidence. The current work is the C-1N
integration of their measurement model and the evidence-backed proximal hinge.

Do not create another test-bench experiment until the C-1N integration exposes
a concrete physical question and the user has recorded an Iteration 0
prediction.

The integration must keep the gait clock disabled. It must expose support
geometry, center-of-mass projection, contact/load evidence, and torso attitude.
It must not claim `C-1N // 02 · STAND` until fixed evaluation evidence supports
stable equilibrium.

## After STAND

Move directly to #25 learned locomotion. The first learned gait can be ugly. Its failure selects the next simulation lane.

Primary lanes:

- #25 Learn — objective -> policy -> behavior.
- #26 Evaluate — treat behavior as a distribution.
- #27 Model — identify and calibrate simulator parameters from rollouts.
- #28 Uncertainty — train and test across distributions and shift.
- #29 Differentiate — backpropagate through simulated dynamics.
- #30 Scale — make simulation experiments reproducible, observable, and fast.

Controls, contact mechanics, actuator limits, state estimation, numerical methods, and other robotics concepts are supporting mechanisms. Pull one back in only when a concrete simulation failure makes it necessary.

The intended direction is:

`physical intuition -> support mechanics -> leg reachability -> STAND -> learned locomotion -> distributional evaluation -> system identification and calibration -> uncertainty and randomization -> scalable simulation`

## Long-range design

`docs/research-platform.md` owns the design for procedural validated worlds, reproducible rollout populations, and scientifically constrained agentic experimentation.

Keep that design inactive until all three conditions exist:

1. C-1N has earned `STAND`.
2. A learned locomotion loop can produce rollout populations.
3. A concrete failure requires more scale, reproducibility, validation, or structured analysis.

Use current experiment failures to select the next learning or engineering block. Do not build platform infrastructure only because it appears in the long-range design.
