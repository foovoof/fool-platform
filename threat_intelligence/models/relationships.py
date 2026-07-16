"""
threat_intelligence/models/relationships.py

Relationship Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import ThreatBase, Auditable, ConfidenceMixin


@dataclass(frozen=True)
class Relationship(ThreatBase, Auditable, ConfidenceMixin):
    """Relationship between threat entities."""
    source_type: str = ""
    source_id: str = ""
    target_type: str = ""
    target_id: str = ""
    relationship_type: str = ""
    description: str = ""
    first_seen: str = ""
    last_seen: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "source_type": self.source_type,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type,
            "description": self.description,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


class RelationshipType:
    """Common relationship types."""
    USES = "uses"
    USED_BY = "used_by"
    TARGETS = "targets"
    TARGETED_BY = "targeted_by"
    DELIVERS = "delivers"
    DELIVERED_BY = "delivered_by"
    DROPS = "drops"
    DROPPED_BY = "dropped_by"
    EXPLOITS = "exploits"
    EXPLOITED_BY = "exploited_by"
    COMMUNICATES_WITH = "communicates_with"
    LOCATED_AT = "located_at"
    HOSTS = "hosts"
    HOSTED_BY = "hosted_by"
    ASSOCIATED_WITH = "associated_with"
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    ATTRIBUTED_TO = "attributed_to"
    BELONGS_TO = "belongs_to"
    ATTACKS = "attacks"
    DEFENDS = "defends"
