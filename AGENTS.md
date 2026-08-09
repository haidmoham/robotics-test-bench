# Agent instructions

This repository is a disposable robotics learning test bench. Optimize for fast experiments that build physical intuition, not framework complexity.

- Read the root `README.md`, then the current experiment README and code before changing anything.
- New experiments belong in `experiments/YYYY-MM-DD-short-question/` and should keep their code, README, and meaningful agent log local to that directory.
- Root docs contain only repo-wide conventions. Keep experiment-specific findings inside the experiment.
- Prefer the smallest change that answers the current question. Keep experiments easy to inspect, revert, and compare.
- Preserve Iteration 0: ask for or respect the human prediction before revealing a non-trivial mechanism or diagnosis when learning is the target.
- Automate setup, API lookup, boilerplate, repetitive edits, plotting, and other implementation friction aggressively.
- Do not outsource the learning target. Leave hypotheses, physical interpretation, architecture tradeoffs, and diagnosis with the human unless explicitly asked to solve them.
- Change one physical or numerical variable at a time when causality matters.
- When behavior is surprising, consider model parameters, contacts, actuators, controller logic, and numerical integration before assuming one cause.
- Verify important claims with the cheapest reliable check: inspect MuJoCo state, run the experiment, print a focused value, or use a minimal test.
- Do not add tests, abstractions, infrastructure, or dependencies by default.
- Record an `agent-log.md` entry only when an interaction changes a prediction, experiment, interpretation, decision, code direction, or next meaningful action. Do not log routine syntax/API help.
- Meaningful agent-log entries use the stable `Q/R/E/A/O` ontology from `templates/agent-interaction.md`: Question -> Response -> Evaluation -> Action -> Outcome. Preserve IDs across updates and record explicit relations and Librarian status.
- New agent-log entries must identify their source provenance. Keep coding-agent, chat, human-observation, and external-reference sources distinct; do not merge claims from different sources without attribution.
- For conversation-derived entries, preserve the epistemic change as an explicit before -> after belief update and keep verification status separate from source provenance.
- Use `templates/agent-interaction.md` as the canonical log shape. Do not store full chat transcripts.
- Commit at meaningful experimental boundaries: completed experiments, informative failures, ontology changes, and before broad refactors. Commit messages should state the hypothesis or change and the observed result when known. Do not batch unrelated learning into one commit.
- Use GitHub Issues for durable follow-up work, not trivial experiment steps.
- Keep communication concise. Distinguish observed behavior from inference when it matters.

## Current conventions

- Python + MuJoCo.
- Prefer direct MuJoCo concepts (`mjModel`, `mjData`, `qpos`, `qvel`, `ctrl`, contacts, timestep) while learning.
- Default experiment loop: predict -> change -> run -> explain -> record next question.
- Do not polish an experiment after its learning value is exhausted; move to the next mechanism.
