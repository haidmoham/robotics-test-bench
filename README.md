# Robotics Test Bench

A disposable laboratory for building robotics intuition through small simulation experiments.

The goal is to shorten the distance between a physical question and an observation. This is not a polished robotics project.

## Core loop

1. State a question.
2. Make an Iteration 0 prediction.
3. Build the smallest useful test.
4. Run it.
5. Observe the result.
6. Update the mental model.
7. Record the next question.

Agents should remove setup, API, boilerplate, and repetitive implementation friction. The human should own prediction, physical interpretation, and diagnosis when those are the learning target.

## Structure

```text
experiments/
  YYYY-MM-DD-short-question/
    README.md
    <experiment code>
    agent-log.md

templates/
  agent-interaction.md
```

Each experiment owns its code and local evidence. Root docs contain only repo-wide conventions.

## Current experiment

[`experiments/2026-08-08-pendulum-control`](experiments/2026-08-08-pendulum-control)

MuJoCo mental model:
- `mjModel` = what the simulated system is.
- `mjData` = what the system is doing now.
- `worldbody` = fixed global frame.
- bodies form a tree; contacts and constraints add relationships beyond that tree.
- `qpos` = generalized configuration.
- `qvel` = generalized velocity.
- `ctrl` = actuator command, not necessarily joint torque.
- `mj_step()` advances kinematics, contact/constraints, forces, acceleration, and integration.

## Rules

- Run something quickly.
- Change one meaningful variable at a time when causality matters.
- Predict before executing.
- Optimize for understanding, not elegance.
- Ugly experiment code is acceptable.
- Refactor only when it removes repeated friction or enables the next question.
- Do not turn this repo into a general robotics encyclopedia.

## Success metrics

Measure questions tested, predictions made, surprising failures, observations, and updated beliefs. Do not optimize for lines of code or production polish.
