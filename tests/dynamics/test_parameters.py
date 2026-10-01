"""Tests for DAWN vehicle parameters."""

import numpy as np
import pytest

from dawn.dynamics.parameters import VehicleParameters


def test_valid_vehicle_parameters_are_accepted():
    parameters = VehicleParameters(
        mass=2.0,
        inertia_body=np.diag([0.2, 0.3, 0.4]),
    )

    assert parameters.mass == 2.0
    np.testing.assert_allclose(
        parameters.inertia_body,
        np.diag([0.2, 0.3, 0.4]),
    )


@pytest.mark.parametrize(
    "invalid_mass",
    [
        0.0,
        -1.0,
        np.inf,
        -np.inf,
        np.nan,
    ],
)
def test_invalid_mass_is_rejected(invalid_mass):
    with pytest.raises(ValueError):
        VehicleParameters(
            mass=invalid_mass,
            inertia_body=np.eye(3),
        )


def test_inertia_tensor_with_wrong_shape_is_rejected():
    with pytest.raises(
        ValueError,
        match="shape",
    ):
        VehicleParameters(
            mass=1.0,
            inertia_body=np.eye(2),
        )


def test_nonfinite_inertia_tensor_is_rejected():
    inertia = np.eye(3)
    inertia[0, 0] = np.nan

    with pytest.raises(
        ValueError,
        match="finite",
    ):
        VehicleParameters(
            mass=1.0,
            inertia_body=inertia,
        )


def test_nonsymmetric_inertia_tensor_is_rejected():
    inertia = np.array(
        [
            [1.0, 0.2, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    with pytest.raises(
        ValueError,
        match="symmetric",
    ):
        VehicleParameters(
            mass=1.0,
            inertia_body=inertia,
        )


def test_non_positive_definite_inertia_tensor_is_rejected():
    inertia = np.diag([0.2, 0.3, -0.4])

    with pytest.raises(
        ValueError,
        match="positive definite",
    ):
        VehicleParameters(
            mass=1.0,
            inertia_body=inertia,
        )


def test_vehicle_parameters_own_a_copy_of_caller_inertia():
    inertia = np.diag([0.2, 0.3, 0.4])
    parameters = VehicleParameters(mass=2.0, inertia_body=inertia)

    inertia[:] = np.nan

    np.testing.assert_array_equal(parameters.inertia_body, np.diag([0.2, 0.3, 0.4]))
