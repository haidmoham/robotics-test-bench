# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item is `NEXT`.
- GitHub issues are active experiment lanes, not a fixed syllabus.
- Closed legacy issues remain historical provenance only. Do not route new work through them unless a current failure explicitly revives the concept.
- Re-evaluate the queue after each resolved experiment or integrated C-1N failure.
- Do not create the next experiment directory until its Iteration 0 prediction exists.

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

Move directly to #25 learned locomotion. The first learned gait is allowed to be ugly. Its failure selects the next simulation lane.

Primary lanes:

- #25 Learn — objective -> policy -> behavior.
- #26 Evaluate — treat behavior as a distribution.
- #27 Model — identify and calibrate simulator parameters from rollouts.
- #28 Uncertainty — train and test across distributions and shift.
- #29 Differentiate — backpropagate through simulated dynamics.
- #30 Scale — make simulation experiments reproducible, observable, and fast.

Controls, contact mechanics, actuator limits, state estimation, numerical methods, or other robotics concepts are supporting mechanisms. Pull them back in only when a concrete simulation failure makes them necessary.

The intended direction is:

`physical intuition -> support mechanics -> leg reachability -> STAND -> learned locomotion -> statistical simulation / model inference / uncertainty / differentiable dynamics / scale`

Hardware is not a graduation requirement for this bench.
