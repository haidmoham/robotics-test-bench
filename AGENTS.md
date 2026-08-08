# Agent instructions

This repository is a small robotics learning test bench. Optimize for fast experiments that build physical intuition, not framework complexity.

- Read `README.md` and the current experiment before changing anything.
- Prefer the smallest change that answers the current question. Keep experiments easy to inspect, revert, and compare.
- Preserve the learning loop: ask for or respect an Iteration 0 prediction before revealing a non-trivial mechanism or diagnosis when the user is learning from the result.
- Automate setup, API lookup, boilerplate, repetitive edits, plotting, and other implementation friction aggressively.
- Do not outsource the learning target. Leave hypotheses, physical interpretation, architecture tradeoffs, and diagnosis with the user unless explicitly asked to solve them.
- Change one physical or numerical variable at a time when possible. Avoid bundled perturbations that make causality unclear.
- When behavior is surprising, consider model parameters, contacts, actuators, controller logic, and numerical integration before assuming one cause.
- Verify important claims with the cheapest reliable check: inspect the MuJoCo model/data, run the experiment, print a focused state value, or use a minimal test.
- Do not add tests, abstractions, infrastructure, or dependencies by default. Add them only when they protect meaningful behavior or remove repeated friction.
- Keep repo-specific findings here in concise comments, docs, or issues. Do not turn this repo into a general robotics knowledge base.
- Use GitHub Issues only for durable follow-up work. Do not create process for trivial experiments.
- Keep communication concise. Distinguish observed behavior from inference when it matters.

## Current conventions

- Python + MuJoCo.
- `pendulum.py` is the current minimal experiment.
- Prefer direct MuJoCo concepts (`mjModel`, `mjData`, `qpos`, `qvel`, `ctrl`, contacts, timestep) over hiding them behind higher-level frameworks while learning.
- For perturbation sessions, default loop: predict -> change one thing -> run -> explain -> revert or record.
