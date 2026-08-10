# Robotics Test Bench

Small MuJoCo experiments for learning robotics from direct simulation evidence.

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
  telemetry.py
  YYYY-MM-DD-short-question/
    README.md
    <experiment code>
    agent-log.md
integrations/
templates/
```

Each experiment owns its code and local evidence. Shared viewer telemetry lives in `experiments/telemetry.py`.

## Working rules

- Use Python + MuJoCo by default.
- Build physical intuition before notation when the mechanism is the learning target.
- Change one meaningful variable at a time when causality matters.
- Define objectives and evaluation conditions explicitly.
- Compare behavior across fixed scenarios, seeds, or parameter draws when the question is statistical.
- Preserve useful failures.
- Add infrastructure only when a real experiment needs it.
- Stop polishing when the experiment has answered its question.
