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
