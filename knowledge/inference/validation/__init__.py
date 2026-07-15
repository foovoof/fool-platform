from __future__ import annotations

"""
knowledge/inference/validation/__init__.py

Validation for Inference Engine.

Provides validation for rules, inference results, and consistency.
"""
from knowledge.inference.validation.inference_validator import (
    InferenceValidator,
    InferenceValidationResult,
)
from knowledge.inference.validation.rule_consistency_validator import (
    RuleConsistencyValidator,
    ConsistencyResult,
)

__all__ = [
    "InferenceValidator",
    "InferenceValidationResult",
    "RuleConsistencyValidator",
    "ConsistencyResult",
]
