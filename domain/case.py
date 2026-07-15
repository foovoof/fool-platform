"""
domain/case.py

Case domain model - container for related investigations.
Mirrors contracts/domain/case.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum

from .classification_level import ClassificationLevel, ClassificationLevelValue
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


class CasePriority(str, Enum):
    """Priority levels for cases."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Case:
    """
    Case is a container for related investigations.
    
    Per the Human Accountability principle, every Case has a named
    human owner and requires human review for closure.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    title: str
    description: str
    status: Status
    classification: ClassificationLevel
    priority: CasePriority
    owner: str
    investigation_refs: frozenset = field(default_factory=frozenset)
    report_refs: frozenset = field(default_factory=frozenset)
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        owner: str,
        provenance: Provenance,
        investigation_refs: list[Reference] | None = None,
        report_refs: list[Reference] | None = None,
        status: Status = Status.DRAFT,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        priority: CasePriority = CasePriority.MEDIUM,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Case":
        """Create a new Case."""
        if not owner or not owner.strip():
            raise ValueError("Case.owner must not be empty: every case requires a human owner.")
        
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            title=title,
            description=description,
            status=status,
            classification=ClassificationLevel(classification),
            priority=priority,
            owner=owner,
            investigation_refs=frozenset(investigation_refs) if investigation_refs else frozenset(),
            report_refs=frozenset(report_refs) if report_refs else frozenset(),
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_investigation_ref(self, ref: Reference) -> "Case":
        """Return a new Case with the given investigation reference added."""
        if ref in self.investigation_refs:
            return self
        return Case(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            title=self.title,
            description=self.description,
            status=self.status,
            classification=self.classification,
            priority=self.priority,
            owner=self.owner,
            investigation_refs=self.investigation_refs | {ref},
            report_refs=self.report_refs,
            tags=self.tags,
            metadata=self.metadata,
        )

    def with_report_ref(self, ref: Reference) -> "Case":
        """Return a new Case with the given report reference added."""
        if ref in self.report_refs:
            return self
        return Case(
            id=self.id,
            version=self.version,
            created_at=self.created_at,
            updated_at=utc_now(),
            title=self.title,
            description=self.description,
            status=self.status,
            classification=self.classification,
            priority=self.priority,
            owner=self.owner,
            investigation_refs=self.investigation_refs,
            report_refs=self.report_refs | {ref},
            tags=self.tags,
            metadata=self.metadata,
        )


__all__ = [
    "Case",
    "CasePriority",
]
