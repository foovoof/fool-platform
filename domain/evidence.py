"""
domain/evidence.py

Evidence domain model - collected information with chain of custody.
Mirrors contracts/domain/evidence.schema.json field-for-field.
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
    freeze_refs,
    new_id,
    utc_now,
)


class EvidenceType(str, Enum):
    """Types of evidence that can be collected."""
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    DATA = "data"
    RECORD = "record"
    LOG = "log"
    METADATA = "metadata"
    OTHER = "other"


@dataclass(frozen=True)
class Evidence:
    """
    Evidence is collected information with chain of custody tracking.
    
    Evidence is the raw material of investigations, always traceable
    to a Source and carrying full provenance.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    evidence_type: EvidenceType
    content: str
    source_ref: Reference
    status: Status
    classification: ClassificationLevel
    confidence: ConfidenceScore
    provenance: Provenance
    collected_at: str
    chain_of_custody: list[Reference] = field(default_factory=list)
    entity_refs: frozenset = field(default_factory=frozenset)
    identity_refs: frozenset = field(default_factory=frozenset)
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        evidence_type: EvidenceType,
        content: str,
        source_ref: Reference,
        confidence: ConfidenceScore,
        provenance: Provenance,
        collected_at: str | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        chain_of_custody: list[Reference] | None = None,
        entity_refs: list[Reference] | None = None,
        identity_refs: list[Reference] | None = None,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Evidence":
        """Create new Evidence."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            evidence_type=evidence_type,
            content=content,
            source_ref=source_ref,
            status=status,
            classification=ClassificationLevel(classification),
            confidence=confidence,
            provenance=provenance,
            collected_at=collected_at or timestamp,
            chain_of_custody=chain_of_custody or [],
            entity_refs=frozenset(entity_refs) if entity_refs else frozenset(),
            identity_refs=frozenset(identity_refs) if identity_refs else frozenset(),
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_chain_entry(self, entry: Reference) -> "Evidence":
        """Return new Evidence with a chain of custody entry."""
        return Evidence(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            evidence_type=self.evidence_type,
            content=self.content,
            source_ref=self.source_ref,
            status=self.status,
            classification=self.classification,
            confidence=self.confidence,
            provenance=self.provenance,
            collected_at=self.collected_at,
            chain_of_custody=[*self.chain_of_custody, entry],
            entity_refs=self.entity_refs,
            identity_refs=self.identity_refs,
            tags=self.tags,
            metadata=self.metadata,
        )


__all__ = [
    "Evidence",
    "EvidenceType",
]
