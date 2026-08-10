# Experiment queue

This file is the authoritative selector for the next robotics test-bench experiment.

- Exactly one item should be marked `NEXT`.
- The `NEXT` item overrides older route suggestions in `README.md` when they conflict.
- GitHub issue numbers remain stable concept identities, not chronology.
- Re-evaluate the queue when an experiment closes or produces stronger evidence.
- Do not create the next experiment directory until its Iteration 0 prediction exists.

## NEXT

### #20 Static support & equilibrium — make standing physical

**Status:** NEXT

#6 established the task-space model needed to stop treating a standing-looking pose as only a joint-position problem.

The gap intentionally left in #6 today is still explicit: one combined planar 2-DOF mechanism across 0, 90, and 180 degrees, comparing local/base and shared-frame static foot displacement. Preserve that as unfinished #6 coverage. Do not implement it now unless later evidence makes it useful, and do not let it block the learning frontier.

The next learning target is:

`contact geometry + center-of-mass projection -> support load -> net body force/moment -> body attitude`

Run the isolated bench experiment defined in issue #20. Keep C-1N out of the bench implementation.

Before code, use one fixed triangular foot layout and predict the three cases from issue #20:

1. center-of-mass projection clearly inside the support triangle;
2. center-of-mass projection close to one edge;
3. center-of-mass projection beyond that edge.

For each case, predict whether the body holds attitude or tips, which supports carry more or less normal load, and the initial roll or pitch direction if equilibrium is lost.

After #20 closes, return to C-1N for a stance-only integration with the gait clock and swing phase disabled. Expose active support geometry, center-of-mass projection, foot contact/load evidence, and torso roll/pitch. If that integration demonstrates understood support-aware stable equilibrium, preserve it as `C-1N // 02 · STAND`.

Do not improve the walking gait as part of #20 or the standing checkpoint.

## Deferred route

The differentiable-dynamics route remains available:

`#5 trajectory tracking -> #12 system identification -> #16 differentiable dynamics -> #13 numerical sensitivity`

It is not the current next experiment.
