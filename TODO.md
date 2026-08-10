# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item is `NEXT`.
- GitHub issues are active experiment lanes, not a fixed syllabus.
- Closed legacy issues remain historical provenance only. Do not route new work through them unless a current failure explicitly revives the concept.
- Re-evaluate the queue after each resolved experiment or integrated C-1N failure.
- Do not create the next experiment directory until its Iteration 0 prediction exists.

## NEXT

### #24 Foundation — support state: make standing measurable

**Status:** NEXT

The immediate goal is still to learn what makes C-1N stand for real.

First isolate static support in the bench. Make this chain physical and measurable:

`contact geometry + center-of-mass projection -> support load -> net body force/moment -> body attitude`

Define standing as reproducible rollout behavior, not a visually plausible pose.

After #24 closes, transfer the measurement model to C-1N. Build a stance-only integration with the gait clock disabled. Expose support geometry, center-of-mass projection, contact/load evidence, and torso attitude. If the robot demonstrates support-aware stable equilibrium under a fixed evaluation, preserve that boundary as `C-1N // 02 · STAND`.

Do not improve walking as part of the standing experiment.

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

`physical intuition -> STAND -> learned locomotion -> statistical simulation / model inference / uncertainty / differentiable dynamics / scale`

Hardware is not a graduation requirement for this bench.