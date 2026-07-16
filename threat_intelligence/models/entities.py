"""
threat_intelligence/models/entities.py

Entity Models for Threat Intelligence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import (
    ThreatBase,
    Auditable,
    Explainable,
    ConfidenceMixin,
)
from threat_intelligence.models.enums import (
    IndicatorType,
    IndicatorStatus,
    ThreatActorType,
    MalwareType,
    MalwareFamily,
    CampaignStatus,
    ThreatLevel,
    EvidenceType,
    FindingType,
)


@dataclass(frozen=True)
class Indicator(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Indicator of compromise."""
    name: str = ""
    description: str = ""
    indicator_type: str = IndicatorType.CUSTOM.value
    value: str = ""
    pattern: str = ""
    pattern_type: str = ""
    status: str = IndicatorStatus.OBSERVED.value
    threat_level: str = ThreatLevel.MEDIUM.value
    first_seen: str = ""
    last_seen: str = ""
    observed_count: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)
    kill_chain_phases: tuple[str, ...] = field(default_factory=tuple)
    malware_family: str = ""
    threat_actor: str = ""
    campaign: str = ""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "indicator_type": self.indicator_type,
            "value": self.value,
            "pattern": self.pattern,
            "pattern_type": self.pattern_type,
            "status": self.status,
            "threat_level": self.threat_level,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "observed_count": self.observed_count,
            "tags": list(self.tags),
            "kill_chain_phases": list(self.kill_chain_phases),
            "malware_family": self.malware_family,
            "threat_actor": self.threat_actor,
            "campaign": self.campaign,
            "explanation": self.explanation,
            "reasoning": self.reasoning,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
            "source_url": self.source_url,
            "source_confidence": self.source_confidence,
        })
        return base


@dataclass(frozen=True)
class ThreatActor(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Threat actor entity."""
    name: str = ""
    alias: str = ""
    description: str = ""
    actor_type: str = ThreatActorType.UNKNOWN.value
    sophistication: str = ""
    resource_level: str = ""
    motivation: str = ""
    intent: str = ""
    target_sectors: tuple[str, ...] = field(default_factory=tuple)
    target_geographies: tuple[str, ...] = field(default_factory=tuple)
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    associated_campaigns: tuple[str, ...] = field(default_factory=tuple)
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    status: str = "active"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "alias": self.alias,
            "description": self.description,
            "actor_type": self.actor_type,
            "sophistication": self.sophistication,
            "resource_level": self.resource_level,
            "motivation": self.motivation,
            "intent": self.intent,
            "target_sectors": list(self.target_sectors),
            "target_geographies": list(self.target_geographies),
            "associated_actors": list(self.associated_actors),
            "associated_malware": list(self.associated_malware),
            "associated_campaigns": list(self.associated_campaigns),
            "capabilities": list(self.capabilities),
            "tags": list(self.tags),
            "status": self.status,
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Campaign(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Campaign entity."""
    name: str = ""
    description: str = ""
    status: str = CampaignStatus.UNKNOWN.value
    objective: str = ""
    start_date: str = ""
    end_date: str = ""
    threat_actor: str = ""
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    target_sectors: tuple[str, ...] = field(default_factory=tuple)
    target_geographies: tuple[str, ...] = field(default_factory=tuple)
    associated_indicators: tuple[str, ...] = field(default_factory=tuple)
    associated_infrastructure: tuple[str, ...] = field(default_factory=tuple)
    intended_impact: str = ""
    observed_impact: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "objective": self.objective,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "threat_actor": self.threat_actor,
            "associated_malware": list(self.associated_malware),
            "target_sectors": list(self.target_sectors),
            "target_geographies": list(self.target_geographies),
            "associated_indicators": list(self.associated_indicators),
            "associated_infrastructure": list(self.associated_infrastructure),
            "intended_impact": self.intended_impact,
            "observed_impact": self.observed_impact,
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Malware(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Malware entity."""
    name: str = ""
    alias: str = ""
    description: str = ""
    malware_type: str = MalwareType.TROJAN.value
    malware_family: str = ""
    family_classification: str = MalwareFamily.OPPORTUNISTIC.value
    is_family: bool = True
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    infections_count: int = 0
    infections_geographies: tuple[str, ...] = field(default_factory=tuple)
    command_and_control: tuple[str, ...] = field(default_factory=tuple)
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_campaigns: tuple[str, ...] = field(default_factory=tuple)
    associated_indicators: tuple[str, ...] = field(default_factory=tuple)
    detection_names: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "alias": self.alias,
            "description": self.description,
            "malware_type": self.malware_type,
            "malware_family": self.malware_family,
            "family_classification": self.family_classification,
            "is_family": self.is_family,
            "capabilities": list(self.capabilities),
            "infections_count": self.infections_count,
            "infections_geographies": list(self.infections_geographies),
            "command_and_control": list(self.command_and_control),
            "associated_actors": list(self.associated_actors),
            "associated_campaigns": list(self.associated_campaigns),
            "associated_indicators": list(self.associated_indicators),
            "detection_names": list(self.detection_names),
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Tool(ThreatBase, Auditable, Explainable):
    """Tool entity."""
    name: str = ""
    description: str = ""
    tool_type: str = ""
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "tool_type": self.tool_type,
            "capabilities": list(self.capabilities),
            "associated_actors": list(self.associated_actors),
            "associated_malware": list(self.associated_malware),
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Infrastructure(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Infrastructure entity."""
    hostname: str = ""
    ip_address: str = ""
    domain: str = ""
    url: str = ""
    asn: str = ""
    hosting_provider: str = ""
    country: str = ""
    infrastructure_type: str = ""
    status: str = "active"
    first_seen: str = ""
    last_seen: str = ""
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    associated_campaigns: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "domain": self.domain,
            "url": self.url,
            "asn": self.asn,
            "hosting_provider": self.hosting_provider,
            "country": self.country,
            "infrastructure_type": self.infrastructure_type,
            "status": self.status,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "associated_actors": list(self.associated_actors),
            "associated_malware": list(self.associated_malware),
            "associated_campaigns": list(self.associated_campaigns),
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Vulnerability(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Vulnerability entity."""
    cve_id: str = ""
    title: str = ""
    description: str = ""
    severity: str = ""
    cvss_score: float = 0.0
    cvss_vector: str = ""
    affected_products: tuple[str, ...] = field(default_factory=tuple)
    remediation: str = ""
    exploitation_level: str = ""
    patch_available: bool = False
    patch_url: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "cve_id": self.cve_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "cvss_vector": self.cvss_vector,
            "affected_products": list(self.affected_products),
            "remediation": self.remediation,
            "exploitation_level": self.exploitation_level,
            "patch_available": self.patch_available,
            "patch_url": self.patch_url,
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base
