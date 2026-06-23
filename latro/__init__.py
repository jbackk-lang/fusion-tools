"""
latro - Localization and Anomaly Tracking (LATRO) for fusion diagnostics.

Provides core analysis algorithms and feature extraction tools to identify
and localize anomalous events in fusion experiment time-series data.
"""

from .latro_core import LatroCore
from .latro_features import LatroFeatures

__all__ = ["LatroCore", "LatroFeatures"]
