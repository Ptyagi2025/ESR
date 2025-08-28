"""Data loading utilities."""

from __future__ import annotations

import pandas as pd


def load_iv_csv(path: str) -> pd.DataFrame:
    """Load I–V or J–V data from a CSV file.

    The CSV is expected to contain two columns labeled ``V`` for voltage
    and ``I`` or ``J`` for current or current density.  Additional columns
    are ignored but preserved in the returned :class:`~pandas.DataFrame`.
    """

    df = pd.read_csv(path)
    return df


__all__ = ["load_iv_csv"]
