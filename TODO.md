# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item is `NEXT`.
- GitHub issues are active experiment lanes, not a fixed syllabus.
- Closed legacy issues remain historical provenance only. Do not route new work through them unless a current failure explicitly revives the concept.
- Re-evaluate the queue after each resolved experiment or integrated C-1N failure.
- Do not create the next experiment directory until its Iteration 0 prediction exists.

## NEXT

### #35 Routing — make Jupyter the scientific front end to the test bench

**Status:** NEXT

Prioritize the notebook and telemetry interface before continuing the static-support lane. Route work through the cheapest valid surface:

`question -> notebook or headless MuJoCo -> structured telemetry/results -> Jupyter analysis -> reusable code or next experiment`

Add a first-class `notebooks/` layer without replacing MuJoCo. Preserve the existing simulator and telemetry infrastructure, make headless results independently consumable, and demonstrate one notebook analyzing stored MuJoCo telemetry. Keep reusable behavior in normal source code and keep robot-behavior claims reproducible from explicit experiments.

After #35 establishes this scientific front end, return to the deferred #24 support experiment and re-evaluate its evidence and analysis path.

## Deferred foundation

### #24 Foundation — support state: make standing measurable

**Status:** Deferred while #35 is active

The immediate goal is still to learn what makes C-1N stand for real.

First isolate static support in the bench. Make this chain physical and measurable:

`contact geometry + center-of-mass projection -> support load -> net body force/moment -> body attitude`

Define standing as reproducible rollout behavior, not a visually plausible pose.

Do not improve walking as part of the standing experiment.

## Before C-1N STAND

### #31 Foundation — leg workspace: separate reachability from gravity compensation

Run #31 after #24 and before the C-1N standing integration.

#24 establishes what support geometry C-1N needs and how to measure it. #31 then asks whether the current leg joint axes and DOFs can physically realize that geometry. Test one fixed-body leg first. Compare the current reachable workspace against one outward-and-down spider-like target. Add an orthogonal proximal hip DOF only if the existing morphology cannot reach the target.

Keep the distinction explicit:

`joint axes + joint limits -> reachable workspace -> available support geometry`

then, only after the pose is reachable:

`reachable pose + gravity/contact -> required joint torque`

Do not modify all six legs until the one-leg experiment provides evidence that the extra DOF is required.

After #31 closes, transfer #24's measurement model and any evidence-backed morphology change to C-1N. Build a stance-only integration with the gait clock disabled. Expose support geometry, center-of-mass projection, contact/load evidence, and torso attitude. If the robot demonstrates support-aware stable equilibrium under a fixed evaluation, preserve that boundary as `C-1N // 02 · STAND`.

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
