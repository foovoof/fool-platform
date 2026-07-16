"""
threat_intelligence/campaigns/models/campaign.py

Campaign Models.
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
class Campaign(CampaignBase, Auditable, Explainable, Versionable, ConfidenceMixin):
    """Campaign entity."""
    name: str = ""
    description: str = ""
    status: str = "planned"
    severity: str = "medium"
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    start_date: str = ""
    end_date: str = ""
    first_observed: str = ""
    last_observed: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)
    objectives: tuple[str, ...] = field(default_factory=tuple)
    motivations: tuple[str, ...] = field(default_factory=tuple)
    sectors: tuple[str, ...] = field(default_factory=tuple)
    geographies: tuple[str, ...] = field(default_factory=tuple)
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    associated_infrastructure: tuple[str, ...] = field(default_factory=tuple)
    associated_indicators: tuple[str, ...] = field(default_factory=tuple)
    associated_evidence: tuple[str, ...] = field(default_factory=tuple)
    associated_assertions: tuple[str, ...] = field(default_factory=tuple)
    victim_count: int = 0
    intended_impact: str = ""
    observed_impact: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    governance_status: str = "draft"
    review_status: str = "pending"
    approved_by: str = ""
    approved_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "severity": self.severity,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "first_observed": self.first_observed,
            "last_observed": self.last_observed,
            "aliases": list(self.aliases),
            "objectives": list(self.objectives),
            "motivations": list(self.motivations),
            "sectors": list(self.sectors),
            "geographies": list(self.geographies),
            "associated_actors": list(self.associated_actors),
            "associated_malware": list(self.associated_malware),
            "associated_infrastructure": list(self.associated_infrastructure),
            "associated_indicators": list(self.associated_indicators),
            "associated_evidence": list(self.associated_evidence),
            "associated_assertions": list(self.associated_assertions),
            "victim_count": self.victim_count,
            "intended_impact": self.intended_impact,
            "observed_impact": self.observed_impact,
            "tags": list(self.tags),
            "governance_status": self.governance_status,
            "review_status": self.review_status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "explanation": self.explanation,
            "reasoning": self.reasoning,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
            "source_url": self.source_url,
        })
        return base


@dataclass(frozen=True)
class CampaignAlias(CampaignBase):
    """Campaign alias."""
    campaign_id: str = ""
    alias: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "alias": self.alias,
            "description": self.description,
        })
        return base


@dataclass(frozen=True)
class CampaignMetadata(CampaignBase):
    """Campaign metadata."""
    campaign_id: str = ""
    metadata_type: str = ""
    key: str = ""
    value: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "metadata_type": self.metadata_type,
            "key": self.key,
            "value": self.value,
        })
        return base
