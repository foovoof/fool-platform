from __future__ import annotations

"""
knowledge/resolution/__init__.py

Resolution implementations for the Knowledge Layer.

Provides deterministic resolution for entities, identities, and relationships.
"""
from knowledge.resolution.entity_resolution import (
    EntityResolutionEngine,
    EntityMatch,
    EntityMatchType,
    MatchExplanation,
)
from knowledge.resolution.identity_resolution import (
    IdentityResolutionEngine,
    IdentityMatch,
    IdentityMatchType,
)
from knowledge.resolution.relationship_resolution import (
    RelationshipResolutionEngine,
    RelationshipMatch,
    RelationshipMatchType,
)
from knowledge.resolution.deduplication import (
    DeduplicationEngine,
    DuplicateCandidate,
    DuplicateGroup,
)

__all__ = [
    "EntityResolutionEngine",
    "EntityMatch",
    "EntityMatchType",
    "MatchExplanation",
    "IdentityResolutionEngine",
    "IdentityMatch",
    "IdentityMatchType",
    "RelationshipResolutionEngine",
    "RelationshipMatch",
    "RelationshipMatchType",
    "DeduplicationEngine",
    "DuplicateCandidate",
    "DuplicateGroup",
]
