# Static support: centered ballast

Question: does a passive three-contact body with a centered ballast remain supported over a fixed rollout?

## Human prediction

The ballast is fixed directly above the original body center. It adds weight without shifting the whole-body COM sideways. With no perturbation, the contact loads should remain roughly balanced, no contact should be lost, no tipping edge should dominate, and roll/pitch should remain near zero.

## Model and run

This is deliberately not C-1N and has no controller. A free platform has three spherical ground contacts forming a triangle. The fixed orange ballast is centered on the platform. The report includes whole-body COM and ground projection, active contacts, normal loads, roll/pitch, angular velocity, and body height.

```bash
python static_support.py --duration 2
```

This first case is only the inside-support baseline. Edge, beyond-edge, and changed-support cases require new predictions.

Related: robotics-test-bench #24, Spider #11.
