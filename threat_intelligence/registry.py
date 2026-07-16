"""
threat_intelligence/registry.py

Threat Intelligence Registry.

Central registry for threat intelligence components.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from threat_intelligence.repository import RepositoryBase
    from threat_intelligence.models import (
        Indicator, ThreatActor, Campaign, Malware,
        Infrastructure, Vulnerability, Tool, Relationship,
        EvidenceReference, IntelligenceFinding, ThreatReport,
        ThreatPackage,
    )


@dataclass
class ThreatIntelligenceRegistry:
    """
    Central registry for threat intelligence components.
    
    Provides access to all repositories and services.
    """
    
    indicator_repository: RepositoryBase | None = None
    threat_actor_repository: RepositoryBase | None = None
    campaign_repository: RepositoryBase | None = None
    malware_repository: RepositoryBase | None = None
    infrastructure_repository: RepositoryBase | None = None
    vulnerability_repository: RepositoryBase | None = None
    tool_repository: RepositoryBase | None = None
    relationship_repository: RepositoryBase | None = None
    evidence_repository: RepositoryBase | None = None
    finding_repository: RepositoryBase | None = None
    report_repository: RepositoryBase | None = None
    package_repository: RepositoryBase | None = None
    
    _instance: ThreatIntelligenceRegistry | None = None
    
    def __new__(cls) -> ThreatIntelligenceRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> ThreatIntelligenceRegistry:
        """Get singleton instance."""
        return cls()
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton instance."""
        cls._instance = None
    
    def get_repository(self, entity_type: str) -> RepositoryBase | None:
        """Get repository by entity type."""
        repositories = {
            "indicator": self.indicator_repository,
            "threat_actor": self.threat_actor_repository,
            "campaign": self.campaign_repository,
            "malware": self.malware_repository,
            "infrastructure": self.infrastructure_repository,
            "vulnerability": self.vulnerability_repository,
            "tool": self.tool_repository,
            "relationship": self.relationship_repository,
            "evidence": self.evidence_repository,
            "finding": self.finding_repository,
            "report": self.report_repository,
            "package": self.package_repository,
        }
        return repositories.get(entity_type)
    
    def register_repository(
        self, entity_type: str, repository: RepositoryBase
    ) -> None:
        """Register a repository."""
        setattr(self, f"{entity_type}_repository", repository)
    
    def get_stats(self) -> dict[str, int]:
        """Get repository statistics."""
        stats = {}
        for entity_type in [
            "indicator", "threat_actor", "campaign", "malware",
            "infrastructure", "vulnerability", "tool", "relationship",
            "evidence", "finding", "report", "package",
        ]:
            repo = self.get_repository(entity_type)
            if repo:
                stats[entity_type] = repo.count()
        return stats
