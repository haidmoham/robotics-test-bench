# Jacobians and task space

Question: How does the same first-joint motion map into shared-frame foot X motion when only the base orientation changes?

## Iteration 0

Holding geometry, joint pose, perturbation size, controller, and timestep fixed, the same small positive first-joint perturbation should produce a large shared-X foot displacement at 0 degrees, near-zero X displacement at 90 degrees, and an equally large displacement with the opposite X sign at 180 degrees. The foot should not stop moving at 90 degrees; its motion should be along shared Z instead. At intermediate orientations, the shared-X magnitude should scale with the cosine of the base orientation: 45 and 135 degrees should have about 71% of the 0-degree magnitude, with opposite signs.

## Smallest useful experiment

`jacobians_task_space.py` is a one-link leg in the X-Z plane. It holds the model, initial joint pose, PD controller, and timestep fixed while changing only the base pitch.

Before the motion starts, the script prints two estimates of the first Jacobian column's X entry:

- MuJoCo's position Jacobian, `Jx`;
- a centered finite difference of foot X position with respect to joint 1.

During the run, it reports joint position, velocity, and acceleration beside shared-frame foot X position, X velocity, and X acceleration. X velocity is `Jx * qvel`; X acceleration is the measured change in that velocity, so it includes the changing Jacobian as the leg moves.

Run a single base orientation at a time:

```bash
python jacobians_task_space.py --base-degrees 0
python jacobians_task_space.py --base-degrees 90
python jacobians_task_space.py --base-degrees 180
```

To watch those three physical runs together, use the overlay viewer borrowed from the Experiment 3 comparison pattern:

```bash
mjpython jacobians_task_space.py --overlay
```

Blue is 0 degrees, orange is 90 degrees, and green is 180 degrees. Each color is an independently stepped, zero-gravity simulation, so the controller produces the same realized joint motion in every color and the visual difference isolates the frame transformation. The overlay affects rendering only. The single-orientation runs above retain normal gravity.

The overlay camera faces the X-Z motion plane directly: screen-left/right is shared X and screen-up/down is shared Z. Read the three base angles in that visible plane, not from a perspective camera.

The colored links are not three legs on one robot. They are three independent copies of the same one-link model, drawn around one shared hinge for comparison. Foot labels identify each base orientation; black markers label the shared hinge, +X, and +Z.

The left graph stack compares the shared joint position, velocity, and acceleration against the sinusoidal target. Because the zero-gravity runs have identical joint dynamics, one actual trace represents all three base orientations without hiding it under duplicate lines. The right stack compares foot X displacement from each foot's starting position, X velocity, and X acceleration. Fixed vertical ranges make sign, magnitude, and phase comparisons stable instead of rescaling each frame. Stack width, height, margins, and gaps respond to the current viewer viewport, so resizing preserves plotting area without overlapping the two stacks. Both stacks use the test bench's canonical viewer helper in [`experiments/telemetry.py`](../telemetry.py), adapted from C-1N.

For a quick non-visual comparison:

```bash
python jacobians_task_space.py --base-degrees 45 --headless --duration 2
```

## What to record

- Do the Jacobian and finite-difference estimates agree in sign and rough magnitude?
- Does the 90-degree run still show joint and foot motion while shared X motion is near zero at the initial pose?
- Does reversing the base to 180 degrees reverse the initial X Jacobian sign without changing the joint perturbation?

Keep controller, geometry, joint start, and timestep unchanged while comparing orientations. Do not add inverse kinematics or a task-space controller yet.

Related: #6
