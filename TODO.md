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

### #24 Foundation — support state: make standing measurable

**Status:** NEXT

The immediate goal is to learn what makes C-1N stand for real.

First isolate static support in the bench. Make this chain physical and measurable:

`contact geometry + center-of-mass projection -> support load -> net body force/moment -> body attitude`

Define standing as reproducible rollout behavior, not as a visually plausible pose.

Do not improve walking as part of the standing experiment.

## Before C-1N STAND

### #31 Foundation — leg workspace: separate reachability from gravity compensation

Run #31 after #24 and before the C-1N standing integration.

#24 establishes the support geometry that C-1N needs and the measurements that evaluate it. #31 then asks whether the current leg axes and degrees of freedom can realize that geometry.

Test one fixed-body leg first. Compare the current reachable workspace with one outward-and-down support target. Add one orthogonal proximal hip degree of freedom only if the current morphology cannot reach the target.

Keep the distinction explicit:

`joint axes + joint limits -> reachable workspace -> available support geometry`

Then, only after the pose is reachable:

`reachable pose + gravity/contact -> required joint torque`

Do not modify all six legs until the one-leg experiment shows that the extra degree of freedom is necessary.

After #31 closes, transfer #24's measurement model and any evidence-backed morphology change through `haidmoham/spider#11`.

Build a stance-only integration with the gait clock disabled. Expose support geometry, center-of-mass projection, contact load, and torso attitude. Create `C-1N // 02 · STAND` only after the robot demonstrates support-aware stable equilibrium under a fixed evaluation.

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
