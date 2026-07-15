"""
domain/source.py

Source domain model - origin of collected evidence.
Mirrors contracts/domain/source.schema.json field-for-field.
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


class SourceType(str, Enum):
    """Types of sources for collected evidence."""
    WEB = "web"
    API = "api"
    DATABASE = "database"
    DOCUMENT = "document"
    USER_INPUT = "user_input"
    AUTOMATED = "automated"
    FEED = "feed"
    OTHER = "other"


class SourceReliability(str, Enum):
    """Reliability rating for a source."""
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass(frozen=True)
class Source:
    """
    Source is the origin of collected evidence.
    
    Every Evidence item traces back to a Source, which carries
    provenance and reliability metadata.
    """
    id: str
    version: str
    created_at: str
    updated_at: str
    source_type: SourceType
    name: str
    url: str | None
    status: Status
    classification: ClassificationLevel
    reliability: SourceReliability
    collected_at: str
    collected_by: str
    contact_info: str | None
    provenance: Provenance
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        source_type: SourceType,
        name: str,
        collected_by: str,
        provenance: Provenance,
        collected_at: str | None = None,
        url: str | None = None,
        status: Status = Status.ACTIVE,
        classification: ClassificationLevelValue = ClassificationLevelValue.INTERNAL,
        reliability: SourceReliability = SourceReliability.UNKNOWN,
        contact_info: str | None = None,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Source":
        """Create a new Source."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            created_at=timestamp,
            updated_at=timestamp,
            source_type=source_type,
            name=name,
            url=url,
            status=status,
            classification=ClassificationLevel(classification),
            reliability=reliability,
            collected_at=collected_at or timestamp,
            collected_by=collected_by,
            contact_info=contact_info,
            provenance=provenance,
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )


__all__ = [
    "Source",
    "SourceReliability",
    "SourceType",
]
