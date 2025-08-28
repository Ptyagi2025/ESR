"""Fitting utilities for tunneling junction models."""

from __future__ import annotations

from typing import Callable, Tuple

import numpy as np
from scipy.optimize import curve_fit

from . import models


def fit_model(
    V: np.ndarray, J: np.ndarray, model: Callable[..., np.ndarray], p0: Tuple[float, ...]
) -> Tuple[np.ndarray, np.ndarray]:
    """Fit a model to data using non-linear least squares.

    Parameters
    ----------
    V, J:
        Voltage and current density arrays.
    model:
        Callable returning the model current density for a voltage array
        followed by its parameters.
    p0:
        Initial guess for parameters.

    Returns
    -------
    popt, pcov:
        Optimized parameters and covariance matrix from ``curve_fit``.
    """

    popt, pcov = curve_fit(model, V, J, p0=p0, maxfev=20000)
    return popt, pcov


def fit_simmons(V: np.ndarray, J: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fit the Simmons model to data."""

    p0 = (1.0, 1.0)  # barrier height (eV), thickness (nm)
    return fit_model(V, J, models.simmons_current_density, p0)


def fit_bdr(V: np.ndarray, J: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fit the Brinkman–Dynes–Rowell model to data."""

    p0 = (1.0, 1.0, 0.0)  # avg height, thickness, asymmetry
    return fit_model(V, J, models.bdr_current_density, p0)


__all__ = ["fit_simmons", "fit_bdr", "fit_model"]
