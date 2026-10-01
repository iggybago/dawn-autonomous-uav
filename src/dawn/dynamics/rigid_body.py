"""Six-degree-of-freedom rigid-body dynamics for DAWN."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.quaternion import (
    quaternion_derivative,
    quaternion_to_rotation_matrix,
)
from dawn.dynamics.state import RigidBodyState


@dataclass
class RigidBodyStateDerivative:
    """Time derivative of the rigid-body state."""

    position_dot_ned: NDArray[np.float64]
    velocity_dot_ned: NDArray[np.float64]
    attitude_dot_q_b_n: NDArray[np.float64]
    angular_velocity_dot_body: NDArray[np.float64]


def rigid_body_derivative(
    state: RigidBodyState,
    inputs: ForcesMoments,
    parameters: VehicleParameters,
    gravity: float = 9.80665,
) -> RigidBodyStateDerivative:
    """Compute the derivative of the 6-DOF rigid-body state.

    Args:
        state: Current rigid-body state.
        inputs: Applied non-gravitational body forces and moments.
        parameters: Vehicle mass and inertia tensor.
        gravity: Gravitational acceleration magnitude [m/s^2].

    Returns:
        Time derivative of the rigid-body state.
    """
    if not np.isfinite(gravity):
        raise ValueError("Gravity magnitude must be finite.")

    if gravity < 0.0:
        raise ValueError("Gravity magnitude must be non-negative.")

    position_dot_ned = state.velocity_ned.copy()

    rotation_body_to_ned = quaternion_to_rotation_matrix(state.attitude_q_b_n)

    gravity_ned = np.array(
        [0.0, 0.0, gravity],
        dtype=np.float64,
    )

    velocity_dot_ned = (
        rotation_body_to_ned @ inputs.force_body / parameters.mass + gravity_ned
    )

    attitude_dot_q_b_n = quaternion_derivative(
        state.attitude_q_b_n,
        state.angular_velocity_body,
    )

    angular_momentum_body = parameters.inertia_body @ state.angular_velocity_body

    gyroscopic_term = np.cross(
        state.angular_velocity_body,
        angular_momentum_body,
    )

    rotational_rhs = inputs.moment_body - gyroscopic_term

    angular_velocity_dot_body = np.linalg.solve(
        parameters.inertia_body,
        rotational_rhs,
    )

    return RigidBodyStateDerivative(
        position_dot_ned=position_dot_ned,
        velocity_dot_ned=velocity_dot_ned,
        attitude_dot_q_b_n=attitude_dot_q_b_n,
        angular_velocity_dot_body=angular_velocity_dot_body,
    )
