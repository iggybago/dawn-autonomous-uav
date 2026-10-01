"""Tests for DAWN rigid-body force and moment inputs."""

import numpy as np
import pytest

from dawn.dynamics.inputs import ForcesMoments


def test_valid_forces_and_moments_are_accepted():
    inputs = ForcesMoments(
        force_body=np.array([1.0, 2.0, 3.0]),
        moment_body=np.array([0.1, 0.2, 0.3]),
    )

    np.testing.assert_allclose(
        inputs.force_body,
        np.array([1.0, 2.0, 3.0]),
    )

    np.testing.assert_allclose(
        inputs.moment_body,
        np.array([0.1, 0.2, 0.3]),
    )


def test_force_with_wrong_shape_is_rejected():
    with pytest.raises(
        ValueError,
        match="shape",
    ):
        ForcesMoments(
            force_body=np.array([1.0, 2.0]),
            moment_body=np.zeros(3),
        )


def test_moment_with_wrong_shape_is_rejected():
    with pytest.raises(
        ValueError,
        match="shape",
    ):
        ForcesMoments(
            force_body=np.zeros(3),
            moment_body=np.array([1.0, 2.0]),
        )


def test_nonfinite_force_is_rejected():
    with pytest.raises(
        ValueError,
        match="finite",
    ):
        ForcesMoments(
            force_body=np.array([0.0, np.nan, 0.0]),
            moment_body=np.zeros(3),
        )


def test_nonfinite_moment_is_rejected():
    with pytest.raises(
        ValueError,
        match="finite",
    ):
        ForcesMoments(
            force_body=np.zeros(3),
            moment_body=np.array([0.0, np.inf, 0.0]),
        )


def test_forces_and_moments_own_copies_of_caller_arrays():
    force = np.array([1.0, 2.0, 3.0])
    moment = np.array([0.1, 0.2, 0.3])
    inputs = ForcesMoments(force_body=force, moment_body=moment)

    force[:] = np.nan
    moment[:] = np.nan

    np.testing.assert_array_equal(inputs.force_body, [1.0, 2.0, 3.0])
    np.testing.assert_array_equal(inputs.moment_body, [0.1, 0.2, 0.3])
