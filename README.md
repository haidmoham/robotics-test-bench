# Robotics Test Bench

Fast, failure-driven robotics experiments. The goal is to use agents to remove setup and boilerplate friction without outsourcing the parts that build physical intuition.

## Operating loop

1. Predict what should happen.
2. Change one thing.
3. Run it.
4. Explain what happened.
5. Revert or record it.

Agent help is welcome for setup, API lookup, boilerplate, plotting, and repetitive code. I should own the prediction, physical interpretation, and diagnosis.

## MuJoCo mental model

- `mjModel` = what the simulated system **is**.
- `mjData` = what the system is **doing now**.
- `worldbody` = the fixed global coordinate frame, not a faithful model of "the world."
- Bodies form a tree rooted at the world frame.
- A robot can have its own root/base body inside that tree.
- Contacts and constraints add relationships beyond the body tree, so the full physical interaction structure can behave like a graph.
- `qpos` = generalized configuration.
- `qvel` = generalized velocity.
- `ctrl` = actuator command; it is not necessarily joint torque.
- `mj_step()` roughly means: kinematics -> collision/contact -> forces/constraints -> acceleration -> integration -> new state.

When behavior looks wrong, suspect more than the controller: model parameters, contacts, actuators, and numerical integration can all be the cause.

## Current experiment

`pendulum.py`: one rigid body, one hinge, gravity, and a MuJoCo viewer.

Useful things to perturb independently:

- gravity
- initial `qpos`
- initial `qvel`
- hinge axis
- mass
- arm length / geometry
- damping
- timestep
- floor / contact geometry

Keep experiments small enough that the result can be predicted before running them.
