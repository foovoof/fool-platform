"""
threat_intelligence/campaigns/models/relationships.py

Campaign Relationship Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase, Auditable, ConfidenceMixin


@dataclass(frozen=True)
class CampaignRelationship(CampaignBase, Auditable, ConfidenceMixin):
    """Campaign relationship."""
    campaign_id: str = ""
    source_type: str = ""
    source_id: str = ""
    target_type: str = ""
    target_id: str = ""
    relationship_type: str = ""
    description: str = ""
    first_observed: str = ""
    last_observed: str = ""
    confidence_explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type,
            "description": self.description,
            "first_observed": self.first_observed,
            "last_observed": self.last_observed,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


class CampaignRelationshipType:
    """Campaign relationship types."""
    USES = "uses"
    TARGETS = "targets"
    DELIVERS = "delivers"
    EXPLOITS = "exploits"
    ATTRIBUTED_TO = "attributed_to"
    ASSOCIATED_WITH = "associated_with"
    PART_OF = "part_of"
    OPERATES_IN = "operates_in"
    AFFECTS = "affects"
    DEPLOYS = "deploys"
    UTILIZES = "utilizes"
    COMPROMISES = "compromises"
