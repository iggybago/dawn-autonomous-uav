"""Compare Euler and RK4 integration against analytical free fall."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from dawn.dynamics.inputs import ForcesMoments
from dawn.dynamics.integrators import euler_step, rk4_step
from dawn.dynamics.parameters import VehicleParameters
from dawn.dynamics.rigid_body import rigid_body_derivative
from dawn.dynamics.state import RigidBodyState


def main() -> None:
    """Compare numerical integrators for a free-fall trajectory."""
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

    times = [0.0]
    euler_positions_down = [0.0]
    rk4_positions_down = [0.0]

    for step in range(steps):
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

        times.append((step + 1) * dt)
        euler_positions_down.append(euler_state.position_ned[2])
        rk4_positions_down.append(rk4_state.position_ned[2])

    times_array = np.array(times)
    euler_positions_down_array = np.array(euler_positions_down)
    rk4_positions_down_array = np.array(rk4_positions_down)

    analytical_positions_down = 0.5 * gravity * times_array**2

    plt.figure(figsize=(8, 5))

    plt.plot(
        times_array,
        analytical_positions_down,
        label="Analytical",
        linewidth=2,
    )

    plt.plot(
        times_array,
        euler_positions_down_array,
        "--",
        label="Euler",
    )

    plt.plot(
        times_array,
        rk4_positions_down_array,
        "o",
        label="RK4",
        markersize=4,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Down position $p_D$ [m]")
    plt.title("DAWN — Free-Fall Integration Comparison")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_directory = Path(__file__).resolve().parents[1] / "results" / "figures"
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / "free_fall_integrator_comparison.png"

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
