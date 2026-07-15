"""
domain/entity.py

Entity domain model - a distinguishable thing of interest in an investigation.
Mirrors contracts/domain/entity.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Sequence

from .classification_level import ClassificationLevel, ClassificationLevelValue
from .confidence_score import ConfidenceScore
from .common import (
    DomainInvariantError,
    EMPTY_METADATA,
    Metadata,
    Provenance,
    Reference,
    Status,
    new_id,
    utc_now,
)


class EntityType(str, Enum):
    """Types of entities that can be distinguished in investigations."""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DEVICE = "device"
    ACCOUNT = "account"
    SERVICE = "service"
    CONTENT = "content"
    EVENT = "event"
    CONCEPT = "concept"
    OTHER = "other"


@dataclass(frozen=True)
class EntityAttributes:
    """Optional typed attributes for an entity."""
    attributes: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Entity:
    """
    Entity is a distinguishable thing of interest in an investigation.
    
    Entities are linked to Identities and can be referenced by Evidence,
    Findings, and other Entities.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    entity_type: EntityType
    name: str
    status: Status
    classification: ClassificationLevel
    provenance: Provenance
    identity_ref: Reference | None = None
    evidence_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    finding_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    relationship_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    confidence: ConfidenceScore | None = None
    attributes: EntityAttributes = field(default_factory=EntityAttributes)
    tags: FrozenSet[str] = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        entity_type: EntityType,
        name: str,
        provenance: Provenance,
        identity_ref: Reference | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        evidence_refs: Sequence[Reference] | None = None,
        finding_refs: Sequence[Reference] | None = None,
        relationship_refs: Sequence[Reference] | None = None,
        confidence: ConfidenceScore | None = None,
        attributes: dict | None = None,
        tags: Sequence[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Entity":
        """Create a new Entity."""
        if not name or not name.strip():
            raise DomainInvariantError("Entity.name must not be empty.")
        
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            entity_type=entity_type,
            name=name,
            status=status,
            classification=ClassificationLevel(classification),
            identity_ref=identity_ref,
            evidence_refs=frozenset(evidence_refs) if evidence_refs else frozenset(),
            finding_refs=frozenset(finding_refs) if finding_refs else frozenset(),
            relationship_refs=frozenset(relationship_refs) if relationship_refs else frozenset(),
            confidence=confidence,
            provenance=provenance,
            attributes=EntityAttributes(attributes) if attributes else EntityAttributes(),
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_evidence_ref(self, ref: Reference) -> "Entity":
        """Return a new Entity with the given evidence reference added."""
        if ref in self.evidence_refs:
            return self
        return Entity(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            entity_type=self.entity_type,
            name=self.name,
            status=self.status,
            classification=self.classification,
            identity_ref=self.identity_ref,
            evidence_refs=self.evidence_refs | {ref},
            finding_refs=self.finding_refs,
            relationship_refs=self.relationship_refs,
            confidence=self.confidence,
            provenance=self.provenance,
            attributes=self.attributes,
            tags=self.tags,
            metadata=self.metadata,
        )


__all__ = [
    "Entity",
    "EntityAttributes",
    "EntityType",
]
