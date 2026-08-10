# Spider integration target

Target repository: `haidmoham/spider`

The spider is a longitudinal integration project. It consumes robotics concepts after the test bench makes them concrete.

## Contract

- The test bench remains the place to isolate questions and repair mental models.
- The spider remains the place to integrate mechanisms into one robot.
- A bench issue never requires spider work for completion.
- A spider hook is a post-experiment suggestion, not a dependency or next-node requirement.
- Hooks should appear only as: now that this experiment is closed, this may be a good time to improve the spider in one targeted way that uses the mechanism just learned.
- Spider work may expose a new question, but that question returns to the bench when isolation is useful.
- Preserve useful failures. Do not rewrite the project history into a clean final demo.
- Keep browser and WASM work downstream of a useful simulation. The web surface should expose robotics behavior, not create the learning target.

## Hook targets

| Bench evidence | Targeted spider improvement after closure |
| --- | --- |
| #2 Multi-DOF dynamics | Build or revise one articulated leg so its joints are treated as a coupled mechanism rather than independent pendulums. |
| #5 Trajectory tracking | Replace hand-staged leg poses with time-indexed joint trajectories and explicit phase relationships. |
| #6 Jacobians & task space | Add torso-frame foot X position, velocity, and acceleration beside the existing joint-space telemetry, align contact state with the traces, and use the mapping to explain the current gait failure before changing the controller. |
| #8 Contact & friction | Add meaningful foot-ground contact and preserve one understandable slip or stance failure. |
| #4 Model-based control | Add a model-aware control comparison and one deliberate model mismatch to the integrated robot. |
| #7 Actuator limits | Give the joints realizable effort limits and expose a gait failure caused by saturation. |
| #12 System identification | Hide one interpretable spider parameter, infer it from one motion, and validate it on another. |
| #16 Differentiable dynamics | Backpropagate rollout loss to one interpretable spider parameter and verify the gradient numerically. |

These are opportunities, not a release plan. The spider can take them in any order that makes sense for its current state.

## Version rule

Version by meaningful capability changes, not elapsed time or polish. A version is useful when it preserves a new robotics capability or a newly understood failure.

The intended evidence loop is:

`bench observation -> model update -> optional spider integration -> integrated failure -> new bench question when useful`
