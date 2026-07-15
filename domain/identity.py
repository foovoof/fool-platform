"""
domain/identity.py

Identity is the central aggregation point of the FOOL Platform domain model.
It resolves a set of observable identifiers into a single subject of interest.
Mirrors contracts/domain/identity.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet, Sequence

from .classification_level import ClassificationLevel, ClassificationLevelValue
from .confidence_score import ConfidenceScore, ConfidenceLevel, ConfidenceMethods
from .common import (



    DomainInvariantError,
    EMPTY_METADATA,
    Metadata,
    Provenance,
    Reference,
    Status,
    freeze_refs,
    freeze_tags,
    new_id,
    utc_now,
    create_provenance,
)


class IdentifierType(str, Enum):
    """Types of observable identifiers."""
    EMAIL = "email"
    PHONE = "phone"
    USERNAME = "username"
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    HASH = "hash"
    WALLET_ADDRESS = "wallet_address"
    DOCUMENT = "document"
    IMAGE = "image"
    PERSON_NAME = "person_name"
    OTHER = "other"


@dataclass(frozen=True)
class Identifier:
    """An observable identifier resolved to belong to an Identity."""
    identifier_type: IdentifierType
    value: str
    confidence: ConfidenceScore
    source_refs: FrozenSet[Reference] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Identity:
    """
    Identity is an immutable aggregate of resolved identifiers.
    
    Identity is the central aggregation point of the FOOL Platform domain model.
    Every identifier, entity, evidence item, and finding either references an
    Identity directly or reaches one transitively.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    status: Status
    classification: ClassificationLevel
    provenance: Provenance
    identifiers: tuple[Identifier, ...]
    display_label: str | None = None
    entity_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    evidence_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    confidence: ConfidenceScore | None = None
    tags: FrozenSet[str] = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    def __post_init__(self) -> None:
        if len(self.identifiers) == 0:
            raise DomainInvariantError(
                "Identity must be created with at least one identifier."
            )

    @classmethod
    def create(
        cls,
        identifiers: Sequence[Identifier],
        provenance: Provenance,
        display_label: str | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        entity_refs: Sequence[Reference] | None = None,
        evidence_refs: Sequence[Reference] | None = None,
        confidence: ConfidenceScore | None = None,
        tags: Sequence[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Identity":
        """
        Create a new Identity.
        
        Args:
            identifiers: At least one identifier to resolve to this identity
            provenance: Origin and lineage of this identity
            display_label: Optional human-readable label
            status: Lifecycle status (default: active)
            classification: Classification level (default: internal)
            entity_refs: Optional references to linked entities
            evidence_refs: Optional references to supporting evidence
            confidence: Optional overall confidence score
            tags: Optional tags for categorization
            metadata: Optional extension attributes
        """
        if len(identifiers) == 0:
            raise DomainInvariantError(
                "Identity must be created with at least one identifier."
            )
        
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            status=status,
            classification=ClassificationLevel(classification),
            provenance=provenance,
            identifiers=tuple(identifiers),
            display_label=display_label,
            entity_refs=frozenset(entity_refs) if entity_refs else frozenset(),
            evidence_refs=frozenset(evidence_refs) if evidence_refs else frozenset(),
            confidence=confidence,
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_identifier(self, identifier: Identifier) -> "Identity":
        """Return a new Identity with the given identifier appended."""
        return Identity(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            status=self.status,
            classification=self.classification,
            provenance=self.provenance,
            identifiers=(*self.identifiers, identifier),
            display_label=self.display_label,
            entity_refs=self.entity_refs,
            evidence_refs=self.evidence_refs,
            confidence=self.confidence,
            tags=self.tags,
            metadata=self.metadata,
        )

    def with_entity_ref(self, entity_ref: Reference) -> "Identity":
        """Return a new Identity linked to the given Entity reference."""
        if entity_ref in self.entity_refs:
            return self
        return Identity(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            status=self.status,
            classification=self.classification,
            provenance=self.provenance,
            identifiers=self.identifiers,
            display_label=self.display_label,
            entity_refs=self.entity_refs | {entity_ref},
            evidence_refs=self.evidence_refs,
            confidence=self.confidence,
            tags=self.tags,
            metadata=self.metadata,
        )

    def has_identifier_value(self, value: str) -> bool:
        """Check if this identity has an identifier with the given value."""
        return any(identifier.value == value for identifier in self.identifiers)


def open_identity(
    origin: str,
    identifiers: Sequence[Identifier],
    display_label: str | None = None,
    status: Status = Status.ACTIVE,
    classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
    entity_refs: Sequence[Reference] | None = None,
    evidence_refs: Sequence[Reference] | None = None,
    confidence: ConfidenceScore | None = None,
    tags: Sequence[str] | None = None,
    metadata: Metadata | None = None,
) -> Identity:
    """
    Convenience factory to open a new identity with provenance from an origin.
    """
    return Identity.create(
        identifiers=identifiers,
        provenance=create_provenance(origin),
        display_label=display_label,
        status=status,
        classification=classification,
        entity_refs=entity_refs,
        evidence_refs=evidence_refs,
        confidence=confidence,
        tags=tags,
        metadata=metadata,
    )


__all__ = [
    "Identifier",
    "IdentifierType",
    "Identity",
    "open_identity",
]
