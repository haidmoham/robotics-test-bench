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

`physical intuition -> support mechanics -> leg reachability -> STAND -> learned locomotion -> distributional evaluation -> system identification / calibration -> uncertainty / randomization -> scalable simulation -> procedural validated worlds -> scientifically constrained agentic experimentation`

## Post-foundation frontier

This bench has no fixed terminal capstone. Once learned locomotion produces behavior that can be evaluated across a population, grow the scale lane into a deep-toy simulation research platform. Do not pull this work ahead of a concrete prerequisite: standing, locomotion, and physics repair remain the current foundation.

The target platform should:

- generate structured pseudorandom physical worlds from declared distributions or grammars;
- reject worlds that fail deterministic MuJoCo, physics, semantic, or experiment-specific validators;
- run reproducible rollout populations and retain seeds, manifests, code/simulator versions, metrics, invalid worlds, failures, and artifacts;
- support treatment comparison, failure clustering, counterexample reduction, and scale experiments through typed interfaces.

A natural-language agent is a first-class control-plane objective, not a chatbot wrapper. It must compile research goals into explicit experiment specifications and call typed generation, validation, execution, and analysis operations. Deterministic validators and simulator contracts remain authoritative.

Scientific policy is structural:

- declare hypotheses, interventions, controls, measured variables, and evaluation criteria before execution when applicable;
- retain validation failures; never silently discard them;
- record provenance and distributions for every treatment;
- create a new analysis record when metrics or protocol change after results are seen;
- distinguish observations, inferences, and speculation; include simulator limits and uncertainty in conclusions;
- prevent the agent from silently changing hidden parameters to rescue a failed result;
- require compatible populations and declared conditions for comparisons.

### Routing rule

Use frontier failures to select the next learning block. A failure in world validity can pull in mechanics, numerical methods, or simulator contracts; poor population evidence can pull in statistics or experiment design; a calibration or transfer gap can pull in system identification and uncertainty; throughput or reproducibility limits can pull in simulation or distributed-systems architecture. Do not build infrastructure or study a topic merely because it appears in the final platform.

Hardware is not a graduation requirement for this bench.