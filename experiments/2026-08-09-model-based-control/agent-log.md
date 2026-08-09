# Agent log

## AI-20260809-004 — Iteration 0 prediction

id: AI-20260809-004
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
  question: Q-20260809-004
  response: R-20260809-004
  evaluation: E-20260809-004
  action: A-20260809-004
  outcome: O-20260809-004
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

- Whether the visual motion, periodic steady-state tracking error, and feedback control effort show that prediction.

## A — Action

Recorded the Iteration 0 prediction before launching the two visual comparison conditions.

## O — Outcome

Pending visual comparison.

### Effect on current belief

The belief that compensation makes the control job easier is retained, while “faster” has been marked as an ambiguous visual proxy rather than a direct speed prediction. No experiment observation has changed the belief yet.

## Librarian update

```yaml
source:
  repository: robotics-test-bench
  path: experiments/2026-08-09-model-based-control/agent-log.md
  commit:
objects:
  - id: Q-20260809-004
    type: Question
    summary: What should gravity compensation change when the plant, target, and PD gains are fixed?
    status: answered-as-prediction
  - id: R-20260809-004
    type: Response
    summary: Gravity compensation should reduce the burden on PD feedback.
    status: recorded
  - id: E-20260809-004
    type: Evaluation
    summary: The prediction is plausible but still needs observation and telemetry.
    status: unconfirmed
  - id: A-20260809-004
    type: Action
    summary: Recorded Iteration 0 before running either controller condition.
    status: completed
  - id: O-20260809-004
    type: Outcome
    summary: Visual and telemetry comparison pending.
    status: pending
relations:
  - subject: Q-20260809-004
    predicate: receives
    object: R-20260809-004
  - subject: R-20260809-004
    predicate: receives
    object: E-20260809-004
  - subject: E-20260809-004
    predicate: causes
    object: A-20260809-004
  - subject: A-20260809-004
    predicate: produces
    object: O-20260809-004
unresolved_questions:
  - Do the visual motion and telemetry support the prediction?
superseded_claims: []
```

Related: #4

## AI-20260809-005 — Visual comparison observation

id: AI-20260809-005
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
  question: Q-20260809-005
  response: R-20260809-005
  evaluation: E-20260809-005
  action: A-20260809-005
  outcome: O-20260809-005
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

## Librarian update

```yaml
source:
  repository: robotics-test-bench
  path: experiments/2026-08-09-model-based-control/agent-log.md
  commit:
objects:
  - id: Q-20260809-005
    type: Question
    summary: What visible difference does gravity compensation produce relative to baseline PD?
    status: answered-by-observation
  - id: R-20260809-005
    type: Response
    summary: The compensated arm looked more fluid and coordinated.
    status: observed
  - id: E-20260809-005
    type: Evaluation
    summary: The visual difference is real, but its mechanism is not established.
    status: unconfirmed
  - id: A-20260809-005
    type: Action
    summary: Recorded the visual observation without causal overclaiming.
    status: completed
  - id: O-20260809-005
    type: Outcome
    summary: Telemetry comparison remains pending.
    status: pending
relations:
  - subject: Q-20260809-005
    predicate: receives
    object: R-20260809-005
  - subject: R-20260809-005
    predicate: receives
    object: E-20260809-005
  - subject: E-20260809-005
    predicate: causes
    object: A-20260809-005
  - subject: A-20260809-005
    predicate: produces
    object: O-20260809-005
unresolved_questions:
  - Does the visual difference correspond to lower feedback effort or tracking error?
superseded_claims: []
```

Related: #4

## AI-20260809-006 — Mathematical interpretation

id: AI-20260809-006
date: 2026-08-09
agent: Codex
status: acted
evaluation: unconfirmed
repo_state:
  repository: robotics-test-bench
  branch: main
  commit: eff6885
  changed_files:
    - experiments/2026-08-09-model-based-control/agent-log.md
related:
  experiment: experiments/2026-08-09-model-based-control
  issues: [4]
objects:
  question: Q-20260809-006
  response: R-20260809-006
  evaluation: E-20260809-006
  action: A-20260809-006
  outcome: O-20260809-006
librarian:
  status: pending
  record_ids: []

## Q — Question

Why might the gravity-compensation arm look more coordinated or fluid?

## R — Response summary

For manipulator dynamics M(q)qdd + C(q,qdot)qdot + g(q) = tau, baseline PD leaves g(q) as a disturbance. PD plus gravity compensation adds an estimate of g(q), so the feedback loop handles mainly tracking error and residual dynamic terms.

## E — Human evaluation

### Accepted

- The hypothesis is mathematically plausible: removing the configuration-dependent gravity forcing can reduce uneven corrective errors between joints.

### Unresolved

- The total torque command need not be smaller because it includes the explicit gravity torque.
- The current visual impression still needs a split between feedback torque and gravity torque to test “easier” directly.

## A — Action

Derived the error dynamics and evaluated the initial gravity-torque vector numerically at the experiment's starting pose.

## O — Outcome

At q=(0.35,-0.70), the model's gravity torque is approximately (13.64, 2.58) N·m. A static PD-only balance estimate with Kp=18 is approximately (0.758, 0.143) radians of position error; this is a nonlinear, moving-target comparison aid, not an observed trajectory result.

### Effect on current belief

The fluid-motion observation is consistent with gravity compensation removing a large configuration-dependent forcing term, but visual smoothness alone does not establish lower feedback effort or lower total control effort.

## Librarian update

```yaml
source:
  repository: robotics-test-bench
  path: experiments/2026-08-09-model-based-control/agent-log.md
  commit:
objects:
  - id: Q-20260809-006
    type: Question
    summary: Why might gravity compensation make the arm look more coordinated or fluid?
    status: answered-as-hypothesis
  - id: R-20260809-006
    type: Response
    summary: Gravity compensation removes g(q) from the feedback loop's apparent disturbance when the model is accurate.
    status: mathematically-supported
  - id: E-20260809-006
    type: Evaluation
    summary: The explanation is plausible, but telemetry must separate feedback, gravity, and total torque.
    status: unconfirmed
  - id: A-20260809-006
    type: Action
    summary: Derived the error dynamics and evaluated gravity torque at the starting pose.
    status: completed
  - id: O-20260809-006
    type: Outcome
    summary: The explanation predicts lower feedback burden, not necessarily lower total torque.
    status: hypothesis-refined
relations:
  - subject: Q-20260809-006
    predicate: receives
    object: R-20260809-006
  - subject: R-20260809-006
    predicate: receives
    object: E-20260809-006
  - subject: E-20260809-006
    predicate: causes
    object: A-20260809-006
  - subject: A-20260809-006
    predicate: produces
    object: O-20260809-006
unresolved_questions:
  - Does measured feedback torque decrease under gravity compensation while tracking error improves or stays comparable?
superseded_claims:
  - Treating lower total actuator torque as the direct meaning of “easier” for the feedback controller.
```

Related: #4
