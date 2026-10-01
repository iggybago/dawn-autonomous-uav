"""Numerical integration methods for DAWN flight dynamics."""

import numpy as np

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.rigid_body import (
    RigidBodyStateDerivative,
    rigid_body_derivative,
)
from dawn.dynamics.state import RigidBodyState


def euler_step(
    state: RigidBodyState,
    derivative: RigidBodyStateDerivative,
    dt: float,
) -> RigidBodyState:
    """Advance the rigid-body state by one explicit Euler step.

    Normalize the attitude quaternion after propagation.

    Args:
        state: Current rigid-body state.
        derivative: State derivative evaluated at the current state.
        dt: Integration time step [s].

    Returns:
        State after one Euler integration step.
    """

    if not np.isfinite(dt):
        raise ValueError("Integration time step must be finite.")

    if dt <= 0.0:
        raise ValueError("Integration time step must be greater than zero.")

    attitude_q_b_n = state.attitude_q_b_n + derivative.attitude_dot_q_b_n * dt

    attitude_q_b_n = attitude_q_b_n / np.linalg.norm(attitude_q_b_n)

    return RigidBodyState(
        position_ned=state.position_ned + derivative.position_dot_ned * dt,
        velocity_ned=state.velocity_ned + derivative.velocity_dot_ned * dt,
        attitude_q_b_n=attitude_q_b_n,
        angular_velocity_body=state.angular_velocity_body
        + derivative.angular_velocity_dot_body * dt,
    )


def _state_plus_derivative(
    state: RigidBodyState,
    derivative: RigidBodyStateDerivative,
    scale: float,
) -> RigidBodyState:
    """Return state + scale * derivative with a normalized attitude quaternion."""
    attitude_q_b_n = state.attitude_q_b_n + scale * derivative.attitude_dot_q_b_n

    attitude_q_b_n = attitude_q_b_n / np.linalg.norm(attitude_q_b_n)

    return RigidBodyState(
        position_ned=state.position_ned + scale * derivative.position_dot_ned,
        velocity_ned=state.velocity_ned + scale * derivative.velocity_dot_ned,
        attitude_q_b_n=attitude_q_b_n,
        angular_velocity_body=state.angular_velocity_body
        + scale * derivative.angular_velocity_dot_body,
    )


def rk4_step(
    state: RigidBodyState,
    inputs: ForcesMoments,
    parameters: VehicleParameters,
    dt: float,
    gravity: float = 9.80665,
) -> RigidBodyState:
    """Advance the state with RK4 stages and quaternion projection.

    Body-force and body-moment components are held constant over the step.
    Mass and body-frame inertia are constant model parameters. Intermediate
    stage quaternions and the final quaternion are normalized, so this is not
    literal unconstrained textbook RK4 on all 13 state components.

    The studies in docs/05_flight_dynamics_model.md provide scenario-specific
    evidence consistent with fourth-order behavior, not a universal proof.

    Args:
        state: Current center-of-mass state and body-to-NED attitude.
        inputs: Non-gravitational FRD force [N] and moment about the center
            of mass [N m], held constant throughout this step.
        parameters: Constant mass [kg] and body-frame inertia [kg m^2].
        dt: Finite, strictly positive integration time step [s].
        gravity: Finite, non-negative gravity magnitude [m/s^2].

    Returns:
        Propagated state with a unit attitude quaternion.
    """

    if not np.isfinite(dt):
        raise ValueError("Integration time step must be finite.")

    if dt <= 0.0:
        raise ValueError("Integration time step must be greater than zero.")

    k1 = rigid_body_derivative(
        state,
        inputs,
        parameters,
        gravity,
    )

    state_k2 = _state_plus_derivative(state, k1, dt / 2.0)
    k2 = rigid_body_derivative(
        state_k2,
        inputs,
        parameters,
        gravity,
    )

    state_k3 = _state_plus_derivative(state, k2, dt / 2.0)
    k3 = rigid_body_derivative(
        state_k3,
        inputs,
        parameters,
        gravity,
    )

    state_k4 = _state_plus_derivative(state, k3, dt)
    k4 = rigid_body_derivative(
        state_k4,
        inputs,
        parameters,
        gravity,
    )

    position_dot = (
        k1.position_dot_ned
        + 2.0 * k2.position_dot_ned
        + 2.0 * k3.position_dot_ned
        + k4.position_dot_ned
    ) / 6.0

    velocity_dot = (
        k1.velocity_dot_ned
        + 2.0 * k2.velocity_dot_ned
        + 2.0 * k3.velocity_dot_ned
        + k4.velocity_dot_ned
    ) / 6.0

    attitude_dot = (
        k1.attitude_dot_q_b_n
        + 2.0 * k2.attitude_dot_q_b_n
        + 2.0 * k3.attitude_dot_q_b_n
        + k4.attitude_dot_q_b_n
    ) / 6.0

    angular_velocity_dot = (
        k1.angular_velocity_dot_body
        + 2.0 * k2.angular_velocity_dot_body
        + 2.0 * k3.angular_velocity_dot_body
        + k4.angular_velocity_dot_body
    ) / 6.0

    weighted_derivative = RigidBodyStateDerivative(
        position_dot_ned=position_dot,
        velocity_dot_ned=velocity_dot,
        attitude_dot_q_b_n=attitude_dot,
        angular_velocity_dot_body=angular_velocity_dot,
    )

    return _state_plus_derivative(
        state,
        weighted_derivative,
        dt,
    )
