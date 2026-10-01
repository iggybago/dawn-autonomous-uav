"""Tests for DAWN rigid-body state validation."""

import numpy as np
import pytest

from dawn.dynamics.state import RigidBodyState


def make_valid_state() -> RigidBodyState:
    """Return a valid rigid-body state for validation tests."""
    return RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )


def test_valid_rigid_body_state_is_accepted():
    state = make_valid_state()

    np.testing.assert_allclose(
        state.position_ned,
        np.zeros(3),
    )
    np.testing.assert_allclose(
        state.velocity_ned,
        np.zeros(3),
    )
    np.testing.assert_allclose(
        state.attitude_q_b_n,
        np.array([1.0, 0.0, 0.0, 0.0]),
    )
    np.testing.assert_allclose(
        state.angular_velocity_body,
        np.zeros(3),
    )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("position_ned", np.zeros(2)),
        ("velocity_ned", np.zeros(2)),
        ("attitude_q_b_n", np.zeros(3)),
        ("angular_velocity_body", np.zeros(2)),
    ],
)
def test_state_vector_with_wrong_shape_is_rejected(
    field_name,
    invalid_value,
):
    state_data = {
        "position_ned": np.zeros(3),
        "velocity_ned": np.zeros(3),
        "attitude_q_b_n": np.array([1.0, 0.0, 0.0, 0.0]),
        "angular_velocity_body": np.zeros(3),
    }

    state_data[field_name] = invalid_value

    with pytest.raises(ValueError, match="shape"):
        RigidBodyState(**state_data)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        (
            "position_ned",
            np.array([np.nan, 0.0, 0.0]),
        ),
        (
            "velocity_ned",
            np.array([0.0, np.inf, 0.0]),
        ),
        (
            "attitude_q_b_n",
            np.array([np.nan, 0.0, 0.0, 0.0]),
        ),
        (
            "angular_velocity_body",
            np.array([0.0, 0.0, np.inf]),
        ),
    ],
)
def test_nonfinite_state_value_is_rejected(
    field_name,
    invalid_value,
):
    state_data = {
        "position_ned": np.zeros(3),
        "velocity_ned": np.zeros(3),
        "attitude_q_b_n": np.array([1.0, 0.0, 0.0, 0.0]),
        "angular_velocity_body": np.zeros(3),
    }

    state_data[field_name] = invalid_value

    with pytest.raises(ValueError, match="finite"):
        RigidBodyState(**state_data)


def test_nonunit_quaternion_is_rejected():
    with pytest.raises(
        ValueError,
        match="unit norm",
    ):
        RigidBodyState(
            position_ned=np.zeros(3),
            velocity_ned=np.zeros(3),
            attitude_q_b_n=np.array([2.0, 0.0, 0.0, 0.0]),
            angular_velocity_body=np.zeros(3),
        )


def test_zero_quaternion_is_rejected():
    with pytest.raises(
        ValueError,
        match="unit norm",
    ):
        RigidBodyState(
            position_ned=np.zeros(3),
            velocity_ned=np.zeros(3),
            attitude_q_b_n=np.zeros(4),
            angular_velocity_body=np.zeros(3),
        )


def test_state_owns_copies_of_caller_arrays():
    state_data = {
        "position_ned": np.array([1.0, 2.0, 3.0]),
        "velocity_ned": np.array([4.0, 5.0, 6.0]),
        "attitude_q_b_n": np.array([1.0, 0.0, 0.0, 0.0]),
        "angular_velocity_body": np.array([0.1, 0.2, 0.3]),
    }
    expected = {name: value.copy() for name, value in state_data.items()}
    state = RigidBodyState(**state_data)

    for value in state_data.values():
        value[:] = np.nan

    for name, value in expected.items():
        np.testing.assert_array_equal(getattr(state, name), value)
