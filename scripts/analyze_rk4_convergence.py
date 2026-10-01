"""Analyze RK4 convergence for torque-free rigid-body rotation."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.integrators import rk4_step
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.quaternion import quaternion_to_rotation_matrix
from dawn.dynamics.state import RigidBodyState


def calculate_rotational_energy(
    state: RigidBodyState,
    parameters: VehicleParameters,
) -> float:
    """Return rigid-body rotational kinetic energy [J]."""
    omega_body = state.angular_velocity_body

    return float(0.5 * omega_body @ parameters.inertia_body @ omega_body)


def calculate_angular_momentum_ned(
    state: RigidBodyState,
    parameters: VehicleParameters,
) -> np.ndarray:
    """Return angular momentum expressed in the NED frame."""
    angular_momentum_body = parameters.inertia_body @ state.angular_velocity_body

    rotation_body_to_ned = quaternion_to_rotation_matrix(state.attitude_q_b_n)

    return rotation_body_to_ned @ angular_momentum_body


def run_simulation(
    dt: float,
    final_time: float,
) -> tuple[float, float]:
    """Run torque-free rotation and return maximum relative errors."""
    parameters = VehicleParameters(
        mass=1.0,
        inertia_body=np.diag([0.2, 0.3, 0.4]),
    )

    inputs = ForcesMoments(
        force_body=np.zeros(3),
        moment_body=np.zeros(3),
    )

    state = RigidBodyState(
        position_ned=np.zeros(3),
        velocity_ned=np.zeros(3),
        attitude_q_b_n=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity_body=np.array([1.0, 2.0, 3.0]),
    )

    initial_energy = calculate_rotational_energy(
        state,
        parameters,
    )

    initial_angular_momentum_ned = calculate_angular_momentum_ned(
        state,
        parameters,
    )

    maximum_relative_energy_error = 0.0
    maximum_relative_angular_momentum_error = 0.0

    steps = int(round(final_time / dt))

    for _ in range(steps):
        state = rk4_step(
            state,
            inputs,
            parameters,
            dt,
            gravity=0.0,
        )

        energy = calculate_rotational_energy(
            state,
            parameters,
        )

        angular_momentum_ned = calculate_angular_momentum_ned(
            state,
            parameters,
        )

        relative_energy_error = abs(energy - initial_energy) / abs(initial_energy)

        relative_angular_momentum_error = np.linalg.norm(
            angular_momentum_ned - initial_angular_momentum_ned
        ) / np.linalg.norm(initial_angular_momentum_ned)

        maximum_relative_energy_error = max(
            maximum_relative_energy_error,
            relative_energy_error,
        )

        maximum_relative_angular_momentum_error = max(
            maximum_relative_angular_momentum_error,
            relative_angular_momentum_error,
        )

    return (
        maximum_relative_energy_error,
        maximum_relative_angular_momentum_error,
    )


def calculate_observed_orders(
    time_steps: np.ndarray,
    errors: np.ndarray,
) -> np.ndarray:
    """Calculate observed convergence order between successive runs."""
    return np.log(errors[:-1] / errors[1:]) / np.log(time_steps[:-1] / time_steps[1:])


def main() -> None:
    """Run and visualize the RK4 convergence study."""
    final_time = 5.0

    time_steps = np.array(
        [
            0.1,
            0.05,
            0.025,
            0.0125,
        ]
    )

    energy_errors = []
    angular_momentum_errors = []

    for dt in time_steps:
        energy_error, angular_momentum_error = run_simulation(
            dt,
            final_time,
        )

        energy_errors.append(energy_error)
        angular_momentum_errors.append(angular_momentum_error)

    energy_errors_array = np.array(energy_errors)
    angular_momentum_errors_array = np.array(angular_momentum_errors)

    energy_orders = calculate_observed_orders(
        time_steps,
        energy_errors_array,
    )

    angular_momentum_orders = calculate_observed_orders(
        time_steps,
        angular_momentum_errors_array,
    )

    print("RK4 convergence study")
    print("=====================")
    print()

    for index, dt in enumerate(time_steps):
        print(
            f"dt = {dt:.4f} s | "
            f"relative energy error = "
            f"{energy_errors_array[index]:.3e} | "
            f"relative angular momentum error = "
            f"{angular_momentum_errors_array[index]:.3e}"
        )

    print()
    print("Observed convergence orders")
    print("===========================")

    for index in range(len(energy_orders)):
        print(
            f"{time_steps[index]:.4f} -> "
            f"{time_steps[index + 1]:.4f} s | "
            f"energy p = {energy_orders[index]:.3f} | "
            f"angular momentum p = "
            f"{angular_momentum_orders[index]:.3f}"
        )

    reference_error = max(
        energy_errors_array[0],
        angular_momentum_errors_array[0],
    )

    fourth_order_reference = reference_error * (time_steps / time_steps[0]) ** 4

    figure, axis = plt.subplots(
        figsize=(8, 6),
    )

    axis.loglog(
        time_steps,
        energy_errors_array,
        "o-",
        label="Rotational energy error",
    )

    axis.loglog(
        time_steps,
        angular_momentum_errors_array,
        "s-",
        label="Angular momentum error",
    )

    axis.loglog(
        time_steps,
        fourth_order_reference,
        "--",
        label="Fourth-order reference",
    )

    axis.set_xlabel("Time step Δt [s]")
    axis.set_ylabel("Maximum relative error [-]")
    axis.set_title("DAWN — RK4 Convergence Study")
    axis.grid(
        True,
        which="both",
        alpha=0.3,
    )
    axis.legend()

    figure.tight_layout()

    output_directory = Path(__file__).resolve().parents[1] / "results" / "figures"

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / "rk4_convergence_study.png"

    figure.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(figure)

    print()
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
