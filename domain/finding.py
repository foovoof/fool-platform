"""
domain/finding.py

Finding domain model - synthesized assessment from evidence analysis.
Mirrors contracts/domain/finding.schema.json field-for-field.
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


class FindingType(str, Enum):
    """Types of findings synthesized from evidence."""
    IDENTITY_LINK = "identity_link"
    RELATIONSHIP = "relationship"
    PATTERN = "pattern"
    ANOMALY = "anomaly"
    THREAT_INDICATOR = "threat_indicator"
    ATTRIBUTION = "attribution"
    TIMELINE_EVENT = "timeline_event"
    ASSESSMENT = "assessment"
    OTHER = "other"


class Severity(str, Enum):
    """Severity level of a finding."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Finding:
    """
    Finding is a synthesized assessment from evidence analysis.
    
    Findings provide reasoning chains connecting Evidence to conclusions,
    with full confidence scoring.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    finding_type: FindingType
    title: str
    summary: str
    status: Status
    classification: ClassificationLevel
    confidence: ConfidenceScore
    provenance: Provenance
    evidence_refs: frozenset = field(default_factory=frozenset)
    entity_refs: frozenset = field(default_factory=frozenset)
    identity_refs: frozenset = field(default_factory=frozenset)
    severity: Severity | None = None
    reasoning_chain: list[str] = field(default_factory=list)
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        finding_type: FindingType,
        title: str,
        summary: str,
        confidence: ConfidenceScore,
        provenance: Provenance,
        evidence_refs: list[Reference] | None = None,
        entity_refs: list[Reference] | None = None,
        identity_refs: list[Reference] | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        severity: Severity | None = None,
        reasoning_chain: list[str] | None = None,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Finding":
        """Create a new Finding."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            finding_type=finding_type,
            title=title,
            summary=summary,
            status=status,
            classification=ClassificationLevel(classification),
            confidence=confidence,
            provenance=provenance,
            evidence_refs=frozenset(evidence_refs) if evidence_refs else frozenset(),
            entity_refs=frozenset(entity_refs) if entity_refs else frozenset(),
            identity_refs=frozenset(identity_refs) if identity_refs else frozenset(),
            severity=severity,
            reasoning_chain=reasoning_chain or [],
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )


__all__ = [
    "Finding",
    "FindingType",
    "Severity",
]
