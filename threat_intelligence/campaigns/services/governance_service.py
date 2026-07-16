"""
threat_intelligence/campaigns/services/governance_service.py

Governance Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import Approval, Review, AuditEntry, AuditTrail
from threat_intelligence.campaigns.repositories import ApprovalRepository, ReviewRepository, AuditEntryRepository


class GovernanceService:
    """Service for campaign governance."""
    
    def __init__(
        self,
        approval_repository: ApprovalRepository | None = None,
        review_repository: ReviewRepository | None = None,
        audit_repository: AuditEntryRepository | None = None,
    ) -> None:
        self._approval_repository = approval_repository or ApprovalRepository()
        self._review_repository = review_repository or ReviewRepository()
        self._audit_repository = audit_repository or AuditEntryRepository()
        self._audit_trails: dict[str, AuditTrail] = {}
    
    def create_approval(
        self,
        campaign_id: str,
        approval_type: str,
        author: str = "",
        **kwargs: Any,
    ) -> Approval:
        """Create a new approval."""
        approval = Approval(
            id=str(uuid4()),
            campaign_id=campaign_id,
            approval_type=approval_type,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        self._add_audit_entry(campaign_id, "approval_created", approval.to_dict())
        return self._approval_repository.create(approval)
    
    def approve(
        self,
        approval_id: str,
        approver: str,
        comments: str = "",
    ) -> Approval | None:
        """Approve a pending approval."""
        approval = self._approval_repository.get(approval_id)
        if not approval:
            return None
        
        updated = Approval(
            id=approval.id,
            campaign_id=approval.campaign_id,
            approval_type=approval.approval_type,
            status="approved",
            approver=approver,
            approved_at=datetime.now(timezone.utc).isoformat(),
            comments=comments,
            created_at=approval.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=approval.created_by,
            modified_by=approver,
            version=approval.version + 1,
            metadata=approval.metadata,
            author=approval.author,
            reason=approval.reason,
        )
        self._add_audit_entry(approval.campaign_id, "approval_approved", updated.to_dict())
        return self._approval_repository.update(updated)
    
    def reject(
        self,
        approval_id: str,
        approver: str,
        rejection_reason: str = "",
    ) -> Approval | None:
        """Reject a pending approval."""
        approval = self._approval_repository.get(approval_id)
        if not approval:
            return None
        
        updated = Approval(
            id=approval.id,
            campaign_id=approval.campaign_id,
            approval_type=approval.approval_type,
            status="rejected",
            approver=approver,
            approved_at=datetime.now(timezone.utc).isoformat(),
            rejection_reason=rejection_reason,
            created_at=approval.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=approval.created_by,
            modified_by=approver,
            version=approval.version + 1,
            metadata=approval.metadata,
            author=approval.author,
            reason=approval.reason,
        )
        self._add_audit_entry(approval.campaign_id, "approval_rejected", updated.to_dict())
        return self._approval_repository.update(updated)
    
    def create_review(
        self,
        campaign_id: str,
        review_type: str,
        author: str = "",
        **kwargs: Any,
    ) -> Review:
        """Create a new review."""
        review = Review(
            id=str(uuid4()),
            campaign_id=campaign_id,
            review_type=review_type,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        self._add_audit_entry(campaign_id, "review_created", review.to_dict())
        return self._review_repository.create(review)
    
    def complete_review(
        self,
        review_id: str,
        reviewer: str,
        findings: str = "",
        recommendations: str = "",
    ) -> Review | None:
        """Complete a review."""
        review = self._review_repository.get(review_id)
        if not review:
            return None
        
        updated = Review(
            id=review.id,
            campaign_id=review.campaign_id,
            review_type=review.review_type,
            status="completed",
            reviewer=reviewer,
            reviewed_at=datetime.now(timezone.utc).isoformat(),
            findings=findings,
            recommendations=recommendations,
            created_at=review.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=review.created_by,
            modified_by=reviewer,
            version=review.version + 1,
            metadata=review.metadata,
            author=review.author,
            reason=review.reason,
        )
        self._add_audit_entry(review.campaign_id, "review_completed", updated.to_dict())
        return self._review_repository.update(updated)
    
    def _add_audit_entry(
        self,
        campaign_id: str,
        action: str,
        entity_data: dict[str, Any],
    ) -> None:
        """Add an audit entry."""
        entry = AuditEntry(
            id=str(uuid4()),
            campaign_id=campaign_id,
            action=action,
            entity_type=entity_data.get("type", "unknown"),
            entity_id=entity_data.get("id", ""),
            new_state=entity_data,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )
        self._audit_repository.create(entry)
        
        if campaign_id not in self._audit_trails:
            self._audit_trails[campaign_id] = AuditTrail(
                campaign_id=campaign_id,
            )
        
        trail = self._audit_trails[campaign_id]
        self._audit_trails[campaign_id] = AuditTrail(
            campaign_id=campaign_id,
            entries=trail.entries + (entry.to_dict(),),
        )
    
    def get_audit_trail(self, campaign_id: str) -> AuditTrail | None:
        """Get audit trail for campaign."""
        return self._audit_trails.get(campaign_id)
    
    def find_approvals_by_campaign(self, campaign_id: str) -> list[Approval]:
        """Find approvals by campaign."""
        return self._approval_repository.search({"campaign_id": campaign_id})
    
    def find_reviews_by_campaign(self, campaign_id: str) -> list[Review]:
        """Find reviews by campaign."""
        return self._review_repository.search({"campaign_id": campaign_id})
