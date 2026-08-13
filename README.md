# Robotics Test Bench

Small MuJoCo experiments for learning robotics from direct simulation evidence.

## Loop

1. State a physical, statistical, or numerical question.
2. Make a prediction.
3. Build the smallest useful test.
4. Run it and measure the result.
5. Update the model and choose the next question.

`TODO.md` selects the current experiment. `docs/research-platform.md` records the long-range simulation-platform direction. The design document never overrides the current queue.

For the C-1N robot, controller, and integrated locomotion checkpoints, start in [spider](https://github.com/haidmoham/spider). This repository owns the smaller experiments that test physical, numerical, statistical, or measurement questions before they become system changes.

## Structure

```text
TODO.md
docs/
  research-platform.md
experiments/
  telemetry.py
  viewer_runtime.py
  YYYY-MM-DD-short-question/
    README.md
    <experiment code>
    agent-log.md
integrations/
templates/
```

Each experiment owns its code and local evidence. Shared viewer telemetry lives in `experiments/telemetry.py`.

## Shared Python environment

Use the shared environment at `../.venv` for this repository, `spider`, and
`spider-web`. Its reproducible package list is `../requirements.txt`.

```powershell
..\.venv\Scripts\jupyter.exe lab
```

Select the `robotics shared (.venv)` kernel for notebooks.

## Working rules

- Use Python and MuJoCo by default.
- Build physical intuition before notation when the mechanism is the learning target.
- Change one meaningful variable at a time when causality matters.
- Begin a visual comparison with a labelled control and one deliberately legible treatment.
- Render the control as a ghost over the treatment when the comparison is spatial.
- Treat overlays as inspection aids, not as evidence.
- Define objectives and evaluation conditions explicitly.
- Compare fixed scenarios, seeds, or parameter draws when the question is statistical.
- Preserve useful failures.
- Add infrastructure only when a real experiment needs it.
- Stop polishing when the experiment has answered its question.
