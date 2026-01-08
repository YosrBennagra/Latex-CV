"""
Validation Package
==================

CV validation, tone checking, and hallucination detection.
"""

from .validator import CVValidator
from .hallucination import HallucinationDetector

__all__ = ["CVValidator", "HallucinationDetector"]
