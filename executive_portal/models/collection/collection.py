"""
executive_portal/models/collection/collection.py

Executive Collection Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase


@dataclass(frozen=True)
class CollectionReference(PortalBase):
    """Reference to a collection item."""
    collection_id: str = ""
    ref_id: str = ""
    ref_type: str = ""
    ref_source: str = ""
    added_by: str = ""
    order: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "collection_id": self.collection_id,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
            "added_by": self.added_by,
            "order": self.order,
        })
        return base


@dataclass(frozen=True)
class CollectionHistory(PortalBase):
    """Collection history entry."""
    collection_id: str = ""
    action: str = ""
    actor: str = ""
    ref_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "collection_id": self.collection_id,
            "action": self.action,
            "actor": self.actor,
            "ref_id": self.ref_id,
        })
        return base


@dataclass(frozen=True)
class CollectionMetadata(PortalBase):
    """Collection metadata."""
    collection_id: str = ""
    classification: str = "unclassified"
    tlp: str = "amber"
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "collection_id": self.collection_id,
            "classification": self.classification,
            "tlp": self.tlp,
            "tags": list(self.tags),
        })
        return base


@dataclass(frozen=True)
class ExecutiveCollection(PortalBase):
    """
    Executive Collection - REFERENCE ONLY.
    
    IMPORTANT: Collections contain REFERENCES only.
    They NEVER duplicate data.
    """
    name: str = ""
    description: str = ""
    owner: str = ""
    collection_type: str = "general"
    status: str = "active"
    references: tuple[CollectionReference, ...] = field(default_factory=tuple)
    metadata: CollectionMetadata = None
    parent_collection_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "collection_type": self.collection_type,
            "status": self.status,
            "references": [r.to_dict() for r in self.references],
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "parent_collection_id": self.parent_collection_id,
        })
        return base
