# C-1N standing requirements ledger

This is the versioned cross-repository ledger for `C-1N // 02 · STAND`.
Each source repository retains its own evidence and implementation details.
Update this ledger only when a requirement's status, evidence boundary, or next
integration gate changes.

| ID | Requirement | Canonical source | Status | Evidence or next gate |
| --- | --- | --- | --- | --- |
| STAND-01 | Make fixed-foot support measurable through contact geometry, COM projection, support load, and torso attitude. | `robotics-test-bench` #24 | completed | Fixed-foot fixture brackets margin exhaustion and rear unloading between `+0.96 m` and `+0.98 m` payload shift. |
| STAND-02 | Establish whether one C-1N leg can reach the required outward-and-down support state. | `robotics-test-bench` #31 | completed | The current two-DOF leg leaves a `0.067 m` residual; the experimental orthogonal proximal hinge reaches the same target to solver tolerance. |
| STAND-03 | Integrate a gait-disabled, support-aware C-1N stance. | `haidmoham/spider` | active | Expose shared-frame support geometry, COM projection, contact/load data, and torso attitude. |
| STAND-04 | Preserve a prediction-led physics repair analysis for a concrete standing failure. | `haidmoham/spider` #12 | active | The static-support notebook is the first candidate. Promote it only after its observed result guides a C-1N change or diagnostic. |
| STAND-05 | Demonstrate reproducible C-1N stable support under a fixed evaluation and declared perturbation. | `haidmoham/spider` | blocked by STAND-03 | Preserve rollout conditions, success tolerance, failure condition, and important failed hypotheses. |

## Update rule

- `active`: work can proceed now.
- `blocked by`: an explicit prerequisite has not met its evidence boundary.
- Do not mark a row complete from a plausible pose, code scaffold, or one attractive rollout.
- Add new rows only for durable capability or evidence requirements. Keep transient tasks in the owning issue or experiment log.
