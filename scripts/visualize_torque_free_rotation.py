"""Visualize torque-free rigid-body rotation and conserved quantities."""

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


def main() -> None:
    """Simulate and visualize torque-free rigid-body rotation."""
    dt = 0.01
    final_time = 5.0
    steps = int(final_time / dt)

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

    times = [0.0]
    angular_velocity_history = [state.angular_velocity_body.copy()]
    energy_history = [calculate_rotational_energy(state, parameters)]
    angular_momentum_ned_history = [calculate_angular_momentum_ned(state, parameters)]

    for step in range(steps):
        state = rk4_step(
            state,
            inputs,
            parameters,
            dt,
            gravity=0.0,
        )

        times.append((step + 1) * dt)
        angular_velocity_history.append(state.angular_velocity_body.copy())
        energy_history.append(calculate_rotational_energy(state, parameters))
        angular_momentum_ned_history.append(
            calculate_angular_momentum_ned(state, parameters)
        )

    times_array = np.array(times)
    angular_velocity_array = np.array(angular_velocity_history)
    energy_array = np.array(energy_history)
    angular_momentum_ned_array = np.array(angular_momentum_ned_history)

    initial_energy = energy_array[0]
    initial_angular_momentum_ned = angular_momentum_ned_array[0]

    energy_error = energy_array - initial_energy

    angular_momentum_error = np.linalg.norm(
        angular_momentum_ned_array - initial_angular_momentum_ned,
        axis=1,
    )

    figure, axes = plt.subplots(
        3,
        1,
        figsize=(9, 10),
        sharex=True,
    )

    axes[0].plot(
        times_array,
        angular_velocity_array[:, 0],
        label="p",
    )
    axes[0].plot(
        times_array,
        angular_velocity_array[:, 1],
        label="q",
    )
    axes[0].plot(
        times_array,
        angular_velocity_array[:, 2],
        label="r",
    )
    axes[0].set_ylabel("Angular velocity [rad/s]")
    axes[0].set_title("Body Angular Velocity")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    axes[1].plot(
        times_array,
        energy_error,
    )
    axes[1].set_ylabel("$E_{rot} - E_{rot,0}$ [J]")
    axes[1].set_title("Rotational Energy Conservation")
    axes[1].grid(alpha=0.3)

    axes[2].plot(
        times_array,
        angular_momentum_ned_array[:, 0],
        label="$H_N$",
    )
    axes[2].plot(
        times_array,
        angular_momentum_ned_array[:, 1],
        label="$H_E$",
    )
    axes[2].plot(
        times_array,
        angular_momentum_ned_array[:, 2],
        label="$H_D$",
    )
    axes[2].set_xlabel("Time [s]")
    axes[2].set_ylabel("Angular momentum [kg m²/s]")
    axes[2].set_title("Angular Momentum in NED")
    axes[2].grid(alpha=0.3)
    axes[2].legend()

    figure.suptitle("DAWN — Torque-Free Rotation: Numerical Verification")
    figure.tight_layout()

    output_directory = Path(__file__).resolve().parents[1] / "results" / "figures"
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / "torque_free_rotation_validation.png"

    figure.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(figure)

    maximum_energy_error = np.max(np.abs(energy_error))
    maximum_angular_momentum_error = np.max(angular_momentum_error)

    print(f"Initial rotational energy: {initial_energy:.6f} J")
    print(f"Initial angular momentum NED: {initial_angular_momentum_ned}")
    print(f"Maximum rotational energy error: {maximum_energy_error:.3e} J")
    print(
        f"Maximum angular momentum error: {maximum_angular_momentum_error:.3e} kg m^2/s"
    )
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
