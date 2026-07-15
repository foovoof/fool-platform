"""
domain/report.py

Report domain model - human-reviewable synthesis of investigation findings.
Mirrors contracts/domain/report.schema.json field-for-field.
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


class ReportType(str, Enum):
    """Types of reports."""
    SUMMARY = "summary"
    DETAILED = "detailed"
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    LEGAL = "legal"
    THREAT_INTELLIGENCE = "threat_intelligence"
    INVESTIGATION = "investigation"
    OTHER = "other"


@dataclass(frozen=True)
class ReportSection:
    """A section within a report."""
    section_id: str
    title: str
    content: str
    order: int


@dataclass(frozen=True)
class Report:
    """
    Report is a human-reviewable synthesis of investigation findings.
    
    Per the Human Accountability principle, every Report requires a
    recorded human reviewed_by before it can reach active (published) status.
    The platform assists; it never publishes a report on its own authority.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    report_type: ReportType
    title: str
    summary: str
    status: Status
    classification: ClassificationLevel
    provenance: Provenance
    case_ref: Reference | None = None
    investigation_ref: Reference | None = None
    finding_refs: frozenset = field(default_factory=frozenset)
    sections: tuple[ReportSection, ...] = field(default_factory=tuple)
    confidence: ConfidenceScore | None = None
    author: str | None = None
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    published_at: str | None = None
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        report_type: ReportType,
        title: str,
        summary: str,
        provenance: Provenance,
        finding_refs: Sequence[Reference] | None = None,
        sections: Sequence[ReportSection] | None = None,
        case_ref: Reference | None = None,
        investigation_ref: Reference | None = None,
        status: Status = Status.DRAFT,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        confidence: ConfidenceScore | None = None,
        author: str | None = None,
        tags: Sequence[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Report":
        """Create a new Report."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            report_type=report_type,
            title=title,
            summary=summary,
            status=status,
            classification=ClassificationLevel(classification),
            provenance=provenance,
            case_ref=case_ref,
            investigation_ref=investigation_ref,
            finding_refs=frozenset(finding_refs) if finding_refs else frozenset(),
            sections=tuple(sections) if sections else tuple(),
            confidence=confidence,
            author=author,
            reviewed_by=None,
            reviewed_at=None,
            published_at=None,
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def submit_for_review(self, author: str) -> "Report":
        """Return a new Report submitted for review."""
        if self.status != Status.DRAFT:
            raise ValueError("Only draft reports can be submitted for review.")
        return Report(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            report_type=self.report_type,
            title=self.title,
            summary=self.summary,
            status=Status.UNDER_REVIEW,
            classification=self.classification,
            provenance=self.provenance,
            case_ref=self.case_ref,
            investigation_ref=self.investigation_ref,
            finding_refs=self.finding_refs,
            sections=self.sections,
            confidence=self.confidence,
            author=author,
            reviewed_by=None,
            reviewed_at=None,
            published_at=None,
            tags=self.tags,
            metadata=self.metadata,
        )

    def approve(self, reviewer: str) -> "Report":
        """Return a new Report approved by the reviewer."""
        if self.status != Status.UNDER_REVIEW:
            raise ValueError("Only reports under review can be approved.")
        return Report(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            report_type=self.report_type,
            title=self.title,
            summary=self.summary,
            status=Status.ACTIVE,
            classification=self.classification,
            provenance=self.provenance,
            case_ref=self.case_ref,
            investigation_ref=self.investigation_ref,
            finding_refs=self.finding_refs,
            sections=self.sections,
            confidence=self.confidence,
            author=self.author,
            reviewed_by=reviewer,
            reviewed_at=utc_now(),
            published_at=utc_now(),
            tags=self.tags,
            metadata=self.metadata,
        )

    def requires_review(self) -> bool:
        """Returns True if this report requires human review before publication."""
        return self.reviewed_by is None


__all__ = [
    "Report",
    "ReportSection",
    "ReportType",
]
