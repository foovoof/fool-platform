"""
threat_intelligence/campaigns/models/evidence.py

Campaign Evidence Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase, Auditable, ConfidenceMixin


@dataclass(frozen=True)
class CampaignEvidence(CampaignBase, Auditable, ConfidenceMixin):
    """Campaign evidence."""
    campaign_id: str = ""
    evidence_type: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    content_type: str = ""
    source: str = ""
    source_url: str = ""
    collected_at: str = ""
    collected_by: str = ""
    assertion_ids: tuple[str, ...] = field(default_factory=tuple)
    indicator_ids: tuple[str, ...] = field(default_factory=tuple)
    malware_ids: tuple[str, ...] = field(default_factory=tuple)
    infrastructure_ids: tuple[str, ...] = field(default_factory=tuple)
    chain_of_custody: tuple[str, ...] = field(default_factory=tuple)
    confidence_explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "evidence_type": self.evidence_type,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "content_type": self.content_type,
            "source": self.source,
            "source_url": self.source_url,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
            "assertion_ids": list(self.assertion_ids),
            "indicator_ids": list(self.indicator_ids),
            "malware_ids": list(self.malware_ids),
            "infrastructure_ids": list(self.infrastructure_ids),
            "chain_of_custody": list(self.chain_of_custody),
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class EvidenceLink(CampaignBase):
    """Evidence link."""
    campaign_id: str = ""
    evidence_id: str = ""
    link_type: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "evidence_id": self.evidence_id,
            "link_type": self.link_type,
            "description": self.description,
        })
        return base
