"""
domain/chain_of_custody.py

ChainOfCustody domain model - tamper-evident custody trail.
Mirrors contracts/domain/chain-of-custody.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from typing import Sequence

from .common import (
    EMPTY_METADATA,
    Metadata,
    Reference,
    new_id,
    utc_now,
)


@dataclass(frozen=True)
class CustodyEntry:
    """
    A single entry in a chain of custody record.
    
    Each entry records who took custody, when, and why.
    """
    entry_id: str
    timestamp: str
    custodian: str
    action: str
    reason: str | None
    verified: bool = False
    verification_method: str | None = None


@dataclass(frozen=True)
class ChainOfCustody:
    """
    ChainOfCustody provides a tamper-evident trail of evidence custody.
    
    Per the Provenance Everywhere principle, Evidence carries a complete
    chain of custody recording every custodian who touched the evidence.
    """
    id: str
    created_at: str
    updated_at: str
    evidence_ref: Reference
    entries: tuple[CustodyEntry, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        evidence_ref: Reference,
        initial_custodian: str,
        reason: str | None = None,
        entries: Sequence[CustodyEntry] | None = None,
        metadata: Metadata | None = None,
    ) -> "ChainOfCustody":
        """Create a new ChainOfCustody with an initial entry."""
        timestamp = utc_now()
        initial_entry = CustodyEntry(
            entry_id=new_id(),
            timestamp=timestamp,
            custodian=initial_custodian,
            action="created",
            reason=reason,
            verified=True,
            verification_method="initial_creation",
        )
        all_entries = (initial_entry,)
        if entries:
            all_entries = (*all_entries, *entries)
        
        return cls(
            id=new_id(),
            created_at=timestamp,
            updated_at=timestamp,
            evidence_ref=evidence_ref,
            entries=all_entries,
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_custody_transfer(
        self,
        new_custodian: str,
        reason: str,
        verified: bool = False,
        verification_method: str | None = None,
    ) -> "ChainOfCustody":
        """Return a new ChainOfCustody with a custody transfer entry."""
        entry = CustodyEntry(
            entry_id=new_id(),
            timestamp=utc_now(),
            custodian=new_custodian,
            action="transferred",
            reason=reason,
            verified=verified,
            verification_method=verification_method,
        )
        return ChainOfCustody(
            id=self.id,
            created_at=self.created_at,
            updated_at=utc_now(),
            evidence_ref=self.evidence_ref,
            entries=(*self.entries, entry),
            metadata=self.metadata,
        )

    def last_custodian(self) -> str | None:
        """Return the custodian from the most recent entry, if any."""
        if not self.entries:
            return None
        return self.entries[-1].custodian


__all__ = [
    "ChainOfCustody",
    "CustodyEntry",
]
