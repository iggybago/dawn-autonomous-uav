"""Quaternion utilities for DAWN flight dynamics."""

import numpy as np
from numpy.typing import NDArray


def quaternion_multiply(
    q1: NDArray[np.float64],
    q2: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute the Hamilton product of two scalar-first quaternions.

    Quaternion convention:
        q = [w, x, y, z]

    Args:
        q1: First quaternion.
        q2: Second quaternion.

    Returns:
        Hamilton product q1 ⊗ q2.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ],
        dtype=np.float64,
    )


def quaternion_to_rotation_matrix(
    q_b_n: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Return the body-to-NED rotation matrix for a unit quaternion.

    The quaternion is scalar-first [w, x, y, z] and represents the
    orientation of the FRD body frame relative to the NED navigation frame.

    The returned matrix satisfies:

        vector_ned = R_b_n @ vector_body

    Args:
        q_b_n: Unit body-to-NED attitude quaternion.

    Returns:
        3x3 body-to-NED rotation matrix.
    """
    w, x, y, z = q_b_n

    return np.array(
        [
            [
                1.0 - 2.0 * (y * y + z * z),
                2.0 * (x * y - w * z),
                2.0 * (x * z + w * y),
            ],
            [
                2.0 * (x * y + w * z),
                1.0 - 2.0 * (x * x + z * z),
                2.0 * (y * z - w * x),
            ],
            [
                2.0 * (x * z - w * y),
                2.0 * (y * z + w * x),
                1.0 - 2.0 * (x * x + y * y),
            ],
        ],
        dtype=np.float64,
    )


def quaternion_derivative(
    q_b_n: NDArray[np.float64],
    angular_velocity_body: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute attitude quaternion derivative from body angular velocity.

    Args:
        q_b_n: Body-to-NED attitude quaternion [w, x, y, z].
        angular_velocity_body: Body angular velocity [p, q, r] [rad/s].

    Returns:
        Quaternion derivative [1/s].
    """
    omega_quaternion = np.array(
        [
            0.0,
            angular_velocity_body[0],
            angular_velocity_body[1],
            angular_velocity_body[2],
        ],
        dtype=np.float64,
    )

    return 0.5 * quaternion_multiply(q_b_n, omega_quaternion)
