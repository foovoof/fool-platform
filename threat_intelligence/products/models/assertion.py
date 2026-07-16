"""
threat_intelligence/products/models/assertion.py

Product Assertion and Evidence Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.products.models.base import (
    ProductBase,
    Auditable,
    ConfidenceMixin,
    ProvenanceMixin,
    Versionable,
)


@dataclass(frozen=True)
class ProductAssertion(ProductBase, Auditable, ConfidenceMixin, Versionable, ProvenanceMixin):
    """Product assertion."""
    product_id: str = ""
    assertion_type: str = ""
    assertion: str = ""
    status: str = "pending"
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    supporting_assertions: tuple[str, ...] = field(default_factory=tuple)
    contradicting_assertions: tuple[str, ...] = field(default_factory=tuple)
    validated: bool = False
    validated_by: str = ""
    validated_at: str = ""
    review_status: str = "pending"
    reviewed_by: str = ""
    reviewed_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "assertion_type": self.assertion_type,
            "assertion": self.assertion,
            "status": self.status,
            "evidence_refs": list(self.evidence_refs),
            "supporting_assertions": list(self.supporting_assertions),
            "contradicting_assertions": list(self.contradicting_assertions),
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "validated": self.validated,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "review_status": self.review_status,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
            "source_url": self.source_url,
        })
        return base


@dataclass(frozen=True)
class ProductEvidence(ProductBase, Auditable, ConfidenceMixin, ProvenanceMixin):
    """Product evidence."""
    product_id: str = ""
    assertion_id: str = ""
    evidence_type: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    content_type: str = ""
    source: str = ""
    source_url: str = ""
    assertion_ids: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "assertion_id": self.assertion_id,
            "evidence_type": self.evidence_type,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "content_type": self.content_type,
            "source": self.source,
            "source_url": self.source_url,
            "assertion_ids": list(self.assertion_ids),
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ProductConfidence(ProductBase):
    """Product confidence binding."""
    product_id: str = ""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    confidence_explanation: str = ""
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    assertion_refs: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "evidence_refs": list(self.evidence_refs),
            "assertion_refs": list(self.assertion_refs),
        })
        return base


@dataclass(frozen=True)
class ProductProvenance(ProductBase):
    """Product provenance."""
    product_id: str = ""
    source_type: str = ""
    source_id: str = ""
    source_description: str = ""
    collection_method: str = ""
    collected_at: str = ""
    collected_by: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "source_description": self.source_description,
            "collection_method": self.collection_method,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
        })
        return base


@dataclass(frozen=True)
class ProductVersion(ProductBase):
    """Product version."""
    product_id: str = ""
    version_number: int = 1
    changes: str = ""
    changes_summary: str = ""
    changed_by: str = ""
    change_reason: str = ""
    previous_version_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "version_number": self.version_number,
            "changes": self.changes,
            "changes_summary": self.changes_summary,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "previous_version_id": self.previous_version_id,
        })
        return base


@dataclass(frozen=True)
class ProductHistory(ProductBase):
    """Product version history."""
    product_id: str = ""
    versions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    total_revisions: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "versions": list(self.versions),
            "total_revisions": self.total_revisions,
        })
        return base


@dataclass(frozen=True)
class LifecycleTransition(ProductBase):
    """Lifecycle transition."""
    product_id: str = ""
    from_status: str = ""
    to_status: str = ""
    reason: str = ""
    transitioned_by: str = ""
    approval_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "reason": self.reason,
            "transitioned_by": self.transitioned_by,
            "approval_id": self.approval_id,
        })
        return base


@dataclass(frozen=True)
class LifecycleState(ProductBase):
    """Current lifecycle state."""
    product_id: str = ""
    status: str = "draft"
    transitions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    last_reviewed: str = ""
    next_review: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "status": self.status,
            "transitions": list(self.transitions),
            "last_reviewed": self.last_reviewed,
            "next_review": self.next_review,
        })
        return base


@dataclass(frozen=True)
class ApprovalRecord(ProductBase):
    """Approval record."""
    product_id: str = ""
    approver: str = ""
    approval_status: str = ""
    approval_notes: str = ""
    approval_timestamp: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "approver": self.approver,
            "approval_status": self.approval_status,
            "approval_notes": self.approval_notes,
            "approval_timestamp": self.approval_timestamp,
        })
        return base
