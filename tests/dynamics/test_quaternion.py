"""Tests for quaternion utilities."""

import numpy as np

from dawn.dynamics.quaternion import (
    quaternion_derivative,
    quaternion_multiply,
    quaternion_to_rotation_matrix,
)


def test_identity_quaternion_gives_identity_rotation():
    q_b_n = np.array([1.0, 0.0, 0.0, 0.0])

    rotation = quaternion_to_rotation_matrix(q_b_n)

    np.testing.assert_allclose(rotation, np.eye(3), rtol=0.0, atol=1e-12)


def test_positive_90_deg_yaw_rotates_body_x_to_ned_y():
    half_angle = np.pi / 4.0
    q_b_n = np.array(
        [
            np.cos(half_angle),
            0.0,
            0.0,
            np.sin(half_angle),
        ]
    )

    rotation = quaternion_to_rotation_matrix(q_b_n)

    body_x = np.array([1.0, 0.0, 0.0])
    vector_ned = rotation @ body_x

    expected_ned = np.array([0.0, 1.0, 0.0])

    np.testing.assert_allclose(vector_ned, expected_ned, rtol=0.0, atol=1e-12)


def test_identity_quaternion_does_not_change_quaternion_product():
    q_identity = np.array([1.0, 0.0, 0.0, 0.0])

    q = np.array(
        [
            np.sqrt(2.0) / 2.0,
            0.0,
            0.0,
            np.sqrt(2.0) / 2.0,
        ]
    )

    result = quaternion_multiply(q_identity, q)

    np.testing.assert_allclose(result, q, rtol=0.0, atol=1e-12)


def test_positive_yaw_rate_gives_positive_initial_z_quaternion_derivative():
    q_b_n = np.array([1.0, 0.0, 0.0, 0.0])
    angular_velocity_body = np.array([0.0, 0.0, 2.0])

    q_dot = quaternion_derivative(q_b_n, angular_velocity_body)

    expected_q_dot = np.array([0.0, 0.0, 0.0, 1.0])

    np.testing.assert_allclose(q_dot, expected_q_dot, rtol=0.0, atol=1e-12)


def test_body_roll_rate_at_positive_yaw_uses_right_hamilton_product():
    # Initial +90-degree yaw maps Forward to East. Apply body roll p=2 rad/s.
    # With s=sqrt(1/2), the attitude is s*(1+k). A small body roll is
    # 1 + i*dt, so (1+k)*(1+i*dt) gives i+k*i = i+j (Hamilton k*i=j).
    # Thus q_dot = [0, s, s, 0] [1/s]. Reversing the order gives i*k=-j
    # and the wrong sign of q_dot_y. No production multiply/DCM builds this oracle.
    s = np.sqrt(0.5)
    q_b_n = np.array([s, 0.0, 0.0, s])
    angular_velocity_body = np.array([2.0, 0.0, 0.0])

    actual = quaternion_derivative(q_b_n, angular_velocity_body)

    np.testing.assert_allclose(actual, [0.0, s, s, 0.0], rtol=0.0, atol=1e-12)
