"""Physical models for tunneling junctions.

This module provides current density equations for the Simmons and
Brinkman–Dynes–Rowell (BDR) models.  These implementations are highly
simplified; the goal is to provide a clear API rather than
research-grade accuracy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class CurrentDensityModel(Protocol):
    """Protocol for models that compute current density.

    Subclasses implement ``__call__`` to return the current density for a
    given voltage array ``V`` and model parameters.  Parameters are stored
    in dataclasses for clarity.
    """

    def __call__(self, V: np.ndarray, *params: float) -> np.ndarray:
        """Return current density for voltage ``V``."""


@dataclass
class SimmonsParams:
    """Parameters for the Simmons model."""

    barrier_height: float  # eV
    barrier_thickness: float  # nm


def simmons_current_density(V: np.ndarray, barrier_height: float, barrier_thickness: float) -> np.ndarray:
    """Simplified Simmons current density.

    The full Simmons equation is rather involved.  For architecture
    demonstration purposes we use a toy exponential expression that still
    depends on the barrier height and thickness.
    """

    A = 1e5  # pre-factor (arbitrary)
    B = 10.0  # decay constant (arbitrary)
    effective = np.maximum(barrier_height - V / 2.0, 0)
    return A * V * np.exp(-B * barrier_thickness * np.sqrt(effective))


@dataclass
class BDRParams:
    """Parameters for the Brinkman–Dynes–Rowell model."""

    avg_barrier_height: float  # eV
    barrier_thickness: float  # nm
    asymmetry: float  # eV


def bdr_current_density(
    V: np.ndarray, avg_barrier_height: float, barrier_thickness: float, asymmetry: float
) -> np.ndarray:
    """Simplified BDR current density.

    Again we employ a simplified expression capturing the essential
    parameter dependencies.
    """

    A = 1e5
    B = 10.0
    effective = np.maximum(avg_barrier_height + asymmetry * V, 0)
    return A * V * np.exp(-B * barrier_thickness * np.sqrt(effective))


# The names exported by this module
__all__ = [
    "SimmonsParams",
    "simmons_current_density",
    "BDRParams",
    "bdr_current_density",
]
