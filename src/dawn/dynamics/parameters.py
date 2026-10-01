"""Physical parameters for DAWN rigid-body dynamics."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class VehicleParameters:
    """Physical parameters of the rigid-body vehicle model.

    Attributes:
        mass: Constant vehicle mass [kg].
        inertia_body: Constant inertia tensor about the center of mass, expressed
            in the FRD body frame [kg m^2].

    The inertia array is copied and validated at construction. Direct field
    mutation is not revalidated. Symmetry and positive definiteness establish
    numerical admissibility, not physical realizability of vehicle parameters.
    """

    mass: float
    inertia_body: NDArray[np.float64]

    def __post_init__(self) -> None:
        """Validate and normalize vehicle parameters."""
        self.mass = float(self.mass)
        self.inertia_body = np.asarray(
            self.inertia_body,
            dtype=np.float64,
        ).copy()

        if not np.isfinite(self.mass):
            raise ValueError("Vehicle mass must be finite.")

        if self.mass <= 0.0:
            raise ValueError("Vehicle mass must be greater than zero.")

        if self.inertia_body.shape != (3, 3):
            raise ValueError("Inertia tensor must have shape (3, 3).")

        if not np.all(np.isfinite(self.inertia_body)):
            raise ValueError("Inertia tensor must contain only finite values.")

        if not np.allclose(
            self.inertia_body,
            self.inertia_body.T,
            rtol=1e-10,
            atol=1e-12,
        ):
            raise ValueError("Inertia tensor must be symmetric.")

        principal_moments = np.linalg.eigvalsh(self.inertia_body)

        if np.any(principal_moments <= 0.0):
            raise ValueError("Inertia tensor must be positive definite.")
