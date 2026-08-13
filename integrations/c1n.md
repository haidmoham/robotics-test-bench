# C-1N integration target

Target repository: `haidmoham/spider` (legacy repository slug; public robot identity: **C-1N**)

C-1N is the longitudinal simulation robot. It integrates bench concepts and preserves visible checkpoints as the simulation becomes more physically grounded, statistically evaluated, and increasingly learned.

The current cross-repository standing requirements and gates live in
[`requirements.md`](requirements.md).

## Identity and checkpoint grammar

Public checkpoints use:

```text
C-1N // NN · CODENAME
```

The number preserves chronology. The codename records a capability or understood failure worth comparing with prior behavior.

Current lineage:

```text
C-1N // 00 · POSE     historical motor-assisted static-pose baseline
C-1N // 01 · SHUFFLE  current coordinated gait failure
C-1N // 02 · STAND    reserved for first support-aware stable stance
C-1N // 03 · STRIDE   reserved for first materially better sustained walk
```

`POSE` does not demonstrate standing. `STAND` and `STRIDE` are reserved names, not completed capabilities.

## Contract

- The test bench isolates questions and repairs mental models.
- C-1N integrates learned mechanisms into one evolving robot.
- Treat this work as a situated engineering apprenticeship. The objective is
  both a working robot and the user's end-to-end physical understanding of why
  it works or fails.
- Use Jupyter as the shared reasoning surface. Set up geometry, force, or
  telemetry evidence first. Explain what each observable means. Then let the
  user form their own prediction before revealing a result or proposing a
  hypothesis.
- Do not supply a prediction for the user to accept or falsify. Ask for a
  prediction only when the physical mechanism is the learning target. Do not
  mistake response time for a blocker.
- Use the active goal as a routing and quality guardrail. It must not pressure
  the user, replace explanation with hill-climbing, or redefine understanding
  as a secondary deliverable.
- Preserve useful failures. Do not rewrite the project history into a clean final demo.
- C-1N is simulation-first. Hardware integration is not a required checkpoint or graduation step.
- Physics and controls remain necessary because learned and simulated behavior must be physically interpretable.
- After the standing foundation, prefer integrations that deepen simulation, statistics, optimization, evaluation, model inference, uncertainty, or learned behavior.
- A bench issue never requires C-1N work for closure unless its own contract explicitly defines a post-close integration checkpoint.
- Instrumentation alone does not require a public checkpoint.
- Keep browser and WASM work downstream of useful simulation behavior. The web surface exposes evidence; it does not create the learning target.

## Required standing bridge

Issue #24 is the current foundation.

First isolate static support in the bench. Define standing through contact geometry, center-of-mass projection, support load, body moment, and reproducible rollout behavior.

Then transfer that measurement model to C-1N with the gait clock disabled.

The `C-1N // 02 · STAND` checkpoint requires:

- support-aware contact evidence;
- center-of-mass/support geometry in a shared frame;
- torso attitude over a fixed rollout;
- a stated success tolerance or failure condition;
- repeatable evidence that the robot maintains stable support rather than only initializing into a plausible pose.

Standing is required because later locomotion objectives and evaluation need a physically meaningful baseline. It is not a commitment to a controls or hardware career path.

## Simulation-first hook targets

| Bench lane | C-1N integration |
| --- | --- |
| #24 Foundation — support state | Establish the first support-aware stable stance and preserve it as `C-1N // 02 · STAND`. |
| #25 Learn — learned locomotion | Train a locomotion policy. Preserve objective exploits and the first understandable learned failure. `STRIDE` requires materially better sustained locomotion under fixed evaluation. |
| #26 Evaluate — behavior as a distribution | Evaluate C-1N across fixed seeds, initial conditions, and scenarios. Compare distributions, not cherry-picked rollouts. |
| #27 Model — simulator calibration | Hide one interpretable C-1N model parameter, estimate it from one rollout set, and validate it on another. |
| #28 Uncertainty — distributions and shift | Randomize a small set of understood physical or sensing parameters and measure in-distribution and held-out degradation. |
| #29 Differentiate — differentiable dynamics | Propagate rollout loss to one interpretable simulated quantity and verify the gradient numerically. |
| #30 Scale — simulation systems | Make C-1N rollouts reproducible, batchable, observable, and fast enough for population-level experiments. |

These are lanes, not a fixed order after `STAND`. Learned locomotion is the first forcing function. Its failures choose which lane becomes useful next.

## Supporting mechanisms

Legacy topics such as trajectory tracking, contact mechanics, actuator limits, state estimation, or numerical sensitivity are not deleted knowledge. They are no longer permanent open routes.

Bring one back when a current C-1N or bench failure makes it causally necessary. Create a focused experiment for the actual failure instead of restoring the old concept graph.

## Version rule

Create a new checkpoint only when a capability or understood failure is worth preserving and comparing with prior behavior. Do not increment for instrumentation, cleanup, presentation polish, a new training run, or elapsed time.

The intended evidence loop is:

`bench question -> prediction -> simulation evidence -> model update -> C-1N integration -> population evaluation -> new failure -> next bench question`
