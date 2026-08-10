# Agent log

## AI-20260809-011 — Shared-frame Jacobian prediction

```yaml
id: AI-20260809-011
date: 2026-08-09
sources:
  - kind: chat
    system: Codex
    reference: current task
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: main
  commit:
  changed_files:
    - experiments/2026-08-09-jacobians-task-space/README.md
    - experiments/2026-08-09-jacobians-task-space/jacobians_task_space.py
    - experiments/2026-08-09-jacobians-task-space/agent-log.md
    - experiments/telemetry.py
related:
  experiment: experiments/2026-08-09-jacobians-task-space
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [6]
  files:
    - experiments/2026-08-09-jacobians-task-space/README.md
    - experiments/2026-08-09-jacobians-task-space/jacobians_task_space.py
    - experiments/telemetry.py
objects:
  question: Q-20260809-011
  response: R-20260809-011
  evaluation: E-20260809-011
  action: A-20260809-011
  outcome: O-20260809-011
librarian:
  status: pending
  record_ids: []
```

## Q — Question

How does the same small positive first-joint perturbation map into shared-frame foot X motion as the base orientation changes?

### Human prediction

Holding geometry, joint pose, perturbation size, controller, and timestep fixed, the same small positive first-joint perturbation should produce a large shared-X foot displacement at 0 degrees, near-zero X displacement at 90 degrees, and an equally large displacement with the opposite X sign at 180 degrees. The foot should keep moving at 90 degrees, but along shared Z. At 45 and 135 degrees, the shared-X magnitude should be about 71% of the 0-degree magnitude, with opposite signs.

### Purpose

Make the joint-space-to-task-space mapping observable before adding foot telemetry to C-1N.

### Context supplied

- `TODO.md` issue #6 selector.
- C-1N's shared-frame joint-space versus foot-motion mismatch.
- A one-link planar geometry chosen to isolate frame orientation.

## R — Response summary

Use a fixed shared frame and rotate only the base. Compare joint telemetry with foot X telemetry, and validate the X Jacobian entry with a centered finite difference.

## E — Human evaluation

### Accepted

- A local foot-motion vector can stay nonzero while its shared-X component vanishes.
- At the initial straight-down pose, base orientation changes the X projection of the same local joint perturbation.

### Verification required

- Run 0, 90, and 180 degree cases and compare the Jacobian with the finite-difference estimate.
- Check whether observed initial X motion supports the predicted sign reversal and near-zero 90-degree projection.

## A — Action

Scaffolded a one-link MuJoCo experiment that varies only base pitch, reports joint and foot X position/velocity/acceleration, prints MuJoCo-versus-finite-difference Jacobian telemetry, and adds a three-orientation viewer overlay with C-1N's rolling graph-stack pattern for direct visual comparison.

## O — Outcome

Pending experiment run.

### Effect on current belief

- Before: synchronized joint commands were not yet connected to shared-frame foot motion.
- After: the working prediction is that base orientation rotates the local foot-motion vector and changes only its shared-frame projection.
- Evidence status: Human-accepted conceptual prediction; simulation observation is pending.

## Librarian update

```yaml
source:
  repository: robotics-test-bench
  path: experiments/2026-08-09-jacobians-task-space/agent-log.md
  commit:
provenance:
  - kind: chat
    system: Codex
    reference: current task
objects:
  - id: Q-20260809-011
    type: Question
    summary: How does one joint perturbation map into shared-frame foot X motion across base orientations?
    status: open
  - id: R-20260809-011
    type: Response
    summary: Use a one-link planar model, fixed shared frame, and finite-difference Jacobian check.
    status: acted
  - id: E-20260809-011
    type: Evaluation
    summary: The human accepted the projection-based prediction; simulation verification remains pending.
    status: unconfirmed
  - id: A-20260809-011
    type: Action
    summary: Scaffolded base-orientation comparisons with joint and task-space telemetry.
    status: completed
  - id: O-20260809-011
    type: Outcome
    summary: Pending runs at 0, 90, and 180 degrees.
    status: pending
relations:
  - subject: Q-20260809-011
    predicate: receives
    object: R-20260809-011
  - subject: R-20260809-011
    predicate: receives
    object: E-20260809-011
  - subject: E-20260809-011
    predicate: causes
    object: A-20260809-011
  - subject: A-20260809-011
    predicate: produces
    object: O-20260809-011
unresolved_questions:
  - Do the observed initial X Jacobian signs and magnitudes match the prediction across orientations?
superseded_claims: []
```

Related: #6

## AI-20260809-014 — Equal-foot-force failure is evidence, not a #6 fix target

```yaml
id: AI-20260809-014
date: 2026-08-09
sources:
  - kind: human-observation
    system: Codex
    reference: current task
  - kind: coding-agent
    system: Codex
    reference: headless tripod run
status: acted
evaluation: unconfirmed
related:
  experiment: experiments/2026-08-09-jacobians-task-space
  issues: [6, 20]
  files:
    - experiments/2026-08-09-jacobians-task-space/tripod_static_support.py
objects:
  question: Q-20260809-014
  response: R-20260809-014
  evaluation: E-20260809-014
  action: A-20260809-014
  outcome: O-20260809-014
librarian:
  status: pending
  record_ids: []
```

## Q — Question

Should the equal-foot-force tripod experiment be extended into a standing controller, or should any impossible negative rear normal-force request be deferred to #20 if it is observed?

## R — Response summary

No. Keep #6 scoped to physically inspecting the joint-motion → foot-motion → Jacobian → torque chain. Treat feasible force allocation, contact feedback, friction, and planted-foot control as #20 work.

## E — Human evaluation

### Accepted

- The equal-force failure is useful evidence, not a defect to conceal.
- #6 must not solve full standing control.

## A — Action

Marked the tripod code and local README with the #6 boundary; retained the equal-foot-force behavior unchanged.

## O — Outcome

The checked 2 s and 8 s forward headless runs kept rear vertical allocations positive. A negative normal-force request remains an unverified diagnostic condition for #20, not evidence from the current run.

### Effect on current belief

- Before: the tripod continuation risked expanding into a standing controller.
- After: it is a bounded physical inspection of Jacobian-transpose torque mapping; contact-feasibility control is explicitly deferred to #20.
- Evidence status: The scoped force-mapping behavior was run locally; the negative-normal condition is not yet reproduced. The scope decision is human-directed.

Related: #6, #20

## AI-20260809-013 — Static tripod support prediction

```yaml
id: AI-20260809-013
date: 2026-08-09
sources:
  - kind: chat
    system: Codex
    reference: current task
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: codex/responsive-jacobian-overlay
  commit:
  changed_files:
    - experiments/2026-08-09-jacobians-task-space/tripod_static_support.py
    - experiments/2026-08-09-jacobians-task-space/README.md
    - experiments/2026-08-09-jacobians-task-space/agent-log.md
related:
  experiment: experiments/2026-08-09-jacobians-task-space
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [6]
  files:
    - experiments/2026-08-09-jacobians-task-space/tripod_static_support.py
objects:
  question: Q-20260809-013
  response: R-20260809-013
  evaluation: E-20260809-013
  action: A-20260809-013
  outcome: O-20260809-013
librarian:
  status: pending
  record_ids: []
```

## Q — Question

How can three planted two-joint legs hold a free body under gravity while the body load shifts forward?

### Human prediction

Each leg needs a joint-space posture controller to maintain a usable bent configuration. Gravity and the body/COM position determine three ground-support forces; shifting forward increases the front force and decreases the rear forces. Each leg maps its assigned foot force into joint torques with its Jacobian transpose. If the support point reaches the triangle edge, lowering the body alone does not restore static balance: fixed feet must move the body projection back, while a walking robot can step.

### Purpose

Apply #6's pose-dependent foot Jacobian to the smallest physically grounded standing problem without adding gait logic.

## R — Response summary

Separate posture regulation from support-force allocation. Use the whole-robot free-body balance to choose foot forces, then use each leg's `J(q).T @ f` to map its assigned force into motor torques.

## E — Human evaluation

### Accepted

- Posture torque is derived from joint configuration error, not from the foot-force allocation.
- Ground reactions are external whole-robot forces; actuator torques appear only when isolating a leg.

### Verification required

- Centered run holds body height with all three positive support forces.
- A forward load-shift run increases the front vertical allocation and decreases both rear allocations.

## A — Action

Added a minimal MuJoCo tripod with a free body, three planted two-joint legs, a posture PD term, and Jacobian-transpose support torques. Added the local free-body diagram asset as the visual reference for the experiment and future portfolio post.

## O — Outcome

Pending the centered hold and one forward-load perturbation.

### Effect on current belief

- Before: the Jacobian was understood as a local motion map but not yet connected to static foot support.
- After: standing is modeled as posture regulation plus a force allocation whose per-leg forces become motor torques through `J(q).T @ f`.
- Evidence status: Human prediction accepted; physical simulation observation is pending.

Related: #6

## AI-20260809-012 — Two-joint velocity-map continuation

```yaml
id: AI-20260809-012
date: 2026-08-09
sources:
  - kind: chat
    system: Codex
    reference: current task
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: codex/responsive-jacobian-overlay
  commit:
  changed_files:
    - experiments/2026-08-09-jacobians-task-space/README.md
    - experiments/2026-08-09-jacobians-task-space/two_joint_planar_leg.py
    - experiments/2026-08-09-jacobians-task-space/agent-log.md
related:
  experiment: experiments/2026-08-09-jacobians-task-space
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [6]
  files:
    - experiments/2026-08-09-jacobians-task-space/two_joint_planar_leg.py
objects:
  question: Q-20260809-012
  response: R-20260809-012
  evaluation: E-20260809-012
  action: A-20260809-012
  outcome: O-20260809-012
librarian:
  status: pending
  record_ids: []
```

## Q — Question

How does the same small two-joint velocity map into foot velocity when only the planar leg pose changes?

### Human prediction

Not yet recorded. Predict the relative world-X and world-Z foot motion before running the two poses.

### Purpose

Continue #6 from one Jacobian column and a rotated frame to the complete 2-by-2 planar velocity map, without introducing locomotion.

## R — Response summary

Set the same `qdot` at two fixed poses, compare `J(q) @ qdot` to MuJoCo's foot velocity, then attribute any velocity change to the changed local map rather than to a changed command.

## E — Human evaluation

### Verification required

- Confirm that predicted and MuJoCo-reported X-Z foot velocities agree at both poses.
- Record the learner's prediction and observed pose-dependent change before explaining it further.

## A — Action

Added the two-joint planar-leg velocity comparison as a continuation inside the active #6 directory, with an optional viewer that alternates the two evaluated poses.

## O — Outcome

Pending the learner's prediction and observation.

### Effect on current belief

- Before: the one-link comparison connected a single joint column to task-space motion across frames.
- After: the next test isolates the full local two-joint velocity mapping while holding `qdot` fixed.
- Evidence status: Experiment scaffold only; no learner interpretation is recorded.

Related: #6
