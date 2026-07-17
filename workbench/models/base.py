"""
workbench/models/base.py

Workbench Base Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class WorkbenchBase:
    """Base class for workbench entities."""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    modified_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "version": self.version,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class Auditable:
    """Mixin for auditable entities."""
    author: str = ""
    reason: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "author": self.author,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Versionable:
    """Mixin for versionable entities."""
    revision_history: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_history": list(self.revision_history),
        }


@dataclass(frozen=True)
class ProvenanceMixin:
    """Mixin for provenance tracking."""
    provenance_source: str = ""
    provenance_url: str = ""
    collected_at: str = ""
    collected_by: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance_source": self.provenance_source,
            "provenance_url": self.provenance_url,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
        }


@dataclass(frozen=True)
class ReferenceOnly:
    """Mixin for reference-only entities."""
    ref_id: str = ""
    ref_type: str = ""
    ref_source: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        }
