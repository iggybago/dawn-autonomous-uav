"""State definitions for DAWN rigid-body dynamics."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class RigidBodyState:
    """State of the DAWN rigid-body model.

    Conventions:
        - Center-of-mass position is expressed in NED [m].
        - Center-of-mass linear velocity is expressed in NED [m/s].
        - Attitude is q_b_n, scalar-first [w, x, y, z].
        - Angular velocity is expressed in the FRD body frame [rad/s].

    Arrays are copied and validated at construction. Direct field mutation
    remains possible and is not revalidated; callers must preserve validity.
    """

    position_ned: NDArray[np.float64]
    velocity_ned: NDArray[np.float64]
    attitude_q_b_n: NDArray[np.float64]
    angular_velocity_body: NDArray[np.float64]

    def __post_init__(self) -> None:
        """Validate and normalize rigid-body state data types."""
        self.position_ned = np.asarray(
            self.position_ned,
            dtype=np.float64,
        ).copy()
        self.velocity_ned = np.asarray(
            self.velocity_ned,
            dtype=np.float64,
        ).copy()
        self.attitude_q_b_n = np.asarray(
            self.attitude_q_b_n,
            dtype=np.float64,
        ).copy()
        self.angular_velocity_body = np.asarray(
            self.angular_velocity_body,
            dtype=np.float64,
        ).copy()

        if self.position_ned.shape != (3,):
            raise ValueError("NED position must have shape (3,).")

        if self.velocity_ned.shape != (3,):
            raise ValueError("NED velocity must have shape (3,).")

        if self.attitude_q_b_n.shape != (4,):
            raise ValueError("Attitude quaternion must have shape (4,).")

        if self.angular_velocity_body.shape != (3,):
            raise ValueError("Body angular velocity must have shape (3,).")

        if not np.all(np.isfinite(self.position_ned)):
            raise ValueError("NED position must contain only finite values.")

        if not np.all(np.isfinite(self.velocity_ned)):
            raise ValueError("NED velocity must contain only finite values.")

        if not np.all(np.isfinite(self.attitude_q_b_n)):
            raise ValueError("Attitude quaternion must contain only finite values.")

        if not np.all(np.isfinite(self.angular_velocity_body)):
            raise ValueError("Body angular velocity must contain only finite values.")

        quaternion_norm = np.linalg.norm(self.attitude_q_b_n)

        if not np.isclose(
            quaternion_norm,
            1.0,
            rtol=1e-9,
            atol=1e-12,
        ):
            raise ValueError("Attitude quaternion must have unit norm.")
