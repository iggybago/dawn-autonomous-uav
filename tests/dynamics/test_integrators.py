import numpy as np
import pytest

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.integrators import euler_step, rk4_step
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.quaternion import quaternion_to_rotation_matrix
from dawn.dynamics.rigid_body import RigidBodyStateDerivative, rigid_body_derivative
from dawn.dynamics.state import RigidBodyState


def test_euler_step_integrates_constant_velocity():
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.array([5.0, 0.0, 0.0]),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )

    derivative = RigidBodyStateDerivative(
        position_dot_ned=np.array([5.0, 0.0, 0.0]),
        velocity_dot_ned=np.zeros(3),
        attitude_dot_q_b_n=np.zeros(4),
        angular_velocity_dot_body=np.zeros(3),
    )

    next_state = euler_step(
        state,
        derivative,
        dt=0.2,
    )

    np.testing.assert_allclose(
        next_state.position_ned,
        np.array([1.0, 0.0, 0.0]),
        rtol=0.0,
        atol=1e-12,
    )


def test_euler_step_preserves_unit_quaternion():
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.array([0.0, 0.0, 1.0]),
    )

    derivative = RigidBodyStateDerivative(
        position_dot_ned=np.zeros(3),
        velocity_dot_ned=np.zeros(3),
        attitude_dot_q_b_n=np.array([0.0, 0.0, 0.0, 0.5]),
        angular_velocity_dot_body=np.zeros(3),
    )

    next_state = euler_step(
        state,
        derivative,
        dt=0.1,
    )

    np.testing.assert_allclose(
        np.linalg.norm(next_state.attitude_q_b_n),
        1.0,
        rtol=0.0,
        atol=1e-12,
    )


def test_free_fall_euler_and_rk4_against_analytical_solution():
    gravity = 9.80665
    dt = 0.1
    final_time = 1.0
    steps = int(final_time / dt)

    parameters = VehicleParameters(
        mass=1.0,
        inertia_body=np.eye(3),
    )

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    initial_state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )

    euler_state = initial_state
    rk4_state = initial_state

    for _ in range(steps):
        euler_derivative = rigid_body_derivative(
            euler_state,
            inputs,
            parameters,
            gravity,
        )

        euler_state = euler_step(
            euler_state,
            euler_derivative,
            dt,
        )

        rk4_state = rk4_step(
            rk4_state,
            inputs,
            parameters,
            dt,
            gravity,
        )

    analytical_position_down = 0.5 * gravity * final_time**2
    analytical_velocity_down = gravity * final_time

    euler_position_error = abs(euler_state.position_ned[2] - analytical_position_down)
    rk4_position_error = abs(rk4_state.position_ned[2] - analytical_position_down)

    np.testing.assert_allclose(
        rk4_state.position_ned[2],
        analytical_position_down,
        rtol=0.0,
        atol=1e-12,
    )

    np.testing.assert_allclose(
        rk4_state.velocity_ned[2],
        analytical_velocity_down,
        rtol=0.0,
        atol=1e-12,
    )

    assert rk4_position_error < euler_position_error


def test_rk4_constant_yaw_rate_against_analytical_solution():
    yaw_rate = 1.0
    dt = 0.1
    final_time = 1.0
    steps = int(final_time / dt)

    parameters = VehicleParameters(
        mass=1.0,
        inertia_body=np.diag([1.0, 1.0, 1.0]),
    )

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.array([0.0, 0.0, yaw_rate]),
    )

    for _ in range(steps):
        state = rk4_step(
            state,
            inputs,
            parameters,
            dt,
            gravity=0.0,
        )

    expected_quaternion = np.array(
        [
            np.cos(yaw_rate * final_time / 2.0),
            0.0,
            0.0,
            np.sin(yaw_rate * final_time / 2.0),
        ]
    )

    # For unit quaternions, the shorter chord is 2*sin(error_angle/4),
    # and the longer chord is 2*cos(error_angle/4). Taking min/max makes
    # this distance invariant to q -> -q and stable for small errors.
    difference_norm = np.linalg.norm(state.attitude_q_b_n - expected_quaternion)
    sum_norm = np.linalg.norm(state.attitude_q_b_n + expected_quaternion)
    attitude_error_rad = 4.0 * np.arctan2(
        min(difference_norm, sum_norm), max(difference_norm, sum_norm)
    )

    # A 1 microradian budget permits margin for stage projection: the usual
    # RK4 leading phase-error scale T*r*(r*dt/2)^4/120 is about 5.2e-8 rad.
    # Normalized Euler has error T*r - 2*steps*atan(r*dt/2) = 8.3e-4 rad,
    # over 800 times this budget. This is an accuracy guard for this scenario.
    assert attitude_error_rad < 1e-6

    np.testing.assert_allclose(
        state.angular_velocity_body,
        np.array([0.0, 0.0, yaw_rate]),
        rtol=0.0,
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "invalid_dt",
    [0.0, -0.1, np.nan, np.inf],
)
def test_euler_rejects_invalid_time_step(invalid_dt):
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )

    derivative = RigidBodyStateDerivative(
        position_dot_ned=np.zeros(3),
        velocity_dot_ned=np.zeros(3),
        attitude_dot_q_b_n=np.zeros(4),
        angular_velocity_dot_body=np.zeros(3),
    )

    with pytest.raises(ValueError):
        euler_step(state, derivative, invalid_dt)


@pytest.mark.parametrize(
    "invalid_dt",
    [0.0, -0.1, np.nan, np.inf],
)
def test_rk4_rejects_invalid_time_step(invalid_dt):
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.zeros(3),
    )

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    parameters = VehicleParameters(
        mass=1.0,
        inertia_body=np.eye(3),
    )

    with pytest.raises(ValueError):
        rk4_step(
            state,
            inputs,
            parameters,
            invalid_dt,
        )


def test_rk4_torque_free_rotation_bounds_energy_and_inertial_momentum_drift():
    parameters = VehicleParameters(mass=1.0, inertia_body=np.diag([0.2, 0.3, 0.4]))
    inputs = ForcesMoments(force_body=np.zeros(3), moment_body=np.zeros(3))
    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.array([1.0, 2.0, 3.0]),
    )
    dt = 0.05
    final_time = 5.0
    # Analytical initial invariants: E0 = (0.2*1^2+0.3*2^2+0.4*3^2)/2;
    # H_n0 = J*omega0 because the initial body and NED frames coincide.
    initial_energy = 2.5  # [J]
    initial_momentum_ned = np.array([0.2, 0.6, 1.2])  # [kg m^2/s]

    # docs/05 section 12 reports maximum relative errors of 1.810e-7 (E)
    # and 2.681e-6 (H_n) for this dt/horizon. Budgets of 1e-6 and 1e-5
    # give modest numerical margin while guarding against lost coupling,
    # frame errors and lower-order propagation; exact conservation is not claimed.
    for _ in range(round(final_time / dt)):
        state = rk4_step(state, inputs, parameters, dt, gravity=0.0)
        omega = state.angular_velocity_body
        energy = 0.5 * omega @ parameters.inertia_body @ omega
        momentum_ned = quaternion_to_rotation_matrix(state.attitude_q_b_n) @ (
            parameters.inertia_body @ omega
        )
        relative_energy_error = abs(energy - initial_energy) / initial_energy
        relative_momentum_error = np.linalg.norm(
            momentum_ned - initial_momentum_ned
        ) / np.linalg.norm(initial_momentum_ned)

        # Check every sample, including finite errors; a NaN cannot pass '<'.
        assert relative_energy_error < 1e-6
        assert relative_momentum_error < 1e-5
