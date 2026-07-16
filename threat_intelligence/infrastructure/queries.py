"""
threat_intelligence/infrastructure/queries.py

Infrastructure Queries.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.infrastructure.service import InfrastructureService


class InfrastructureQueryService:
    """Service for querying infrastructure."""
    
    def __init__(self, service: InfrastructureService | None = None) -> None:
        self._service = service or InfrastructureService()
    
    def find_by_type(self, infra_type: str) -> list[dict[str, Any]]:
        """Find infrastructure by type."""
        results = self._service.find_by_type(infra_type)
        return [r.to_dict() for r in results]
    
    def find_by_role(self, role: str) -> list[dict[str, Any]]:
        """Find infrastructure by role."""
        results = self._service.find_by_role(role)
        return [r.to_dict() for r in results]
    
    def find_by_status(self, status: str) -> list[dict[str, Any]]:
        """Find infrastructure by status."""
        results = self._service.find_by_status(status)
        return [r.to_dict() for r in results]
    
    def find_by_confidence(self, confidence_level: str) -> list[dict[str, Any]]:
        """Find infrastructure by confidence level."""
        results = self._service.search({"confidence_level": confidence_level})
        return [r.to_dict() for r in results]
    
    def find_by_actor(self, actor_id: str) -> list[dict[str, Any]]:
        """Find infrastructure by associated actor."""
        results = self._service.find_by_actor(actor_id)
        return [r.to_dict() for r in results]
    
    def find_by_malware(self, malware_id: str) -> list[dict[str, Any]]:
        """Find infrastructure by associated malware."""
        results = self._service.find_by_malware(malware_id)
        return [r.to_dict() for r in results]
    
    def find_by_campaign(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find infrastructure by associated campaign."""
        results = self._service.find_by_campaign(campaign_id)
        return [r.to_dict() for r in results]
    
    def find_by_service(self, service: str) -> list[dict[str, Any]]:
        """Find infrastructure by service."""
        results = self._service.search({"services": service})
        return [r.to_dict() for r in results]
    
    def find_by_protocol(self, protocol: str) -> list[dict[str, Any]]:
        """Find infrastructure by protocol."""
        results = self._service.search({"protocols": protocol})
        return [r.to_dict() for r in results]
    
    def find_by_country(self, country: str) -> list[dict[str, Any]]:
        """Find infrastructure by country."""
        results = self._service.search({"country": country})
        return [r.to_dict() for r in results]
    
    def find_by_asn(self, asn: int) -> list[dict[str, Any]]:
        """Find infrastructure by ASN."""
        results = self._service.search({"asn": asn})
        return [r.to_dict() for r in results]
    
    def find_by_cidr(self, cidr: str) -> list[dict[str, Any]]:
        """Find infrastructure by CIDR."""
        results = self._service.search({"cidr": cidr})
        return [r.to_dict() for r in results]
    
    def find_by_tag(self, tag: str) -> list[dict[str, Any]]:
        """Find infrastructure by tag."""
        results = self._service.search({"tags": tag})
        return [r.to_dict() for r in results]
