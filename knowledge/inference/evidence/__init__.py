from __future__ import annotations

"""
knowledge/inference/evidence/__init__.py

Evidence Propagation for Inference Engine.

Provides evidence tracking, chain building, and propagation.
"""
from knowledge.inference.evidence.evidence_tracker import (
    Evidence,
    EvidenceTracker,
    EvidenceType,
)
from knowledge.inference.evidence.evidence_chain import EvidenceChain, EvidenceChainBuilder
from knowledge.inference.evidence.evidence_propagation import EvidencePropagation

__all__ = [
    "Evidence",
    "EvidenceType",
    "EvidenceTracker",
    "EvidenceChain",
    "EvidenceChainBuilder",
    "EvidencePropagation",
]
