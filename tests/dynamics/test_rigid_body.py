"""Tests for DAWN six-degree-of-freedom rigid-body dynamics."""

import numpy as np
import pytest

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.rigid_body import rigid_body_derivative
from dawn.dynamics.state import RigidBodyState


def make_level_stationary_state() -> RigidBodyState:
    """Return a stationary state aligned with the NED frame."""
    return RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )


def make_test_vehicle() -> VehicleParameters:
    """Return simple vehicle parameters for analytical tests."""
    return VehicleParameters(
        mass=2.0,
        inertia_body=np.diag([0.2, 0.3, 0.4]),
    )


def test_free_fall_accelerates_downward():
    state = make_level_stationary_state()
    parameters = make_test_vehicle()

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    derivative = rigid_body_derivative(state, inputs, parameters)

    expected_acceleration_ned = np.array([0.0, 0.0, 9.80665])

    np.testing.assert_allclose(
        derivative.velocity_dot_ned,
        expected_acceleration_ned,
        rtol=0.0,
        atol=1e-12,
    )


def test_level_hover_has_zero_linear_acceleration():
    state = make_level_stationary_state()
    parameters = make_test_vehicle()

    gravity = 9.80665
    thrust = parameters.mass * gravity

    inputs = ForcesMoments(
        force_body=np.array([0.0, 0.0, -thrust]),
        moment_body=np.zeros(3),
    )

    derivative = rigid_body_derivative(
        state,
        inputs,
        parameters,
        gravity=gravity,
    )

    np.testing.assert_allclose(
        derivative.velocity_dot_ned,
        np.zeros(3),
        rtol=0.0,
        atol=1e-12,
    )


def test_pure_roll_moment_produces_expected_roll_acceleration():
    state = make_level_stationary_state()
    parameters = make_test_vehicle()

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.array([0.1, 0.0, 0.0]),
    )

    derivative = rigid_body_derivative(state, inputs, parameters)

    expected_angular_acceleration = np.array([0.5, 0.0, 0.0])

    np.testing.assert_allclose(
        derivative.angular_velocity_dot_body,
        expected_angular_acceleration,
        rtol=0.0,
        atol=1e-12,
    )


def test_zero_angular_velocity_gives_zero_attitude_derivative():
    state = make_level_stationary_state()
    parameters = make_test_vehicle()

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    derivative = rigid_body_derivative(state, inputs, parameters)

    np.testing.assert_allclose(
        derivative.attitude_dot_q_b_n,
        np.zeros(4),
        rtol=0.0,
        atol=1e-12,
    )


def test_positive_pitch_tilts_thrust_toward_south():
    parameters = make_test_vehicle()

    pitch = np.deg2rad(30.0)

    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array(
            [
                np.cos(pitch / 2.0),
                0.0,
                np.sin(pitch / 2.0),
                0.0,
            ]
        ),
        angular_velocity_body=np.zeros(3),
    )

    gravity = 9.80665
    thrust = parameters.mass * gravity

    inputs = ForcesMoments(
        force_body=np.array([0.0, 0.0, -thrust]),
        moment_body=np.zeros(3),
    )

    derivative = rigid_body_derivative(
        state,
        inputs,
        parameters,
        gravity=gravity,
    )

    expected_acceleration_ned = np.array(
        [
            -gravity * np.sin(pitch),
            0.0,
            gravity * (1.0 - np.cos(pitch)),
        ]
    )

    np.testing.assert_allclose(
        derivative.velocity_dot_ned,
        expected_acceleration_ned,
        rtol=0.0,
        atol=1e-12,
    )


def test_torque_free_rotation_includes_gyroscopic_coupling():
    parameters = make_test_vehicle()

    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.array([1.0, 2.0, 3.0]),
    )

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    derivative = rigid_body_derivative(
        state,
        inputs,
        parameters,
        gravity=0.0,
    )

    expected_angular_acceleration = np.array([-3.0, 2.0, -0.5])

    np.testing.assert_allclose(
        derivative.angular_velocity_dot_body,
        expected_angular_acceleration,
        rtol=0.0,
        atol=1e-12,
    )


def test_negative_gravity_is_rejected():
    state = make_level_stationary_state()
    vehicle = make_test_vehicle()
    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    with pytest.raises(ValueError, match="non-negative"):
        rigid_body_derivative(
            state,
            inputs,
            vehicle,
            gravity=-9.80665,
        )


def test_nonfinite_gravity_is_rejected():
    state = make_level_stationary_state()
    vehicle = make_test_vehicle()
    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    with pytest.raises(ValueError, match="finite"):
        rigid_body_derivative(
            state,
            inputs,
            vehicle,
            gravity=np.nan,
        )


def test_position_derivative_does_not_alias_state_velocity():
    state = make_level_stationary_state()
    state.velocity_ned[:] = [1.0, 2.0, 3.0]
    inputs = ForcesMoments(force_body=np.zeros(3), moment_body=np.zeros(3))

    derivative = rigid_body_derivative(state, inputs, make_test_vehicle())
    np.testing.assert_array_equal(derivative.position_dot_ned, [1.0, 2.0, 3.0])
    derivative.position_dot_ned[:] = np.nan

    np.testing.assert_array_equal(state.velocity_ned, [1.0, 2.0, 3.0])


def test_full_inertia_matches_rotated_principal_axis_solution():
    # Q maps principal-axis coordinates into FRD body coordinates by a
    # right-handed 45-degree rotation about +Z. It is not the body-to-NED DCM.
    c = np.sqrt(0.5)
    principal_to_body = np.array([[c, -c, 0.0], [c, c, 0.0], [0.0, 0.0, 1.0]])
    inertia_principal = np.diag([0.2, 0.3, 0.4])  # [kg m^2]
    parameters = VehicleParameters(
        mass=2.0,
        inertia_body=principal_to_body @ inertia_principal @ principal_to_body.T,
    )
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=principal_to_body @ np.array([1.0, 2.0, 3.0]),
    )
    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=principal_to_body @ np.array([0.1, 0.2, 0.3]),  # [N m]
    )

    # Independent scalar Euler equations in principal axes, in rad/s^2:
    # p_dot = (0.1 + (0.3 - 0.4)*2*3)/0.2 = -2.5
    # q_dot = (0.2 + (0.4 - 0.2)*1*3)/0.3 = 8/3
    # r_dot = (0.3 + (0.2 - 0.3)*1*2)/0.4 = 0.25
    expected = principal_to_body @ np.array([-2.5, 8.0 / 3.0, 0.25])
    derivative = rigid_body_derivative(state, inputs, parameters, gravity=0.0)

    # Roundoff allowance for small, well-conditioned float64 matrix operations.
    np.testing.assert_allclose(
        derivative.angular_velocity_dot_body, expected, rtol=0.0, atol=1e-12
    )
