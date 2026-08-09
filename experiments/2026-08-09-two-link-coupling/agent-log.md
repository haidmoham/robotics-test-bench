# Agent log

## AI-20260809-001 — Multi-DOF coupling scaffold

```yaml
id: AI-20260809-001
date: 2026-08-09
agent: Codex
status: acted
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

How does commanding joint 1 change joint 2's behavior in a planar two-link arm, and how does that change with configuration, gravity, and joint-2 control?

### Human prediction

For the passive-elbow run, expect a janky, loosely waving arm: shoulder-driven motion with the elbow trailing or moving in a way that was not explicitly commanded.

### Refined prediction

The elbow motor never drives in passive mode, so the observed flopping should be understood as the behavior of an unpowered joint rather than a motor that is too weak to overcome gravity.

### Next prediction

With joint 2 switched to `hold` while keeping elbow-down configuration and normal gravity, expect a more distinctive, intentional-looking motion—possibly not a wave, but more recognizable than the passive flopping.

### Gravity-off prediction

With gravity disabled, expect the staged coupled motion to look cleaner and more recognizable because the motors do not need to oppose the gravitational load.

### Purpose

Move beyond one-joint control intuition with the smallest experiment that can expose state-dependent multi-joint dynamics.

### Context supplied

- GitHub issue #2.
- The prior one-link pendulum experiment.
- Direct MuJoCo access to `qpos`, `qvel`, `ctrl`, and `qacc`.

## R — Response summary

A two-link vertical-plane MuJoCo arm was scaffolded. It drives only joint 1, lets joint 2 be passive or lightly held, and exposes pose and gravity as single-variable comparisons.

## E — Human evaluation

### Accepted

- In the passive, elbow-down run with normal Earth gravity enabled (`0 0 -9.81` m/s²), joint 2 visibly flopped around while joint 1 was commanded.
- The motion was not exactly the predicted janky wave, but it was qualitatively close enough to support the expectation of uncommanded elbow movement.
- With the same configuration and gravity but `joint2_mode=hold`, the motion looked more organized and wave-like than the passive run.
- The faster, in-plane rotated, control-coupled run produced an unmistakable wave; from the user's forward viewpoint, it appeared upside down.
- With gravity disabled, the staged coupled wave looked cleaner and more recognizable, matching the gravity-off prediction.

### Rejected

- “The elbow motor is too weak to overcome gravity” was rejected. In passive mode, the elbow motor receives `ctrl[1] = 0.0` and never drives.

### Unresolved

- Does joint 2 show behavior that the independent-pendulum mental model misses?
- Which observed differences depend on configuration, gravity, or motion?
- Does the observed motion resemble the predicted janky, loosely waving arm?
- Does changing joint 2 to `hold` materially change the elbow behavior now that the passive motor command is explicit?
- Does the held-elbow run produce the predicted more intentional-looking motion?
- Does the gravity-off run look cleaner and more recognizable than the normal-gravity run?

### Verification required

- Repeat the passive-elbow comparison from the `elbow-up` configuration.
- Repeat one case with gravity disabled and inspect the printed state samples.

## A — Action

Created the local experiment scaffold and documented an Iteration 0 prediction prompt plus minimal comparison runs. Added a `wave` mode that gives joint 2 its own phase-shifted sinusoidal target and PD tracking command, then added explicit control coupling so joint 2's target includes a tunable fraction of joint 1's desired motion.

Raised the shoulder base from `z=1.5 m` to `z=2.5 m` to keep the elbow-down arm above the floor while preserving the same control experiment.

Rotated the arm +90° within the plane orthogonal to the hinge axes (about Y), increased the wave frequency from `0.8` to `1.4` rad/s, and increased the wave tracking gains to make the coordinated motion faster.

Increased joint 2's wave amplitude from `0.55` to `0.70` rad and its tracking gains from `Kp=8, Kd=1` to `Kp=10, Kd=1.2` so its contribution is more visually distinct.

Widened joint 2's excursion to `1.20` rad with `Kp=14, Kd=1.5` so the intentionally non-human wave hyperextends in both directions.

Changed the coupled joint-2 target to sweep exactly from `-2` to `+2 rad` at the current coupling gain, compensating the base wave amplitude for the joint-1 cross-feed.

Replaced the always-on target with staged `ready → wave → return → hold` targets using smoothstep return interpolation, and added a small sphere at the link tip as a hand proxy.

Reverted the deliberately extreme joint-2 target range from `-2…+2 rad` to `-1.2…+1.2 rad` while preserving the staged motion and hand proxy.

## O — Outcome

Observed two runs with the same elbow-down configuration and normal Earth gravity: passive joint 2 flopped around, while held joint 2 produced more organized, wave-like motion. The faster, in-plane rotated, control-coupled run produced a recognizable wave, though its orientation was upside down from the user's forward viewpoint. The visual resemblance is now confirmed; the remaining mismatch is viewpoint/orientation.

### Effect on current belief

The prediction that shoulder-driven motion would produce uncommanded elbow motion is supported, and the held-elbow comparison changed the visible behavior. The gravity-off result strengthens the belief that removing gravitational load makes this simple controller track the intended qualitative wave more cleanly; orientation remains a presentation variable.

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
    status: open
  - id: R-20260809-001
    type: Response
    summary: Created a minimal two-link comparison scaffold with pose, gravity, and joint-2 control toggles.
    status: proposed
  - id: E-20260809-001
    type: Evaluation
    summary: Passive elbow flopped while joint 1 was driven; the gravity-off staged wave was cleaner and more recognizable, matching the prediction.
    status: confirmed
  - id: A-20260809-001
    type: Action
    summary: Added README, MuJoCo experiment script, local agent log, staged phase-shifted and coupled wave controller, raised base height, in-plane rotation, faster wave tracking, controlled `-1.2` to `+1.2 rad` joint-2 target, and a hand proxy for issue #2.
    status: completed
  - id: O-20260809-001
    type: Outcome
    summary: With normal Earth gravity enabled, passive joint 2 flopped while the held-joint-2 run looked more organized; with gravity off, the staged coupled run produced a cleaner, recognizable wave.
    status: observed
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
  - Does joint 2 move in a way that cannot be understood as an independent pendulum?
superseded_claims:
  - The initial motor-strength explanation was superseded by the code-level observation that passive joint 2 is unpowered.
```

Related: #2
