# Agent log

## AI-20260808-001 — P vs. PD prediction

**Question**
What should look different when the pendulum uses position-only feedback versus position + velocity feedback?

**Human prediction**
P-only should overshoot/oscillate more. PD should damp motion and settle more cleanly.

**Action**
Ran the pendulum control experiment and compared P and PD behavior.

**Outcome**
Prediction matched the observed behavior.

**Effect on current belief**
Position error creates corrective drive; velocity feedback adds damping. This intuition is strong enough to move on rather than over-study the API.

Related: #1
