"""
Data formatting helpers for Cricbuzz LiveStats UI and visualizations.
"""

from typing import Union, Optional
from datetime import datetime


def format_runs(runs: Union[int, float, None]) -> str:
    """Formats runs with comma separation (e.g. 12,450)."""
    if runs is None:
        return "0"
    return f"{int(runs):,}"


def format_strike_rate(sr: Union[float, int, None]) -> str:
    """Formats strike rate to 2 decimal places."""
    if sr is None or sr == 0:
        return "0.00"
    return f"{float(sr):.2f}"


def format_economy(econ: Union[float, int, None]) -> str:
    """Formats economy rate to 2 decimal places."""
    if econ is None or econ == 0:
        return "0.00"
    return f"{float(econ):.2f}"


def format_date(dt: Union[str, datetime, None]) -> str:
    """Formats dates to 'DD MMM YYYY' format."""
    if not dt:
        return "N/A"
    if isinstance(dt, str):
        try:
            parsed = datetime.strptime(dt[:10], "%Y-%m-%d")
            return parsed.strftime("%d %b %Y")
        except ValueError:
            return dt
    return dt.strftime("%d %b %Y")


def format_percentage(pct: Union[float, int, None]) -> str:
    """Formats float as percentage string."""
    if pct is None:
        return "0.0%"
    return f"{float(pct):.1f}%"
