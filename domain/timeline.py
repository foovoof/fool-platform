"""
domain/timeline.py

Timeline domain model - ordered sequence of events.
Mirrors contracts/domain/timeline.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from typing import Sequence

from .common import (
    EMPTY_METADATA,
    Metadata,
    Provenance,
    Reference,
    new_id,
    utc_now,
)


@dataclass(frozen=True)
class TimelineEntry:
    """A single entry in a timeline."""
    timestamp: str
    event_type: str
    description: str
    actor: str | None
    evidence_refs: tuple[Reference, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))


@dataclass(frozen=True)
class Timeline:
    """
    Timeline represents an ordered sequence of events.
    
    Timelines provide chronological context for investigations,
    tracking when things happened and in what sequence.
    """
    id: str
    created_at: str
    updated_at: str
    title: str
    provenance: Provenance
    entries: tuple[TimelineEntry, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        title: str,
        provenance: Provenance,
        entries: Sequence[TimelineEntry] | None = None,
        metadata: Metadata | None = None,
    ) -> "Timeline":
        """Create a new Timeline."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            created_at=timestamp,
            updated_at=timestamp,
            title=title,
            provenance=provenance,
            entries=tuple(entries) if entries else tuple(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_entry(self, entry: TimelineEntry) -> "Timeline":
        """Return a new Timeline with the given entry appended."""
        return Timeline(
            id=self.id,
            created_at=self.created_at,
            updated_at=utc_now(),
            title=self.title,
            provenance=self.provenance,
            entries=(*self.entries, entry),
            metadata=self.metadata,
        )

    def sorted(self) -> "Timeline":
        """Return a new Timeline with entries sorted by timestamp."""
        sorted_entries = tuple(
            sorted(self.entries, key=lambda e: e.timestamp)
        )
        return Timeline(
            id=self.id,
            created_at=self.created_at,
            updated_at=utc_now(),
            title=self.title,
            provenance=self.provenance,
            entries=sorted_entries,
            metadata=self.metadata,
        )


__all__ = [
    "Timeline",
    "TimelineEntry",
]
