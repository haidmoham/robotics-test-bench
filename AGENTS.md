# Agent instructions

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
- Preserve Iteration 0. Get or respect the human prediction before you reveal a non-trivial mechanism or diagnosis.
- Do not outsource the hypothesis, causal interpretation, objective design, architecture tradeoff, or diagnosis unless the human asks for the answer.
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
- Run `#24` static support.
- Then run `#31` leg workspace.
- Then integrate the results through `haidmoham/spider#11` and earn `C-1N // 02 · STAND` with reproducible evidence.
- After `STAND`, move to `#25` learned locomotion.
- Let later policy and simulator failures select the next mechanism.
- Keep the platform direction in `docs/research-platform.md` inactive until a concrete scale, reproducibility, validation, or analysis need appears.
