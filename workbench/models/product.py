"""
workbench/models/product.py

Product Governance Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workbench.models.base import (
    WorkbenchBase,
    Auditable,
    Versionable,
    ProvenanceMixin,
    ReferenceOnly,
)


@dataclass(frozen=True)
class AssertionReference(WorkbenchBase, ReferenceOnly, ProvenanceMixin):
    """Reference to platform assertion - NEVER duplicated."""
    product_id: str = ""
    assertion_id: str = ""
    assertion_ref: str = ""
    source_system: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "assertion_id": self.assertion_id,
            "assertion_ref": self.assertion_ref,
            "source_system": self.source_system,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
            "provenance_source": self.provenance_source,
            "provenance_url": self.provenance_url,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
        })
        return base


@dataclass(frozen=True)
class EvidencePackageReference(WorkbenchBase, ReferenceOnly, ProvenanceMixin):
    """Reference to platform evidence package - NEVER duplicated."""
    product_id: str = ""
    evidence_id: str = ""
    evidence_ref: str = ""
    source_system: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "evidence_id": self.evidence_id,
            "evidence_ref": self.evidence_ref,
            "source_system": self.source_system,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
            "provenance_source": self.provenance_source,
            "provenance_url": self.provenance_url,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
        })
        return base


@dataclass(frozen=True)
class KnowledgeReference(WorkbenchBase, ReferenceOnly):
    """Reference to platform knowledge entity - NEVER duplicated."""
    product_id: str = ""
    knowledge_id: str = ""
    knowledge_ref: str = ""
    source_system: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "knowledge_id": self.knowledge_id,
            "knowledge_ref": self.knowledge_ref,
            "source_system": self.source_system,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class ProductVersion(WorkbenchBase, Auditable):
    """Product version history."""
    product_id: str = ""
    version_number: int = 1
    changes: str = ""
    changes_summary: str = ""
    previous_version_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "version_number": self.version_number,
            "changes": self.changes,
            "changes_summary": self.changes_summary,
            "previous_version_id": self.previous_version_id,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ProductHistory(WorkbenchBase):
    """Product history entry."""
    product_id: str = ""
    action: str = ""
    actor: str = ""
    previous_state: dict[str, Any] = field(default_factory=dict)
    new_state: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "action": self.action,
            "actor": self.actor,
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class IntelligenceProduct(WorkbenchBase, Auditable, Versionable):
    """
    Intelligence Product Governance Wrapper.
    
    IMPORTANT: This model references platform intelligence products.
    It NEVER owns or duplicates them.
    """
    product_type: str = ""
    title: str = ""
    description: str = ""
    status: str = "draft"
    owner: str = ""
    assertion_refs: tuple[AssertionReference, ...] = field(default_factory=tuple)
    evidence_refs: tuple[EvidencePackageReference, ...] = field(default_factory=tuple)
    knowledge_refs: tuple[KnowledgeReference, ...] = field(default_factory=tuple)
    collection_ids: tuple[str, ...] = field(default_factory=tuple)
    review_cycle_id: str = ""
    publication_id: str = ""
    superseded_by_id: str = ""
    parent_product_id: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    classification: str = ""
    tlp: str = "amber"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_type": self.product_type,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "owner": self.owner,
            "assertion_refs": [r.to_dict() for r in self.assertion_refs],
            "evidence_refs": [r.to_dict() for r in self.evidence_refs],
            "knowledge_refs": [r.to_dict() for r in self.knowledge_refs],
            "collection_ids": list(self.collection_ids),
            "review_cycle_id": self.review_cycle_id,
            "publication_id": self.publication_id,
            "superseded_by_id": self.superseded_by_id,
            "parent_product_id": self.parent_product_id,
            "tags": list(self.tags),
            "classification": self.classification,
            "tlp": self.tlp,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class IntelligenceCollection(WorkbenchBase, Auditable, Versionable):
    """
    Intelligence Collection Governance.
    
    Collections contain REFERENCES only - never duplicated content.
    """
    name: str = ""
    description: str = ""
    owner: str = ""
    status: str = "active"
    product_refs: tuple[str, ...] = field(default_factory=tuple)
    collection_policy: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "status": self.status,
            "product_refs": list(self.product_refs),
            "collection_policy": self.collection_policy,
            "author": self.author,
            "reason": self.reason,
        })
        return base
