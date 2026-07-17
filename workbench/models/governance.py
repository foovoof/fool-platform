"""
workbench/models/governance.py

Governance Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workbench.models.base import (
    WorkbenchBase,
    Auditable,
)


@dataclass(frozen=True)
class Reviewer:
    """Reviewer information."""
    user_id: str = ""
    name: str = ""
    email: str = ""
    role: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }


@dataclass(frozen=True)
class ReviewCycle(WorkbenchBase, Auditable):
    """Review cycle for products."""
    product_id: str = ""
    status: str = "pending"
    reviewers: tuple[Reviewer, ...] = field(default_factory=tuple)
    started_at: str = ""
    completed_at: str = ""
    review_notes: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "status": self.status,
            "reviewers": [r.to_dict() for r in self.reviewers],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "review_notes": self.review_notes,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ApprovalRecord(WorkbenchBase, Auditable):
    """Approval workflow record."""
    product_id: str = ""
    approval_type: str = ""
    status: str = "pending"
    approver: Reviewer = None
    decision_at: str = ""
    decision_notes: str = ""
    approval_chain: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "approval_type": self.approval_type,
            "status": self.status,
            "approver": self.approver.to_dict() if self.approver else None,
            "decision_at": self.decision_at,
            "decision_notes": self.decision_notes,
            "approval_chain": list(self.approval_chain),
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ApprovalWorkflow(WorkbenchBase):
    """Approval workflow definition."""
    name: str = ""
    description: str = ""
    required_approvals: int = 1
    approver_roles: tuple[str, ...] = field(default_factory=tuple)
    approval_steps: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "required_approvals": self.required_approvals,
            "approver_roles": list(self.approver_roles),
            "approval_steps": list(self.approval_steps),
        })
        return base


@dataclass(frozen=True)
class PublicationHistory(WorkbenchBase):
    """Publication history entry."""
    product_id: str = ""
    publication_id: str = ""
    status: str = ""
    published_at: str = ""
    published_by: str = ""
    withdrawn_at: str = ""
    withdrawn_by: str = ""
    withdrawal_reason: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "publication_id": self.publication_id,
            "status": self.status,
            "published_at": self.published_at,
            "published_by": self.published_by,
            "withdrawn_at": self.withdrawn_at,
            "withdrawn_by": self.withdrawn_by,
            "withdrawal_reason": self.withdrawal_reason,
        })
        return base


@dataclass(frozen=True)
class Publication(WorkbenchBase, Auditable):
    """Publication governance."""
    product_id: str = ""
    status: str = "draft"
    published_at: str = ""
    published_by: str = ""
    publication_channels: tuple[str, ...] = field(default_factory=tuple)
    access_level: str = "restricted"
    history: tuple[PublicationHistory, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "status": self.status,
            "published_at": self.published_at,
            "published_by": self.published_by,
            "publication_channels": list(self.publication_channels),
            "access_level": self.access_level,
            "history": [h.to_dict() for h in self.history],
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class SourceAssessment(WorkbenchBase, Auditable):
    """Source reliability assessment - HUMAN GOVERNANCED ONLY."""
    source_id: str = ""
    source_name: str = ""
    reliability: str = "c"
    reliability_notes: str = ""
    confidence_in_source: str = "medium"
    assessment_notes: str = ""
    assessor: Reviewer = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "source_id": self.source_id,
            "source_name": self.source_name,
            "reliability": self.reliability,
            "reliability_notes": self.reliability_notes,
            "confidence_in_source": self.confidence_in_source,
            "assessment_notes": self.assessment_notes,
            "assessor": self.assessor.to_dict() if self.assessor else None,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ConfidenceReview(WorkbenchBase, Auditable):
    """Confidence review - HUMAN GOVERNANCED ONLY."""
    product_id: str = ""
    assertion_id: str = ""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    review_notes: str = ""
    reviewer: Reviewer = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "assertion_id": self.assertion_id,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "review_notes": self.review_notes,
            "reviewer": self.reviewer.to_dict() if self.reviewer else None,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class GovernanceDecision(WorkbenchBase, Auditable):
    """Governance decision record."""
    product_id: str = ""
    decision_type: str = ""
    decision: str = ""
    decision_made_by: Reviewer = None
    decision_at: str = ""
    decision_notes: str = ""
    conditions: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "decision_type": self.decision_type,
            "decision": self.decision,
            "decision_made_by": self.decision_made_by.to_dict() if self.decision_made_by else None,
            "decision_at": self.decision_at,
            "decision_notes": self.decision_notes,
            "conditions": list(self.conditions),
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class PublicationPolicy(WorkbenchBase):
    """Publication policy definition."""
    name: str = ""
    description: str = ""
    required_reviews: int = 1
    required_approvals: int = 1
    allowed_tlp: tuple[str, ...] = field(default_factory=tuple)
    approval_workflow_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "required_reviews": self.required_reviews,
            "required_approvals": self.required_approvals,
            "allowed_tlp": list(self.allowed_tlp),
            "approval_workflow_id": self.approval_workflow_id,
        })
        return base
