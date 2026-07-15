from __future__ import annotations

"""
knowledge/inference/explanation/__init__.py

Explanation Engine for Inference.

Provides explanation generation for inference results.
"""
from knowledge.inference.explanation.explanation_model import Explanation
from knowledge.inference.explanation.explanation_generator import ExplanationGenerator

__all__ = [
    "Explanation",
    "ExplanationGenerator",
]
