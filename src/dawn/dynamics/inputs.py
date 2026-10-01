"""Input definitions for DAWN rigid-body dynamics."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class ForcesMoments:
    """External non-gravitational forces and moments applied to the vehicle.

    Conventions:
        - Force is expressed in the FRD body frame [N].
        - Moment is about the center of mass, expressed in FRD [N m].
        - Gravity is not included in force_body.

    Arrays are copied and validated at construction. Direct field mutation
    remains possible and is not revalidated; callers must preserve validity.
    """

    force_body: NDArray[np.float64]
    moment_body: NDArray[np.float64]

    def __post_init__(self) -> None:
        """Validate and normalize force and moment vectors."""
        self.force_body = np.asarray(
            self.force_body,
            dtype=np.float64,
        ).copy()
        self.moment_body = np.asarray(
            self.moment_body,
            dtype=np.float64,
        ).copy()

        if self.force_body.shape != (3,):
            raise ValueError("Body force must have shape (3,).")

        if self.moment_body.shape != (3,):
            raise ValueError("Body moment must have shape (3,).")

        if not np.all(np.isfinite(self.force_body)):
            raise ValueError("Body force must contain only finite values.")

        if not np.all(np.isfinite(self.moment_body)):
            raise ValueError("Body moment must contain only finite values.")
