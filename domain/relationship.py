"""
domain/relationship.py

Relationship domain model - connections between entities.
Mirrors contracts/domain/relationship.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum

from .classification_level import ClassificationLevel, ClassificationLevelValue
from .confidence_score import ConfidenceScore, ConfidenceLevel, ConfidenceMethods
from .common import (



    EMPTY_METADATA,
    Metadata,
    Provenance,
    Reference,
    Status,
    new_id,
    utc_now,
)


class RelationshipType(str, Enum):
    """Types of relationships between entities."""
    OWNS = "owns"
    CONTROLS = "controls"
    ASSOCIATED_WITH = "associated_with"
    LOCATED_AT = "located_at"
    WORKS_FOR = "works_for"
    COMMUNICATES_WITH = "communicates_with"
    TRANSACTS_WITH = "transacts_with"
    HOSTS = "hosts"
    AUTHORED = "authored"
    REFERENCES = "references"
    SIMILAR_TO = "similar_to"
    CONFLICTS_WITH = "conflicts_with"
    OTHER = "other"


@dataclass(frozen=True)
class Relationship:
    """
    Relationship represents a connection between entities.
    
    Relationships carry confidence scores and provenance,
    supporting graph analysis of connected entities.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    relationship_type: RelationshipType
    source_ref: Reference
    target_ref: Reference
    status: Status
    classification: ClassificationLevel
    confidence: ConfidenceScore
    provenance: Provenance
    evidence_refs: frozenset = field(default_factory=frozenset)
    properties: dict = field(default_factory=dict)
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        relationship_type: RelationshipType,
        source_ref: Reference,
        target_ref: Reference,
        confidence: ConfidenceScore,
        provenance: Provenance,
        evidence_refs: list[Reference] | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        properties: dict | None = None,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Relationship":
        """Create a new Relationship."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            relationship_type=relationship_type,
            source_ref=source_ref,
            target_ref=target_ref,
            status=status,
            classification=ClassificationLevel(classification),
            confidence=confidence,
            provenance=provenance,
            evidence_refs=frozenset(evidence_refs) if evidence_refs else frozenset(),
            properties=properties or {},
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )


__all__ = [
    "Relationship",
    "RelationshipType",
]
