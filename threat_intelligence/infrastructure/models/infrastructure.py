"""
threat_intelligence/infrastructure/models/infrastructure.py

Infrastructure Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.infrastructure.models.base import (
    InfrastructureBase,
    Auditable,
    ConfidenceMixin,
    Versionable,
)


@dataclass(frozen=True)
class Infrastructure(InfrastructureBase, Auditable, ConfidenceMixin, Versionable):
    """Infrastructure entity."""
    name: str = ""
    infrastructure_type: str = ""
    value: str = ""
    role: str = ""
    hosting_type: str = ""
    status: str = "draft"
    description: str = ""
    first_observed: str = ""
    last_observed: str = ""
    asn: int = 0
    cidr: str = ""
    isp: str = ""
    organization: str = ""
    country: str = ""
    region: str = ""
    city: str = ""
    coordinates: tuple[float, float] = field(default_factory=lambda: (0.0, 0.0))
    services: tuple[str, ...] = field(default_factory=tuple)
    protocols: tuple[str, ...] = field(default_factory=tuple)
    ports: tuple[int, ...] = field(default_factory=tuple)
    certificates: tuple[str, ...] = field(default_factory=tuple)
    associated_actors: tuple[str, ...] = field(default_factory=tuple)
    associated_malware: tuple[str, ...] = field(default_factory=tuple)
    associated_campaigns: tuple[str, ...] = field(default_factory=tuple)
    associated_indicators: tuple[str, ...] = field(default_factory=tuple)
    associated_evidence: tuple[str, ...] = field(default_factory=tuple)
    associated_assertions: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    governance_status: str = "draft"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "infrastructure_type": self.infrastructure_type,
            "value": self.value,
            "role": self.role,
            "hosting_type": self.hosting_type,
            "status": self.status,
            "description": self.description,
            "first_observed": self.first_observed,
            "last_observed": self.last_observed,
            "asn": self.asn,
            "cidr": self.cidr,
            "isp": self.isp,
            "organization": self.organization,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "coordinates": list(self.coordinates),
            "services": list(self.services),
            "protocols": list(self.protocols),
            "ports": list(self.ports),
            "certificates": list(self.certificates),
            "associated_actors": list(self.associated_actors),
            "associated_malware": list(self.associated_malware),
            "associated_campaigns": list(self.associated_campaigns),
            "associated_indicators": list(self.associated_indicators),
            "associated_evidence": list(self.associated_evidence),
            "associated_assertions": list(self.associated_assertions),
            "tags": list(self.tags),
            "governance_status": self.governance_status,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
            "source_url": self.source_url,
        })
        return base


@dataclass(frozen=True)
class InfrastructureIdentity(InfrastructureBase):
    """Infrastructure identity."""
    infrastructure_id: str = ""
    identity_type: str = ""
    value: str = ""
    verified: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "identity_type": self.identity_type,
            "value": self.value,
            "verified": self.verified,
        })
        return base


@dataclass(frozen=True)
class InfrastructureAlias(InfrastructureBase):
    """Infrastructure alias."""
    infrastructure_id: str = ""
    alias: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "alias": self.alias,
            "description": self.description,
        })
        return base


@dataclass(frozen=True)
class InfrastructureCapability(InfrastructureBase):
    """Infrastructure capability."""
    infrastructure_id: str = ""
    capability_type: str = ""
    description: str = ""
    enabled: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "capability_type": self.capability_type,
            "description": self.description,
            "enabled": self.enabled,
        })
        return base


@dataclass(frozen=True)
class InfrastructureMetadata(InfrastructureBase):
    """Infrastructure metadata."""
    infrastructure_id: str = ""
    metadata_type: str = ""
    key: str = ""
    value: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "metadata_type": self.metadata_type,
            "key": self.key,
            "value": self.value,
        })
        return base
