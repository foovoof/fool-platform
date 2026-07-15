"""
domain/common/__init__.py

Shared value types for the FOOL Platform domain layer.
Mirrors contracts/common/common-defs.schema.json field-for-field.

Domain Purity: standard library only. No platform, intelligence, ai, data,
infrastructure, security, apps, connectors, or tools imports.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, FrozenSet, Sequence
from uuid import UUID, uuid4


class ClassificationLevelValue(str, Enum):
    """Sensitivity classification of a domain object."""
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"


class Status(str, Enum):
    """Canonical lifecycle status shared by case/investigation/report style objects."""
    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    ARCHIVED = "archived"
    RETRACTED = "retracted"


class ConfidenceLevel(str, Enum):
    """Human-interpretable confidence bucket derived from a confidence score."""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass(frozen=True)
class Reference:
    """A pointer from one domain object to another by id and type."""
    ref_id: str
    ref_type: str
    ref_version: str | None = None


def make_reference(ref_id: str, ref_type: str, ref_version: str | None = None) -> Reference:
    """Factory function to create a Reference."""
    return Reference(ref_id=ref_id, ref_type=ref_type, ref_version=ref_version)


@dataclass(frozen=True)
class Provenance:
    """Origin, lineage, and custody trail attached to any information-bearing object."""
    origin: str
    recorded_at: str
    lineage: FrozenSet[str] = field(default_factory=frozenset)
    custody_refs: FrozenSet[Reference] = field(default_factory=frozenset)
    source_refs: FrozenSet[Reference] = field(default_factory=frozenset)


def create_provenance(
    origin: str,
    recorded_at: str | None = None,
    lineage: Sequence[str] | None = None,
    custody_refs: Sequence[Reference] | None = None,
    source_refs: Sequence[Reference] | None = None,
) -> Provenance:
    """Factory function to create a Provenance object."""
    if not origin or not origin.strip():
        raise ValueError("Provenance.origin must not be empty: no domain object may be anonymous.")
    return Provenance(
        origin=origin,
        recorded_at=recorded_at or utc_now(),
        lineage=frozenset(lineage) if lineage else frozenset(),
        custody_refs=frozenset(custody_refs) if custody_refs else frozenset(),
        source_refs=frozenset(source_refs) if source_refs else frozenset(),
    )


Metadata = dict[str, Any]
"""Open key/value bag for non-canonical, extension-owned attributes."""

EMPTY_METADATA: Metadata = {}


def freeze_tags(tags: Sequence[str] | None = None) -> FrozenSet[str]:
    """Freeze a sequence of tags into an immutable frozenset."""
    if not tags:
        return frozenset()
    return frozenset(set(tags))


def freeze_refs(refs: Sequence[Reference] | None = None) -> FrozenSet[Reference]:
    """Freeze a sequence of references into an immutable frozenset."""
    if not refs:
        return frozenset()
    return frozenset(refs)


def new_id() -> str:
    """Generate a new canonical identifier for a domain object."""
    return str(uuid4())


def utc_now() -> str:
    """Produce a timezone-aware ISO 8601 timestamp for 'now'."""
    return datetime.now(timezone.utc).isoformat()


class DomainInvariantError(Exception):
    """Raised when a domain invariant is violated during pure, local construction."""
    pass


__all__ = [
    "ClassificationLevelValue",
    "ConfidenceLevel",
    "DomainInvariantError",
    "EMPTY_METADATA",
    "freeze_refs",
    "freeze_tags",
    "make_reference",
    "Metadata",
    "new_id",
    "Provenance",
    "Reference",
    "Status",
    "utc_now",
    "create_provenance",
]
