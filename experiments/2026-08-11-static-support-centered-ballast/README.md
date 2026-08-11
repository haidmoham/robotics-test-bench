# Static support: centered ballast

Question: does the bench's existing articulated tripod remain supported when a centered ballast is added over a fixed rollout?

## Human prediction

The default treatment ballast is purposefully forward-offset at the recorded
chassis-relative position. With no perturbation, the contact loads should
remain roughly balanced, no contact should be lost, no tipping edge should
dominate, and roll/pitch should remain near zero.

## Model and run

This is deliberately not C-1N. It duplicates the existing three-leg, two-joint tripod construction and its centered posture/support hold. The translucent blue reference is a separate, settled no-ballast model; the live treatment adds a fixed 1 kg orange ballast. The report measures actual whole-body COM and ground projection, active contacts, normal loads, roll/pitch, angular velocity, and body height.

The hold is existing experimental infrastructure, not the variable under test. The only physical model change from the centered tripod hold is the ballast mass and its attachment point. #31 will separately ask whether the leg geometry can reach the required support points.

```bash
python static_support.py --duration 2
mview static_support.py --duration 120
```

The treatment defaults to 1 kg. Its position is chassis-relative, and its
default \(z=0.14\) m puts the ballast on the chassis top; it is not a world
height. Keep that recorded position fixed when comparing mass alone; reproduce
the 10 kg case headlessly
with:

```bash
python static_support.py --duration 2 --ballast-mass 10
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
arrows belong to the treatment; their scale adapts to its ballast mass. The
shared telemetry stack shows per-foot loads, COM projection,
support margin, roll/pitch, angular velocity, and body height. The overlay is
an inspection aid; press `T` to page between those groups. The JSON report
remains the experiment evidence.

This first case is only the inside-support baseline. Edge, beyond-edge, and changed-support cases require new predictions.

## Five-placement live comparison

For a legible first comparison, inspect five representative positions from the
\(x,y \in \{-0.2,-0.1,0,0.1,0.2\}\) m grid in separate live windows: center,
forward, rearward, left, and right. Keep the 1 kg mass fixed and use the
placement arguments to change only the ballast location. These views are
inspection aids, not evidence artifacts. Use the default chassis-top `z=0.14`
m unless height itself is the variable under test.

## Portfolio note

Keep the human learning beat for a later blog post: stability is not about the
robot's visible footprint or the ballast alone. It is the mass-weighted,
combined center-of-mass projection relative to the feet's support region. The
threshold becomes legible when that projection reaches a support boundary;
whether it passes beyond it remains an experimental claim to check against
the recorded contact geometry.

Also preserve the learning detour: turning that picture into a reliable model
requires mechanics practice on static equilibrium, unilateral contact forces,
moments about a pivot edge, and rigid-body angular-velocity vectors. The
experiment exposed the distinction between an orientation quaternion and an
angular rate, and between a fall plane and its perpendicular rotation axis.

Use Daniel Kleppner and Robert Kolenkow, *An Introduction to Mechanics*, 2nd
edition (Cambridge University Press), as the source of the associated practice
problems. Bind this experiment to that study sequence: return to its support
geometry, contact-force, moment, and rigid-body-kinematics questions after
each relevant problem set, rather than treating the simulation as a substitute
for the mechanics.

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

## Stopping boundary

This experiment stops here. It made the static-support question concrete and
revealed a physical-intuition gap around contact geometry, moments, and
rigid-body rotation; it does not establish an attached-ballast stability
conclusion. The earlier mass sweep used a suspended-ballast configuration and
is preserved only as a model-configuration failure, not as attached-ballast
evidence.

Before continuing this lane, repair that intuition with the documented
mechanics problems, then return with a fresh prediction and a deliberately
specified attached-ballast treatment. This stop is part of the prospective
blog story: the useful result is recognizing when further simulation would
outpace the physical model being learned.
