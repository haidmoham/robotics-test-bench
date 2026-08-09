# Spider integration target

Target repository: `haidmoham/spider`

The spider is a longitudinal integration project. It consumes robotics concepts after the test bench makes them concrete.

## Contract

- The test bench remains the place to isolate questions and repair mental models.
- The spider remains the place to integrate mechanisms into one robot.
- A bench issue never requires spider work for completion.
- Spider work may expose a new question, but that question returns to the bench when isolation is useful.
- Each meaningful spider version should record which bench evidence justified the change.
- Preserve useful failures. Do not rewrite the project history into a clean final demo.
- Keep browser and WASM work downstream of a useful simulation. The web surface should expose robotics behavior, not create the learning target.

## Integration hooks

| Bench evidence | Spider use | Candidate version |
| --- | --- | --- |
| #2 Multi-DOF dynamics | Build the articulated leg model without independent-joint assumptions. | `v0.1` |
| #5 Trajectory tracking | Replace static poses with time-indexed leg trajectories and gait phase relationships. | `v0.2` |
| #8 Contact & friction | Add feet, ground contact, slip, stance, and failure under changed friction. | `v0.3` |
| #4 Model-based control | Carry torque decomposition and deliberate model mismatch into the integrated robot. | `v0.4` |
| #7 Actuator limits | Make gait feasibility depend on realizable actuation instead of unlimited commands. | `v0.4` |
| #12 System identification | Hide one physical parameter and infer it from spider behavior, then validate on another gait. | `v0.5` |
| #16 Differentiable dynamics | Backpropagate rollout loss to one interpretable physical or gait parameter and verify the gradient. | `v0.6` |

A later `v1.0` can expose the mature simulation through WASM when there is at least one useful behavior and one understandable failure worth interacting with.

## Version rule

Do not version by elapsed time or polish. Cut a meaningful version when a new robotics capability changes what the integrated spider can do or explain.

The intended evidence chain is:

`bench observation -> model update -> spider integration -> integrated failure -> new bench question when needed`
