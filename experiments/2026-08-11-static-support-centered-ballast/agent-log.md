# Agent log

## AI-20260811-001 — Centered ballast support baseline

```yaml
id: AI-20260811-001
date: 2026-08-11
sources:
  - kind: human-observation
    system: chat
    reference: Spider #11 SYNTHESIS GATE 0 discussion
  - kind: coding-agent
    system: Codex
    reference: robotics-test-bench #24
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: codex/static-support-centered-ballast
  commit:
  changed_files:
    - experiments/2026-08-11-static-support-centered-ballast/README.md
    - experiments/2026-08-11-static-support-centered-ballast/static_support.py
    - experiments/2026-08-11-static-support-centered-ballast/agent-log.md
related:
  experiment: experiments/2026-08-11-static-support-centered-ballast
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [24]
  files:
    - experiments/2026-08-11-static-support-centered-ballast/static_support.py
objects:
  question: Q-20260811-001
  response: R-20260811-001
  evaluation: E-20260811-001
  action: A-20260811-001
  outcome: O-20260811-001
librarian:
  status: pending
  record_ids: []
```

## Q — Question

Does a passive three-contact body with a centered ballast remain supported over a fixed rollout?

### Human prediction

The centered ballast adds weight without a sideways COM shift. Without perturbation, the contacts should remain roughly balanced, none should be lost, no tipping edge should dominate, and roll/pitch should remain near zero.

## R — Response summary

A minimal free-body MuJoCo rollout can measure COM projection, contact loads, attitude, angular velocity, and height without a controller.

## E — Human evaluation

### Verification required

- Run the two-second rollout and compare its observations with the prediction.

## A — Action

Scaffolded the passive centered-ballast experiment and structured final-state report.

## O — Outcome

The two-second centered-ballast rollout ended with all three contacts active.
Reported normal loads were approximately `4.94 N` at each contact. The COM
projection was inside the three-contact support triangle. Maximum absolute roll
and pitch were below `3e-9 degrees`; final body height was `0.139858 m`.

### Effect on current belief

- Before: centered ballast is predicted to preserve balanced support.
- After: the selected centered rollout produced the predicted contact and
  attitude pattern; causal interpretation remains with the human.
- Evidence status: one deterministic simulation observation.
