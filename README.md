# Robotics Test Bench

Small MuJoCo experiments for learning robotics from direct simulation evidence.

MuJoCo measures embodied behavior; Jupyter interrogates saved results; reusable
Python implements; reproducible experiments establish claims.

## Loop

1. State a physical, statistical, or numerical question.
2. Make a prediction.
3. Build the smallest useful test.
4. Run it and measure the result.
5. Update the model and choose the next question.

`TODO.md` selects the current experiment.

## Structure

```text
TODO.md
experiments/
  artifacts.py
  telemetry.py
  viewer_runtime.py
  YYYY-MM-DD-short-question/
    README.md
    <experiment code>
    agent-log.md
integrations/
notebooks/
results/  # ignored run artifacts; keep only .gitkeep in Git
templates/
```

Each experiment owns its code and local evidence. Shared viewer telemetry lives in `experiments/telemetry.py`.

## Scientific front end

Choose the cheapest valid surface for each question:

- Use a notebook-native model for derivations, numerical checks, plots, and small parameter sweeps that do not need embodiment.
- Use headless MuJoCo when contact, dynamics, control, or simulator behavior matters; save its structured telemetry in `results/`, then analyze it in a notebook.
- Move behavior that becomes reusable out of a notebook and into normal Python source. A notebook may discover or explain, but it does not establish the authoritative state of the robot.

See [`notebooks/README.md`](notebooks/README.md) for the artifact contract and a runnable first analysis.

## Working rules

- Use Python + MuJoCo by default.
- Build physical intuition before notation when the mechanism is the learning target.
- Change one meaningful variable at a time when causality matters.
- For a visual comparison, begin with a labelled control and a deliberately legible treatment. Render the control as a ghost over the live treatment, show shared telemetry, and inspect the viewer before interpreting the rollout.
- Define objectives and evaluation conditions explicitly.
- Compare behavior across fixed scenarios, seeds, or parameter draws when the question is statistical.
- Preserve useful failures.
- Treat telemetry artifacts as first-class inputs: simulate once, interrogate the result many times.
- Add infrastructure only when a real experiment needs it.
- Stop polishing when the experiment has answered its question.
