"""
model_j - Model-J disruption detector for fusion plasma diagnostics.

Provides a rule-based and threshold-driven disruption precursor detector
inspired by the J-invariant classification approach used in fusion research.
"""

from .model_j_detector import ModelJDetector

__all__ = ["ModelJDetector"]
