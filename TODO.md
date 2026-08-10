# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item should be marked `NEXT`.
- The `NEXT` item overrides older route suggestions in `README.md` when they conflict.
- GitHub issue numbers remain stable concept identities, not chronology.
- Re-evaluate the queue when an experiment closes or produces stronger evidence.
- Do not create the next experiment directory until its Iteration 0 prediction exists.

## NEXT

### #6 Jacobians & task space — make joint commands physical

**Status:** NEXT

C-1N exposed the motivating failure: synchronized joint-space commands do not imply synchronized foot motion in a shared torso/world frame.

Run the isolated bench experiment defined in issue #6. The learning target is the mapping:

`joint command -> joint motion -> forward kinematics -> shared-frame end-effector motion`

The experiment must compare joint-space position/velocity/acceleration with task-space end-effector X position/velocity/acceleration and verify at least one Jacobian column by finite difference or geometry.

Before code, predict the sign and rough relative size of shared-frame end-effector X motion produced by the same small positive first-joint perturbation at three different base orientations.

After the bench experiment closes, use its C-1N hook to add torso-frame foot task-space telemetry to the canonical robot. If that integration preserves the understood failure, it becomes the `C-1N // 02 · FRAME` checkpoint. Do not fix the C-1N gait as part of the bench experiment.

## Deferred route

The prior differentiable-dynamics route remains available after #6:

`#5 trajectory tracking -> #12 system identification -> #16 differentiable dynamics -> #13 numerical sensitivity`

It is not the current next experiment.