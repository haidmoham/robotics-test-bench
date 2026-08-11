# Static support: centered ballast

Question: does the bench's existing articulated tripod remain supported when a centered ballast is added over a fixed rollout?

## Human prediction

The ballast is fixed directly above the original body center. It adds weight without shifting the whole-body COM sideways. With no perturbation, the contact loads should remain roughly balanced, no contact should be lost, no tipping edge should dominate, and roll/pitch should remain near zero.

## Model and run

This is deliberately not C-1N. It duplicates the existing three-leg, two-joint tripod construction and its centered posture/support hold. The translucent blue reference is a separate, settled no-ballast model; the live treatment adds one fixed orange ballast directly above the chassis center. The report measures actual whole-body COM and ground projection, active contacts, normal loads, roll/pitch, angular velocity, and body height.

The hold is existing experimental infrastructure, not the variable under test. The only physical model change from the centered tripod hold is the ballast mass and its attachment point. #31 will separately ask whether the leg geometry can reach the required support points.

```bash
python static_support.py --duration 2
mview static_support.py --duration 120
```

The viewer defaults to real-time playback. The physical scene renders at 60
FPS; all telemetry channels retain a six-second trace sampled at 10 Hz and
refresh at 10 Hz. MuJoCo renders one three-panel telemetry page at a time so
the plots do not consume the scene's frame budget. Press `T` to switch between
support and motion telemetry; every channel continues sampling on either page.
Raise `--playback-speed` only for an intentionally faster visual pass. The
immutable model uses MuJoCo's faster state-only viewer sync; the ghost model,
force overlay, and custom figures remain viewer-side layers.

Move the treatment ballast in chassis-relative metres with `--ballast-x`,
`--ballast-y`, and `--ballast-z`. The blue no-ballast control remains fixed,
and the JSON output records the exact treatment position.

```bash
mview static_support.py --ballast-x 0.10 --duration 120
```

The viewer renders two overlapping models: the translucent blue, settled
no-ballast baseline and the live treatment. Red gravity and green support
arrows belong to the treatment; their scale adapts to its heavy ballast. The
shared telemetry stack shows per-foot loads, COM projection,
support margin, roll/pitch, angular velocity, and body height. The overlay is
an inspection aid; press `T` to page between those groups. The JSON report
remains the experiment evidence.

This first case is only the inside-support baseline. Edge, beyond-edge, and changed-support cases require new predictions.

## Perturbation mode

The baseline stays unchanged unless `--push-x` is non-zero. That option applies
a finite world-`+X` force at the chassis body for the requested interval, and
the orange overlay arrow shows when it is active. The JSON report records the
exact force, start, and duration so a pushed rollout is not confused with the
baseline.

```bash
python static_support.py --duration 2 --push-x 8 --push-start 0.5 --push-duration 0.1
mjpython static_support.py --viewer --duration 120 --push-x 8 --push-start 0.5 --push-duration 0.1
```

Choose and record a human prediction before interpreting the perturbed result.

Related: robotics-test-bench #24, Spider #11.
