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

Does the existing articulated tripod remain supported when a centered ballast is added over a fixed rollout?

### Human prediction

The centered ballast adds weight without a sideways COM shift. Without perturbation, the contacts should remain roughly balanced, none should be lost, no tipping edge should dominate, and roll/pitch should remain near zero.

The next requested comparison is an explicit, finite horizontal push. Its
prediction and interpretation remain pending human input; it must not be
collapsed into the no-perturbation baseline.

## R — Response summary

The #24 experiment should reuse the bench's existing articulated tripod and
its centered hold, while measuring actual support state. The ballast is the
only new physical-model variable.

## E — Human evaluation

### Rejected

- The initial scaffold was a pair of boxes supported by three balls. The human
  rejected it because it did not exercise an actual tripod construction.

### Verification required

- Run the corrected two-second articulated-tripod rollout and compare its
  observations with the prediction.

## A — Action

Duplicated the existing three-leg, two-joint tripod construction and its
centered posture/support hold into this experiment. Added a separate settled
no-ballast ghost model as the static visual reference, and a centered 10 kg
treatment ballast with COM projection, contact-load, and attitude telemetry.

## O — Outcome

The two-second corrected rollout ended with all three tripod feet active.
Measured normal loads were approximately `9.71 N` at each foot. The COM
projection was inside the three-contact support triangle. Maximum absolute roll
was below `4e-14 degrees`, maximum absolute pitch was `0.001283 degrees`, and
final body height was `0.884162 m`.

### Effect on current belief

- Before: the 0.45 kg centered-ballast baseline was predicted to preserve
  balanced support.
- After: the articulated-tripod rollout produced the predicted contact and
  attitude pattern for that baseline. The 10 kg treatment has no recorded
  human prediction or interpretation yet.
- Evidence status: one deterministic observation on the corrected 0.45 kg
  model. The earlier rigid-body scaffold result is superseded.

## AI-20260811-002 — Visual comparison starting convention

```yaml
id: AI-20260811-002
date: 2026-08-11
sources:
  - kind: chat
    system: chat
    reference: user instruction in this session
  - kind: coding-agent
    system: Codex
    reference: robotics-test-bench viewer infrastructure
status: acted
evaluation: confirmed
repo_state:
  repository: robotics-test-bench
  branch: codex/static-support-centered-ballast
  commit:
  changed_files:
    - AGENTS.md
    - README.md
    - experiments/telemetry.py
    - experiments/viewer_runtime.py
    - experiments/2026-08-11-static-support-centered-ballast/static_support.py
related:
  experiment: experiments/2026-08-11-static-support-centered-ballast
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [24]
  files:
    - AGENTS.md
    - experiments/telemetry.py
    - experiments/viewer_runtime.py
objects:
  question: Q-20260811-002
  response: R-20260811-002
  evaluation: E-20260811-002
  action: A-20260811-002
  outcome: O-20260811-002
librarian:
  status: not-needed
  record_ids: []
```

## Q — Question

How should future test-bench comparisons become visually inspectable before
their telemetry is interpreted?

## R — Response summary

Use a labelled control, a deliberately legible treatment, a control ghost
overlay, and the shared telemetry stack. Launch the viewer first; preserve
headless output as the evidence channel.

## E — Human evaluation

### Accepted

- Make this the project-local default for comparison-oriented experiments.

## A — Action

Added the convention to the repository instructions and root working rules.
The shared `add_ghost_model_geoms` helper supplies the viewer-only overlay;
the shared `WallClockPlayback` helper supplies smooth wall-clock pacing by
batching fixed physics steps before each viewer sync. The static-support
experiment demonstrates both. `TelemetryPager` keeps all signals sampled while
showing one three-panel analytical page at a time; attached MuJoCo figures are
rendered on every video frame, so page selection protects the scene frame
budget even when figure data publication is already throttled.

## O — Outcome

Project-local convention recorded. It does not assert a physical result or
replace an experiment's prediction, controls, or headless validation.

## AI-20260811-003 — Ballast-mass comparison evidence

```yaml
id: AI-20260811-003
date: 2026-08-11
sources:
  - kind: chat
    system: chat
    reference: user decision to forward-offset the treatment and report of unexpected 10 kg fall rate
  - kind: chat
    system: chat
    reference: user's support-projection interpretation after the 1–100 kg mass sweep
  - kind: coding-agent
    system: Codex
    reference: two-second deterministic headless rollouts
status: acted
evaluation: observed
repo_state:
  repository: robotics-test-bench
  branch: codex/static-support-centered-ballast
  commit:
  changed_files:
    - experiments/2026-08-11-static-support-centered-ballast/static_support.py
    - experiments/2026-08-11-static-support-centered-ballast/README.md
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
  question: Q-20260811-003
  response: R-20260811-003
  evaluation: E-20260811-003
  action: A-20260811-003
  outcome: O-20260811-003
librarian:
  status: pending
  record_ids: []
```

## Q — Question

What changes in the fixed two-second headless rollout when the purposefully
forward-offset treatment ballast is 1 kg rather than 10 kg?

### Human prediction history

The original centered-ballast prediction remains preserved in
`AI-20260811-001`: added weight without a sideways COM shift was expected to
retain balanced contact loads and near-zero roll/pitch. The user subsequently
purposefully shifted the treatment ballast forward to destabilize the case and
reported not expecting the 10 kg fall to be so rapid. No 1 kg prediction or
human physical interpretation has been recorded.

## R — Response summary

Make 1 kg the default treatment mass and expose `--ballast-mass` so the 10 kg
case remains reproducible at the same recorded ballast position.

## E — Evaluation

Observed deterministic headless output. The user now interprets the 10 kg
case as the forward ballast shifting the combined robot-and-ballast
center-of-mass ground projection outside the robot's supporting ground region,
which initiates the tip. This is a human interpretation, not independently
verified mechanism evidence.

## A — Action

Set the default treatment ballast to 1 kg and added `--ballast-mass` for an
explicit mass comparison.

## O — Outcome

At two seconds, final angular velocity was approximately
`[4.81e-16, 0.00045124, 6.72e-17] rad/s` at 1 kg and
`[-5.20e-16, 1.38365267, 4.87e-14] rad/s` at 10 kg. Maximum absolute pitch
was `0.113972 degrees` at 1 kg and `24.756557 degrees` at 10 kg. These are
observations, not an interpretation of the mechanism.

### Effect on current belief

- Before: the rapid 10 kg fall was surprising; no 1 kg interpretation had
  been recorded.
- After: the user’s working model is that the combined center-of-mass ground
  projection passes outside the supporting ground region as the forward
  ballast increases, creating the tip.
- Evidence status: human interpretation grounded in the recorded deterministic
  sweep; it remains to be tested against the measured support boundary and
  contact geometry.
