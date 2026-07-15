from __future__ import annotations

"""
knowledge/graph/repository/__init__.py

Repository implementations for the Knowledge Layer.
"""
from knowledge.graph.repository.base import KnowledgeRepository
from knowledge.graph.repository.graph_repository import GraphRepository
from knowledge.graph.repository.entity_repository import EntityRepository
from knowledge.graph.repository.identity_repository import IdentityRepository
from knowledge.graph.repository.relationship_repository import RelationshipRepository
from knowledge.graph.repository.evidence_repository import EvidenceRepository

__all__ = [
    "KnowledgeRepository",
    "GraphRepository",
    "EntityRepository",
    "IdentityRepository",
    "RelationshipRepository",
    "EvidenceRepository",
]
