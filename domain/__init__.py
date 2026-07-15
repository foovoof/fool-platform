"""
domain/__init__.py

FOOL Platform Domain Layer.

This package implements the canonical domain models in Python,
mirroring the contracts defined in contracts/domain/*.schema.json.

Domain Purity: standard library only. No platform, intelligence, ai, data,
infrastructure, security, apps, connectors, or tools imports.

Canonical Source of Truth:
- Standards define semantics.
- Contracts define interoperability.
- Implementations conform to contracts.
"""

from .annotation import Annotation, AnnotationType
from .case import Case, CasePriority
from .chain_of_custody import ChainOfCustody, CustodyEntry
from .classification_level import ClassificationLevel
from .common import (
    ClassificationLevelValue,
    ConfidenceLevel,
    DomainInvariantError,
    EMPTY_METADATA,
    Metadata,
    Provenance,
    Reference,
    Status,
    create_provenance,
    freeze_refs,
    freeze_tags,
    make_reference,
    new_id,
    utc_now,
)
from .confidence_score import (
    ConfidenceLevel,
    ConfidenceMethod,
    ConfidenceMethods,
    ConfidenceScore,
)
from .entity import Entity, EntityAttributes, EntityType
from .event import Event, EventType
from .evidence import Evidence, EvidenceType
from .finding import Finding, FindingType, Severity
from .identity import Identity, Identifier, IdentifierType, open_identity
from .investigation import Investigation, InvestigationType
from .relationship import Relationship, RelationshipType
from .report import Report, ReportSection, ReportType
from .source import Source, SourceReliability, SourceType
from .timeline import Timeline, TimelineEntry

__all__ = [
    # Common
    "ClassificationLevel",
    "ClassificationLevelValue",
    "ConfidenceLevel",
    "DomainInvariantError",
    "EMPTY_METADATA",
    "Metadata",
    "Provenance",
    "Reference",
    "Status",
    "create_provenance",
    "freeze_refs",
    "freeze_tags",
    "make_reference",
    "new_id",
    "utc_now",
    # Annotation
    "Annotation",
    "AnnotationType",
    # Case
    "Case",
    "CasePriority",
    # Chain of Custody
    "ChainOfCustody",
    "CustodyEntry",
    # Classification Level
    "ClassificationLevel",
    # Confidence Score
    "ConfidenceMethod",
    "ConfidenceMethods",
    "ConfidenceScore",
    # Entity
    "Entity",
    "EntityAttributes",
    "EntityType",
    # Event
    "Event",
    "EventType",
    # Evidence
    "Evidence",
    "EvidenceType",
    # Finding
    "Finding",
    "FindingType",
    "Severity",
    # Identity
    "Identity",
    "Identifier",
    "IdentifierType",
    "open_identity",
    # Investigation
    "Investigation",
    "InvestigationType",
    # Relationship
    "Relationship",
    "RelationshipType",
    # Report
    "Report",
    "ReportSection",
    "ReportType",
    # Source
    "Source",
    "SourceReliability",
    "SourceType",
    # Timeline
    "Timeline",
    "TimelineEntry",
]
