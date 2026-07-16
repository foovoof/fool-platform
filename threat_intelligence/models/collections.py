"""
threat_intelligence/models/collections.py

Collection Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import ThreatBase, Auditable


@dataclass(frozen=True)
class ThreatPackage(ThreatBase, Auditable):
    """Package of threat intelligence."""
    name: str = ""
    description: str = ""
    package_type: str = ""
    indicators: tuple[str, ...] = field(default_factory=tuple)
    threat_actors: tuple[str, ...] = field(default_factory=tuple)
    malware: tuple[str, ...] = field(default_factory=tuple)
    campaigns: tuple[str, ...] = field(default_factory=tuple)
    infrastructure: tuple[str, ...] = field(default_factory=tuple)
    vulnerabilities: tuple[str, ...] = field(default_factory=tuple)
    relationships: tuple[str, ...] = field(default_factory=tuple)
    confidence_level: str = "medium"
    threat_level: str = "medium"
    valid_from: str = ""
    valid_until: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "package_type": self.package_type,
            "indicators": list(self.indicators),
            "threat_actors": list(self.threat_actors),
            "malware": list(self.malware),
            "campaigns": list(self.campaigns),
            "infrastructure": list(self.infrastructure),
            "vulnerabilities": list(self.vulnerabilities),
            "relationships": list(self.relationships),
            "confidence_level": self.confidence_level,
            "threat_level": self.threat_level,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class ThreatCollection(ThreatBase, Auditable):
    """Collection of threat intelligence items."""
    name: str = ""
    description: str = ""
    collection_type: str = ""
    items: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    item_count: int = 0
    sources: tuple[str, ...] = field(default_factory=tuple)
    collection_period_start: str = ""
    collection_period_end: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "collection_type": self.collection_type,
            "items": list(self.items),
            "item_count": self.item_count,
            "sources": list(self.sources),
            "collection_period_start": self.collection_period_start,
            "collection_period_end": self.collection_period_end,
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base
