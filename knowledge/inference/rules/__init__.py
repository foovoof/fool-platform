from __future__ import annotations

"""
knowledge/inference/rules/__init__.py

Rule Foundation for Inference.

Provides rule registration, validation, and evaluation.
"""
from knowledge.inference.rules.rule_registry import (
    Rule,
    RuleCondition,
    RuleOutput,
    RuleRegistry,
    ConditionType,
    OutputType,
)
from knowledge.inference.rules.rule_validator import RuleValidator
from knowledge.inference.rules.rule_evaluator import RuleEvaluator, EvaluationContext
from knowledge.inference.rules.rule_execution import RuleExecutor, ExecutionContext

__all__ = [
    "Rule",
    "RuleCondition",
    "RuleOutput",
    "RuleRegistry",
    "ConditionType",
    "OutputType",
    "RuleValidator",
    "RuleEvaluator",
    "EvaluationContext",
    "RuleExecutor",
    "ExecutionContext",
]
