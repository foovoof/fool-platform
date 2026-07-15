"""
domain/investigation.py

Investigation domain model - structured inquiry into a subject.
Mirrors contracts/domain/investigation.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

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


class InvestigationType(str, Enum):
    """Types of investigations."""
    OSINT = "osint"
    HUMINT = "humint"
    TECHNICAL = "technical"
    FORENSIC = "forensic"
    COMBINED = "combined"
    OTHER = "other"


@dataclass(frozen=True)
class Investigation:
    """
    Investigation is a structured inquiry into a subject.
    
    Investigations aggregate evidence, findings, and timelines
    focused on a specific subject or question.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    investigation_type: InvestigationType
    title: str
    objective: str
    status: Status
    classification: ClassificationLevel
    owner: str
    identity_ref: Reference | None = None
    subject_description: str | None = None
    scope: str | None = None
    findings_refs: frozenset = field(default_factory=frozenset)
    evidence_refs: frozenset = field(default_factory=frozenset)
    timeline_ref: Reference | None = None
    workflow_ref: Reference | None = None
    confidence: ConfidenceScore | None = None
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        investigation_type: InvestigationType,
        title: str,
        objective: str,
        owner: str,
        provenance: Provenance,
        identity_ref: Reference | None = None,
        subject_description: str | None = None,
        scope: str | None = None,
        status: Status = Status.DRAFT,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        findings_refs: Sequence[Reference] | None = None,
        evidence_refs: Sequence[Reference] | None = None,
        timeline_ref: Reference | None = None,
        workflow_ref: Reference | None = None,
        confidence: ConfidenceScore | None = None,
        tags: Sequence[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Investigation":
        """Create a new Investigation."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            investigation_type=investigation_type,
            title=title,
            objective=objective,
            status=status,
            classification=ClassificationLevel(classification),
            owner=owner,
            identity_ref=identity_ref,
            subject_description=subject_description,
            scope=scope,
            findings_refs=frozenset(findings_refs) if findings_refs else frozenset(),
            evidence_refs=frozenset(evidence_refs) if evidence_refs else frozenset(),
            timeline_ref=timeline_ref,
            workflow_ref=workflow_ref,
            confidence=confidence,
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_finding_ref(self, ref: Reference) -> "Investigation":
        """Return a new Investigation with the given finding reference added."""
        if ref in self.findings_refs:
            return self
        return Investigation(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            investigation_type=self.investigation_type,
            title=self.title,
            objective=self.objective,
            status=self.status,
            classification=self.classification,
            owner=self.owner,
            identity_ref=self.identity_ref,
            subject_description=self.subject_description,
            scope=self.scope,
            findings_refs=self.findings_refs | {ref},
            evidence_refs=self.evidence_refs,
            timeline_ref=self.timeline_ref,
            workflow_ref=self.workflow_ref,
            confidence=self.confidence,
            tags=self.tags,
            metadata=self.metadata,
        )

    def with_evidence_ref(self, ref: Reference) -> "Investigation":
        """Return a new Investigation with the given evidence reference added."""
        if ref in self.evidence_refs:
            return self
        return Investigation(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            investigation_type=self.investigation_type,
            title=self.title,
            objective=self.objective,
            status=self.status,
            classification=self.classification,
            owner=self.owner,
            identity_ref=self.identity_ref,
            subject_description=self.subject_description,
            scope=self.scope,
            findings_refs=self.findings_refs,
            evidence_refs=self.evidence_refs | {ref},
            timeline_ref=self.timeline_ref,
            workflow_ref=self.workflow_ref,
            confidence=self.confidence,
            tags=self.tags,
            metadata=self.metadata,
        )


__all__ = [
    "Investigation",
    "InvestigationType",
]
