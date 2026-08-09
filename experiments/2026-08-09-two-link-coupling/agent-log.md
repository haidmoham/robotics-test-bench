# Agent log

## AI-20260809-001 — Multi-DOF coupling

```yaml
id: AI-20260809-001
date: 2026-08-09
agent: Codex
status: resolved
evaluation: confirmed
repo_state:
  repository: robotics-test-bench
  branch: main
  commit:
  changed_files:
    - experiments/2026-08-09-two-link-coupling/README.md
    - experiments/2026-08-09-two-link-coupling/two_link_coupling.py
    - experiments/2026-08-09-two-link-coupling/agent-log.md
related:
  experiment: experiments/2026-08-09-two-link-coupling
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: [2]
  files:
    - experiments/2026-08-09-two-link-coupling/README.md
    - experiments/2026-08-09-two-link-coupling/two_link_coupling.py
objects:
  question: Q-20260809-001
  response: R-20260809-001
  evaluation: E-20260809-001
  action: A-20260809-001
  outcome: O-20260809-001
librarian:
  status: pending
  record_ids: []
```

## Q — Question

How does commanding joint 1 change joint 2's behavior in a planar two-link arm, and what does that reveal about multi-joint dynamics?

### Human prediction

For the passive-elbow run, expect a janky, loosely waving arm: shoulder-driven motion with the elbow trailing or moving in a way that was not explicitly commanded.

### Refined prediction

The elbow motor never drives in passive mode, so the observed flopping should be understood as the behavior of an unpowered joint rather than a motor that is too weak to overcome gravity.

### Next prediction

With joint 2 switched to `hold` while keeping elbow-down configuration and normal gravity, expect a more distinctive, intentional-looking motion than the passive flopping.

### Gravity-off prediction

With gravity disabled, expect the staged motion to look cleaner because the motors do not need to oppose the gravitational load.

### Purpose

Move beyond one-joint control intuition with the smallest experiment that can expose state-dependent multi-joint dynamics.

### Context supplied

- GitHub issue #2.
- The prior one-link pendulum experiment.
- Direct MuJoCo access to `qpos`, `qvel`, `ctrl`, and `qacc`.

## R — Response summary

A two-link MuJoCo arm was used to compare a passive elbow, a held elbow, and gravity-on/off behavior while keeping the controller deliberately simple.

## E — Human evaluation

### Accepted

- In the passive, elbow-down run with normal gravity, joint 2 visibly moved while only joint 1 was commanded.
- The motion was qualitatively close to the predicted janky, loosely waving arm.
- With the same configuration and gravity but `joint2_mode=hold`, the motion became more organized and wave-like.
- With gravity disabled, the staged motion looked cleaner and more recognizable, matching the gravity-off prediction.
- The experiment made the important distinction between physical coupling and controller-imposed coupling visible. Explicit target cross-feed can create a coordinated gesture, but it is not evidence for the passive physical coupling that motivated issue #2.
- Further parameter search for a more exact wave was judged to have low learning value once the coupling behavior was understood.

### Rejected

- “The elbow motor is too weak to overcome gravity” was rejected. In passive mode, the elbow motor receives `ctrl[1] = 0.0` and never drives.

### Deferred

- A precise decomposition of which coupling effects dominate across pose, gravity, and velocity can be revisited when a later experiment needs it.
- The elbow-up comparison remains available as a follow-up, but it is not required for the current learning target.

### Verification required

None for the current closure. Deferred comparisons should make a fresh prediction if they are revisited.

## A — Action

Built the minimal two-link experiment, compared passive and held joint-2 behavior, and tested a gravity-off case. Added a coordinated wave mode for exploration, then stopped waveform tuning when it no longer tested the multi-DOF mental model.

## O — Outcome

Issue #2 is resolved for now. The experiment produced direct evidence that one joint's behavior cannot be reasoned about as an isolated pendulum once it is part of a moving two-link system. The passive elbow moved with zero elbow command, changing joint-2 control changed the motion, and removing gravity changed the resulting behavior.

The recognizable wave was useful as an engaging visualization, but reproducing a particular waveform became a controller-tuning search rather than the learning target.

### Effect on current belief

The independent-joint mental model is insufficient for this system. Multi-joint behavior depends on the state and motion of the full mechanism, not only the local command at each joint. The next useful work does not need more tuning of this experiment.

## Librarian update

```yaml
source:
  repository: robotics-test-bench
  path: experiments/2026-08-09-two-link-coupling/agent-log.md
  commit:
objects:
  - id: Q-20260809-001
    type: Question
    summary: How does driving one joint affect the other joint in a two-link arm?
    status: resolved
  - id: R-20260809-001
    type: Response
    summary: Used a minimal two-link comparison with passive/held elbow behavior and gravity as discriminating conditions.
    status: confirmed
  - id: E-20260809-001
    type: Evaluation
    summary: Passive joint 2 moved with zero elbow command; holding it changed the motion; gravity-off behavior changed as predicted; waveform tuning stopped when it ceased to test the coupling model.
    status: confirmed
  - id: A-20260809-001
    type: Action
    summary: Built and ran the two-link coupling experiment, compared meaningful control conditions, and stopped presentation-oriented tuning after the learning target was met.
    status: completed
  - id: O-20260809-001
    type: Outcome
    summary: Independent-joint intuition was replaced by a full-state multi-joint mental model; issue #2 is resolved for now.
    status: resolved
relations:
  - subject: Q-20260809-001
    predicate: receives
    object: R-20260809-001
  - subject: R-20260809-001
    predicate: receives
    object: E-20260809-001
  - subject: E-20260809-001
    predicate: causes
    object: A-20260809-001
  - subject: A-20260809-001
    predicate: produces
    object: O-20260809-001
unresolved_questions:
  - Deferred: which coupling terms dominate across pose, gravity, and velocity when a later task requires that decomposition?
superseded_claims:
  - The initial motor-strength explanation was superseded by the code-level observation that passive joint 2 is unpowered.
```

Related: #2
