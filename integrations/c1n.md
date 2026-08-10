# C-1N integration target

Target repository: `haidmoham/spider` (legacy repository slug; public robot identity: **C-1N**)

C-1N is the longitudinal integration robot. It consumes robotics concepts after the test bench makes them concrete.

## Identity and checkpoint grammar

Public checkpoints use:

```text
C-1N // NN · CODENAME
```

The number preserves chronology. The codename records the capability or understanding gained at that boundary.

Current lineage:

```text
C-1N // 00 · POSE     motor-assisted static-pose baseline
C-1N // 01 · SHUFFLE  current coordinated gait failure
C-1N // 02 · FRAME    next integration boundary after task-space telemetry is understood
C-1N // 03 · STAND    reserved for the first support-aware stable stance
C-1N // 04 · STRIDE   reserved for the first materially better walk
```

`POSE` is historical and does not claim demonstrated standing. `FRAME`, `STAND`, and `STRIDE` are reserved names, not completed checkpoints.

## Contract

- The test bench remains the place to isolate questions and repair mental models.
- C-1N remains the place to integrate mechanisms into one robot.
- A bench issue never requires C-1N work for completion.
- A C-1N hook is a post-experiment suggestion, not a dependency or next-node requirement.
- Hooks should appear only as: now that this experiment is closed, this may be a good time to improve C-1N in one targeted way that uses the mechanism just learned.
- C-1N work may expose a new question, but that question returns to the bench when isolation is useful.
- Preserve useful failures. Do not rewrite the project history into a clean final demo.
- Keep browser and WASM work downstream of a useful simulation. The web surface should expose robotics behavior, not create the learning target.

## Hook targets

| Bench evidence | Targeted C-1N improvement after closure |
| --- | --- |
| #2 Multi-DOF dynamics | Build or revise one articulated leg so its joints are treated as a coupled mechanism rather than independent pendulums. |
| #5 Trajectory tracking | Replace hand-staged leg poses with time-indexed joint trajectories and explicit phase relationships. |
| #6 Jacobians & task space | Add torso-frame foot X position, velocity, and acceleration beside the existing joint-space telemetry, align contact state with the traces, and use the mapping to explain the current gait failure before changing the controller. Preserve that boundary as `C-1N // 02 · FRAME`. |
| #20 Static support & equilibrium | Build a stance-only controller with the gait clock disabled. Expose active support geometry, center-of-mass projection, foot contact/load evidence, and torso attitude. Preserve the first understood support-aware stable stance as `C-1N // 03 · STAND`. |
| #8 Contact & friction | Add meaningful foot-ground contact and preserve one understandable slip or stance failure. |
| #4 Model-based control | Add a model-aware control comparison and one deliberate model mismatch to the integrated robot. |
| #7 Actuator limits | Give the joints realizable effort limits and expose a gait failure caused by saturation. |
| #12 System identification | Hide one interpretable C-1N parameter, infer it from one motion, and validate it on another. |
| #16 Differentiable dynamics | Backpropagate rollout loss to one interpretable C-1N parameter and verify the gradient numerically. |

These are opportunities, not a release plan. C-1N can take them in any order that makes sense for its current state.

## Version rule

Create a new checkpoint only when a capability or understood failure is worth preserving and comparing with prior behavior. Do not increment for cleanup, presentation polish, or elapsed time.

The intended evidence loop is:

`bench observation -> model update -> optional C-1N integration -> integrated failure -> new bench question when useful`
