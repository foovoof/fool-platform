from __future__ import annotations

"""
knowledge/inference/__init__.py

Deterministic Inference Foundation for the Knowledge Layer.

This module provides rule-based inference capabilities for FOOL Platform.

IMPORTANT: This is Phase 3B. This does NOT implement:
- Intelligence Runtime
- Planning
- Goal Selection
- Strategy Generation
- Autonomous Reasoning
- AI/LLM

The inference engine ONLY:
- Evaluates rules against knowledge
- Derives new facts deterministically
- Generates explainable conclusions
- Produces recommendations (NOT decisions)
"""
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.engine.inference_result import (
    InferenceResult,
    InferenceConclusion,
)
from knowledge.inference.engine.inference_engine import InferenceEngine

__all__ = [
    "InferenceSession",
    "InferenceResult",
    "InferenceConclusion",
    "InferenceEngine",
]
