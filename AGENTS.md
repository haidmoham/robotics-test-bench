# Agent instructions

<!-- shared-practice:start -->
<!-- Source: robotics-test-bench/guidance/practice.md. Refresh with scripts/sync_practice_contract.py from that repository. -->
## Shared practice rule

- Before advancing a meaningful learning step, get one real attempt from the user: code, a prediction, an explanation, a diagnosis, or a proposed design with a reason. A conversational attempt counts. Reuse a relevant attempt already supplied; do not restart this check every turn. Acknowledgment alone does not count.
- Keep this boundary in the conversation. If no attempt exists, pause the learning step and help the user make one. Do not supply the attempt yourself or move ahead to its solution, run, or interpretation.
- Do not require an "Iteration 0" label, a written form, a prediction variable, or a code switch to enforce participation. Do not turn each explanation into a quiz. Answer direct conceptual questions and offer hints that help the user attempt the work.
- Review the attempt with the user. Let that feedback guide the next change. Do not count agent output, setup checks, or notebook execution as demonstrated user capability.
- At interpretation time, launch the simulator so the user can visually inspect the relevant treatment before explaining its result. Show the treatment label and changed parameters. Replay the measured run when available; otherwise reproduce its setup and identify the view as a rerun. Include the control when comparing treatments. Keep measurements alongside the view and leave the causal interpretation with the user. This is standing permission to launch the relevant view at that stage; it does not authorize a new learning experiment or an earlier solution.
- Automate peripheral setup, cleanup, and verification. Preparing a notebook does not authorize executing its learning experiment. Notebook cells can run normally when the user chooses to run them; the agent must preserve the conversational boundary before running them on the user's behalf.
- Honor an explicit request for a full solution for that part only. Keep the remaining learning work with the user.
<!-- shared-practice:end -->

## Purpose

This repository is my laboratory for implementing, modifying, and understanding robotics simulations. I am the primary implementer; preserve that authorship.

## Agent role

- Do not implement models, policies, training code, experiments, or tests unless I explicitly ask.
- Agents may maintain project plumbing: environment configuration, dependency metadata, formatting/linting/test tooling, and developer documentation.
- Prefer explaining concepts, answering questions, reviewing my code, and identifying issues.
- When reviewing, describe the problem and possible approaches before changing code.
- Keep unsolicited setup and abstraction to a minimum.
- Do not choose a framework, dependency, architecture, or project convention for me.

## Read order and ownership

- Read `README.md` and `TODO.md` first.
- Read the current experiment README and code before you edit anything.
- Treat the single `NEXT` item in `TODO.md` as the current experiment.
- Treat `docs/research-platform.md` as long-range design only. It never overrides `TODO.md`.
- Keep root documents limited to repository-wide rules.
- Keep experiment-specific findings in the experiment directory.
- Put new experiments in `experiments/YYYY-MM-DD-short-question/`.

## Experiment execution

- Build the smallest test that answers the current question.
- Follow the shared practice rule for the user's first attempt. Keep the learning boundary conversational.
- Do not outsource the hypothesis, causal interpretation, objective design, architecture tradeoff, or diagnosis unless the human asks for the answer.
- Prioritize the human's learning over completing the solution. Prepare the notebook, telemetry, or calculation fixture. Let the human inspect it before you interpret a learning-target result.
- Separate analysis setup from analysis execution. Do not run or interpret a learning-target calculation without explicit permission.
- Do not use goals, issue state, or the experiment queue to pressure the human or substitute delivery speed for understanding.
- Change one physical, statistical, numerical, or objective variable at a time when causality matters.
- Distinguish observed behavior from inference.
- Verify important claims with the cheapest reliable check.
- Preserve useful failures and negative cases.
- Do not add tests, abstractions, dependencies, or infrastructure by default.
- Add infrastructure only when a real experiment needs reproducibility, throughput, or structured evaluation.
- Stop polishing when the experiment has answered its question.

## Viewer and telemetry

- Start comparison experiments with one control and one deliberately legible treatment.
- Label the treatment.
- Render the control as a translucent ghost over the treatment when the comparison is spatial.
- Treat the overlay as an inspection aid, not as evidence.
- Use `experiments/telemetry.py` when telemetry makes the changed variable or its physical consequence inspectable.
- Capture timestamped samples independently of display availability.
- Represent unavailable measurements explicitly. Do not freeze every channel.
- Use one three-panel MuJoCo plot page at a time with `TelemetryPager`.
- Match plot publication to the telemetry sample rate. Use 10 Hz as the initial rate unless the experiment requires another rate.
- Launch custom experiment views with `launch_experiment_viewer`.
- Preserve MuJoCo's built-in side UI.
- Use `WallClockPlayback` from `experiments/viewer_runtime.py` for continuous physics viewers.
- Batch fixed-timestep physics to the wall-clock target. Update overlays and synchronize once per frame. Then wait for the 60 Hz frame deadline.
- Use `viewer.sync(state_only=True)` when the model is immutable after launch.
- Use full synchronization only for runtime model edits.
- Gate expensive plot rebuilding separately with `WallClockRateGate`.
- Do not sleep inside every physics step.
- Do not busy-synchronize the viewer.

## Evidence integrity

- Keep hypotheses, interventions, controls, and measurements distinct.
- Keep training objectives separate from evaluation metrics.
- Treat a successful rollout as one sample, not as a conclusion.
- Compare fixed scenarios, seeds, and parameter draws when the question is statistical.
- Record code, simulator, seed, distribution, policy, and metric provenance when they affect the result.
- Retain invalid cases and failed rollouts.
- Create a new record when a metric or protocol changes after results are visible.
- Do not change hidden parameters to rescue a failed result.
- Validate fitted parameters and learned conclusions on behavior that was not used for fitting or selection.

## Agent logs and commits

- Add an `agent-log.md` entry only when an interaction changes a prediction, experiment, interpretation, decision, code direction, or next meaningful action.
- Do not log routine syntax or API help.
- Use the `Q/R/E/A/O` shape from `templates/agent-interaction.md`.
- Preserve stable IDs across updates and parallel work.
- Do not regenerate, renumber, or silently replace an existing entry.
- Identify the source provenance for every new entry.
- Keep coding-agent, chat, human-observation, and external-reference sources distinct.
- Preserve an explicit before-to-after belief update for conversation-derived entries.
- Keep verification status separate from provenance.
- Use the installed `commit-boundary` skill with `.ontology/commit-rules.md` before a commit changes evidence state, queue state, stable IDs, provenance, experiment closure, or C-1N integration claims.
- Commit at meaningful experiment boundaries, informative failures, ontology changes, and before broad refactors.
- State the hypothesis or decision and the observed result in the commit message when the result is known.

## Issues and chronology

- Use GitHub Issues for the active simulation frontier.
- Do not use issues as a permanent encyclopedia of prerequisites.
- Treat closed legacy issues as historical provenance.
- Do not reopen or recreate a legacy curriculum unless a current failure makes it necessary.
- Treat an issue number as stable concept identity, not chronology.
- Use the dated experiment directory and its resolving commit as the chronology source.

## Current route

- Use Python and MuJoCo by default.
- Prefer direct MuJoCo concepts while the mechanism is the learning target.
- #24 static support and #31 leg workspace are resolved bench evidence.
- Preserve C-1N's recorded STAND baseline and its limits. Bench evidence does not certify the human's present understanding.
- Follow `#25` into user-written RL/PPO. Use the C-1N notebook guide for the initial control-step ramp-up.
- Let later policy and simulator failures select the next mechanism.
- Keep the platform direction in `docs/research-platform.md` inactive until a concrete scale, reproducibility, validation, or analysis need appears.

## Current notebook learning contract

- Use `$practice` for the walking-policy work. The human owns the learning decisions and algorithm implementation. Use production for peripheral setup, cleanup, and verification. Preparation does not authorize training or completing an unanswered exercise.
- The 2026-09-04 user instruction supersedes issue #25's earlier instruction to use an existing RL implementation. The human writes RL and PPO with PyTorch operations, autograd, and optimizers.
- Use Jupyter first for predictions, bounded experiments, plots, and interpretation. Keep reusable simulation behavior in Python modules.
- Do not add prediction forms or code gates to new learning notebooks. Run All may execute experiments; validate structure and syntax during preparation instead.
- Do not supply completed rollout, return, advantage, policy-loss, value-loss, or update code unless the human explicitly asks for that solution.
- Preserve the existing Ant-v5 scaffold and its stable records as prior work. Do not infer a new prediction or understanding from those records.
