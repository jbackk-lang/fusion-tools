"""
timdr - Time-Domain Reduction (TIMDR) tools for fusion signal analysis.

Provides filtering and visualization utilities for processing
fusion diagnostic time-series data.
"""

from .timdr_filter import TimdrFilter
from .timdr_visualization import TimdrVisualizer

__all__ = ["TimdrFilter", "TimdrVisualizer"]
