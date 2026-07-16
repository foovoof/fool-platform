"""
threat_intelligence/campaigns/models/assertion.py

Campaign Assertion Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import (
    CampaignBase,
    Auditable,
    Explainable,
    Versionable,
    ConfidenceMixin,
)


@dataclass(frozen=True)
class CampaignAssertion(CampaignBase, Auditable, Explainable, Versionable, ConfidenceMixin):
    """Campaign assertion."""
    campaign_id: str = ""
    assertion_type: str = ""
    assertion: str = ""
    status: str = "pending"
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    supporting_assertions: tuple[str, ...] = field(default_factory=tuple)
    contradicting_assertions: tuple[str, ...] = field(default_factory=tuple)
    confidence_explanation: str = ""
    confidence_score: float = 0.5
    confidence_level: str = "medium"
    source: str = ""
    source_url: str = ""
    validated: bool = False
    validated_by: str = ""
    validated_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "assertion_type": self.assertion_type,
            "assertion": self.assertion,
            "status": self.status,
            "evidence_ids": list(self.evidence_ids),
            "supporting_assertions": list(self.supporting_assertions),
            "contradicting_assertions": list(self.contradicting_assertions),
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "source": self.source,
            "source_url": self.source_url,
            "validated": self.validated,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "explanation": self.explanation,
            "reasoning": self.reasoning,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class AssertionRevision(CampaignBase):
    """Assertion revision history."""
    assertion_id: str = ""
    revision_number: int = 1
    previous_assertion: str = ""
    changes: str = ""
    changed_by: str = ""
    change_reason: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "assertion_id": self.assertion_id,
            "revision_number": self.revision_number,
            "previous_assertion": self.previous_assertion,
            "changes": self.changes,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
        })
        return base
