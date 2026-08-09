# Agent log

## AI-20260809-003 — Iteration 0 prediction

id: AI-20260809-003
date: 2026-08-09
agent: Codex
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: main
  commit: 57b626d
  changed_files:
    - experiments/2026-08-09-model-based-control/agent-log.md
related:
  experiment: experiments/2026-08-09-model-based-control
  issues: [4]
objects:
  question: Q-20260809-003
  response: R-20260809-003
  evaluation: E-20260809-003
  action: A-20260809-003
  outcome: O-20260809-003
librarian:
  status: pending
  record_ids: []

## Q — Question

With the arm, target, and PD gains unchanged, what effect should adding gravity compensation have?

## R — Response summary

The human prediction was that gravity compensation should make the controller's job easier.

## E — Human evaluation

### Accepted

- Gravity compensation should reduce the burden on the PD feedback.
- Refined prediction: the visual motion may look faster or less delayed, the tracking error may differ with the arm's configuration, and the two controllers will differ in whether their command includes a gravity-related term.

### Clarification

- The experiment changes neither the PD gains nor the plant gravity. It only adds a model-predicted joint-torque vector to the unchanged PD command.
- Tracking error is measured relative to the moving target trajectory, not a fixed reference point.
- Both plants experience gravity; only one controller explicitly estimates and adds a compensating torque.
- “Faster” is not yet a precise prediction because the feedback gains and plant dynamics are unchanged.

### Unresolved

- Whether the visual motion, steady-state error, and control effort show that prediction.

## A — Action

Recorded the Iteration 0 prediction before launching the two visual comparison conditions.

## O — Outcome

Pending visual comparison.

### Effect on current belief

The belief that compensation makes the control job easier is retained, while “faster” has been marked as an ambiguous visual proxy rather than a direct speed prediction. No experiment observation has changed the belief yet.

Related: #4

## AI-20260809-004 — Visual comparison observation

id: AI-20260809-004
date: 2026-08-09
agent: Codex
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: main
  commit: 519eef4
  changed_files:
    - experiments/2026-08-09-model-based-control/agent-log.md
related:
  experiment: experiments/2026-08-09-model-based-control
  issues: [4]
objects:
  question: Q-20260809-004
  response: R-20260809-004
  evaluation: E-20260809-004
  action: A-20260809-004
  outcome: O-20260809-004
librarian:
  status: pending
  record_ids: []

## Q — Question

What visible difference does the gravity-compensation condition produce relative to baseline PD?

## R — Response summary

The human observed that the gravity-compensation run looked more fluid, as if the whole arm moved in greater unison.

## E — Human evaluation

### Accepted

- The visual difference was noticeable in the orange gravity-compensation condition.

### Unresolved

- Whether the appearance corresponds to smaller target-tracking error, lower feedback correction, or a timing/viewpoint difference.

## A — Action

Recorded the visual observation without treating its cause as verified.

## O — Outcome

Pending telemetry comparison.

### Effect on current belief

The prediction that gravity compensation may make the control job easier is qualitatively supported by the visual impression, but the mechanism remains unconfirmed.

Related: #4
