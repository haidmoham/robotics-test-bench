# Agent instructions

This repository is a disposable robotics learning test bench. Optimize for fast simulation experiments that build physical intuition and then compound into statistical modeling, robot learning, evaluation, and simulation systems work.

- Read the root `README.md` and `TODO.md`, then the current experiment README and code before changing anything.
- `TODO.md` is the authoritative selector for the next experiment. Treat its single `NEXT` item as current even when older experiments or closed issues suggest another route.
- New experiments belong in `experiments/YYYY-MM-DD-short-question/` and should keep their code, README, and meaningful agent log local to that directory.
- Root docs contain only repo-wide conventions. Keep experiment-specific findings inside the experiment.
- Prefer the smallest change that answers the current question. Keep experiments easy to inspect, revert, and compare.
- Start comparison-oriented experiments visually: construct a control and one deliberately legible contrast treatment, render their states together with the control as a translucent ghost, and launch that viewer before asking for interpretation. Keep the treatment explicitly labelled and do not mistake the overlay for evidence.
- Use the shared rolling telemetry stack (`experiments/telemetry.py`) in viewer experiments when its signals make the changed variable or its physical consequence inspectable. Capture timestamped samples independently of display availability, and represent unavailable measurements explicitly instead of freezing every channel. Keep MuJoCo analytical overlays to one three-panel page at a time with `TelemetryPager`; attached `MjvFigure`s are rendered every video frame even when their data is refreshed less often. Match plot publication to the telemetry sample rate (10 Hz is the default starting point). Launch custom experiment views with `launch_experiment_viewer` and preserve MuJoCo's informative built-in side UI; custom telemetry supplements those controls and diagnostics. For continuous physics viewers, use `WallClockPlayback` from `experiments/viewer_runtime.py`: batch fixed-timestep physics to its wall-clock simulation target, update overlays and sync once, then wait for its 60 Hz frame deadline. Use `viewer.sync(state_only=True)` when the model is immutable after launch; reserve full sync for runtime model edits. Gate expensive plot rebuilding separately with `WallClockRateGate`. Do not pace by sleeping inside every physics step or busy-sync the viewer.
- Do not assume formal physics coursework. Build new physical mechanisms from a concrete force picture before notation. Name forces and contacts. State the motion or rotation each force tends to cause. State what resists or constrains that motion. Show how geometry or leverage changes the effect. Introduce the equation last.
- Treat physics and controls as enabling literacy for simulation. Do not route the user toward controls specialization or low-level hardware work by default.
- C++ is in scope when it improves robotics employability, simulator performance, autonomy software, numerical code, or integration with robotics libraries. Do not treat C++ as evidence that the user should become an embedded or firmware engineer.
- ROS 2 is in scope when a simulator, autonomy stack, or target robotics role needs it. Do not make ROS 2, device drivers, microcontrollers, board-level electronics, firmware, or motor electronics the learning destination.
- Hardware is not a graduation requirement. Physical-system knowledge matters because simulator assumptions need interpretation and eventual external validation, not because the learning path must terminate in hardware.
- Prefer work that exploits the user's statistics background: inference, uncertainty, experiment design, evaluation, stochastic modeling, system identification, calibration, optimization, and learned behavior.
- Preserve Iteration 0: ask for or respect the human prediction before revealing a non-trivial mechanism or diagnosis when learning is the target.
- Automate setup, API lookup, boilerplate, repetitive edits, plotting, batch execution, and experiment plumbing aggressively.
- Do not outsource the learning target. Leave hypotheses, physical interpretation, objective design, architecture tradeoffs, and diagnosis with the human unless explicitly asked to solve them.
- Before giving a conceptual explanation for a surprising result, let the human state a first diagnosis and, when practical, one observation that could falsify it.
- Use chat or stronger reasoning to challenge, falsify, or verify a stated human model. Do not use stronger reasoning as the default first-pass diagnosis when the mechanism itself is the learning target.
- Prefer delaying conceptual help over deliberately using an unreliable model. Preserve reasoning friction, not information-quality friction.
- Periodically test transfer with a cold rep: explain, predict, or implement a familiar mechanism without conceptual AI help. Routine syntax, API, boilerplate, and experiment plumbing can remain automated.
- Change one physical, statistical, numerical, or objective variable at a time when causality matters.
- When behavior is surprising, consider objective design, state representation, model parameters, contacts, actuators, estimator assumptions, stochastic variation, policy optimization, and numerical integration before assuming one cause.
- Verify important claims with the cheapest reliable check: inspect MuJoCo state, run the experiment, print a focused value, compare held-out rollouts, or use a minimal numerical check.
- Do not add tests, abstractions, infrastructure, or dependencies by default. Add simulation infrastructure when a real experiment needs reproducibility, throughput, or structured evaluation.
- Record an `agent-log.md` entry only when an interaction changes a prediction, experiment, interpretation, decision, code direction, or next meaningful action. Do not log routine syntax/API help.
- Meaningful agent-log entries use the stable `Q/R/E/A/O` ontology from `templates/agent-interaction.md`: Question -> Response -> Evaluation -> Action -> Outcome. Preserve IDs across updates and record explicit relations and Librarian status.
- When parallel work lands, preserve existing stable `AI/Q/R/E/A/O` entries by ID. Integrate or rebase around them; do not regenerate, renumber, or silently replace a conversation-derived entry because another branch changed the same log.
- Before landing a commit that changes evidence state, queue state, stable IDs, provenance, experiment closure, or C-1N integration claims, use the installed `commit-boundary` skill with `.ontology/commit-rules.md`.
- New agent-log entries must identify their source provenance. Keep coding-agent, chat, human-observation, and external-reference sources distinct; do not merge claims from different sources without attribution.
- For conversation-derived entries, preserve the epistemic change as an explicit before -> after belief update and keep verification status separate from source provenance.
- Use `templates/agent-interaction.md` as the canonical log shape. Do not store full chat transcripts.
- Commit at meaningful experimental boundaries: completed experiments, informative failures, ontology changes, and before broad refactors. Commit messages should state the hypothesis or decision and the observed result when known.
- Use GitHub Issues for the active simulation frontier, not as a permanent encyclopedia of robotics prerequisites.
- Closed legacy issues are historical provenance. Do not reopen or recreate their old curriculum unless a current failure explicitly makes that mechanism the next useful experiment.
- Treat a GitHub issue number as stable concept identity, not experiment chronology. Do not renumber or backfill issues when evidence resolves out of issue order.
- Treat the dated experiment directory and the commit that records its resolved boundary as the chronology source.
- Keep communication concise. Distinguish observed behavior from inference when it matters.

## Current conventions

- Python + MuJoCo are the current default tools. Introduce C++ when a concrete simulator, performance, interoperability, or target-role need justifies it.
- Prefer direct MuJoCo concepts (`mjModel`, `mjData`, `qpos`, `qvel`, `ctrl`, contacts, timestep) while physical intuition is still the learning target.
- Default experiment loop: predict -> change -> run -> explain -> challenge -> record next question.
- Preserve the immediate foundation: learn static support well enough to establish `C-1N // 02 · STAND` from reproducible rollout evidence.
- After `STAND`, move directly into learned locomotion. Let policy and simulator failures pull in the next mechanism.
- Prefer future work that compounds the user's software and statistics background: policy optimization, rollout evaluation, system identification, simulator calibration, uncertainty, distribution shift, differentiable dynamics, numerical fidelity, and scalable simulation infrastructure.
- Treat a successful-looking rollout as a sample, not a conclusion. Compare behavior across fixed scenarios, seeds, and parameter draws when the question is statistical.
- Separate training objectives from evaluation metrics. Preserve objective components when learned behavior is the question.
- Validate fitted simulator parameters and learned conclusions on behavior not used for fitting or selection.
- Pull deeper controls, contact, actuator, estimation, or numerical concepts back in only when a current simulation failure makes them causally relevant.
- Do not polish an experiment after its learning value is exhausted; move to the next question.
