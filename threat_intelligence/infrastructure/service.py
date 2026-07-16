"""
threat_intelligence/infrastructure/service.py

Infrastructure Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.infrastructure.models import (
    Infrastructure,
    InfrastructureAssertion,
    InfrastructureEvidence,
    InfrastructureRelationship,
    InfrastructureVersion,
    InfrastructureHistory,
    LifecycleState,
    LifecycleTransition,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._infrastructure: dict[str, Infrastructure] = {}
        self._assertions: dict[str, InfrastructureAssertion] = {}
        self._evidence: dict[str, InfrastructureEvidence] = {}
        self._relationships: dict[str, InfrastructureRelationship] = {}
        self._versions: dict[str, InfrastructureVersion] = {}
        self._histories: dict[str, InfrastructureHistory] = {}
        self._lifecycles: dict[str, LifecycleState] = {}


_storage = InMemoryStorage()


class InfrastructureService:
    """Service for managing infrastructure."""
    
    def create(
        self,
        name: str,
        infrastructure_type: str,
        value: str,
        author: str = "",
        **kwargs: Any,
    ) -> Infrastructure:
        """Create new infrastructure."""
        infra = Infrastructure(
            id=str(uuid4()),
            name=name,
            infrastructure_type=infrastructure_type,
            value=value,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._infrastructure[infra.id] = infra
        return infra
    
    def get(self, infrastructure_id: str) -> Infrastructure | None:
        """Get infrastructure by ID."""
        return _storage._infrastructure.get(infrastructure_id)
    
    def update(self, infrastructure: Infrastructure) -> Infrastructure:
        """Update infrastructure."""
        updated = Infrastructure(
            id=infrastructure.id,
            name=infrastructure.name,
            infrastructure_type=infrastructure.infrastructure_type,
            value=infrastructure.value,
            role=infrastructure.role,
            hosting_type=infrastructure.hosting_type,
            status=infrastructure.status,
            description=infrastructure.description,
            first_observed=infrastructure.first_observed,
            last_observed=infrastructure.last_observed,
            asn=infrastructure.asn,
            cidr=infrastructure.cidr,
            isp=infrastructure.isp,
            organization=infrastructure.organization,
            country=infrastructure.country,
            region=infrastructure.region,
            city=infrastructure.city,
            coordinates=infrastructure.coordinates,
            services=infrastructure.services,
            protocols=infrastructure.protocols,
            ports=infrastructure.ports,
            certificates=infrastructure.certificates,
            associated_actors=infrastructure.associated_actors,
            associated_malware=infrastructure.associated_malware,
            associated_campaigns=infrastructure.associated_campaigns,
            associated_indicators=infrastructure.associated_indicators,
            associated_evidence=infrastructure.associated_evidence,
            associated_assertions=infrastructure.associated_assertions,
            tags=infrastructure.tags,
            governance_status=infrastructure.governance_status,
            confidence_level=infrastructure.confidence_level,
            confidence_score=infrastructure.confidence_score,
            confidence_explanation=infrastructure.confidence_explanation,
            author=infrastructure.author,
            reason=infrastructure.reason,
            source=infrastructure.source,
            source_url=infrastructure.source_url,
            created_at=infrastructure.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=infrastructure.created_by,
            modified_by=infrastructure.modified_by,
            version=infrastructure.version + 1,
            metadata=infrastructure.metadata,
            revision_history=infrastructure.revision_history,
        )
        _storage._infrastructure[updated.id] = updated
        return updated
    
    def delete(self, infrastructure_id: str) -> bool:
        """Delete infrastructure."""
        if infrastructure_id in _storage._infrastructure:
            del _storage._infrastructure[infrastructure_id]
            return True
        return False
    
    def list_all(self) -> list[Infrastructure]:
        """List all infrastructure."""
        return list(_storage._infrastructure.values())
    
    def search(self, query: dict[str, Any]) -> list[Infrastructure]:
        """Search infrastructure."""
        results = []
        for infra in _storage._infrastructure.values():
            if self._matches_query(infra, query):
                results.append(infra)
        return results
    
    def _matches_query(self, infra: Infrastructure, query: dict[str, Any]) -> bool:
        """Check if infrastructure matches query."""
        for key, value in query.items():
            infra_value = getattr(infra, key, None)
            if infra_value is None:
                return False
            if isinstance(value, (list, tuple)):
                if infra_value not in value:
                    return False
            elif infra_value != value:
                return False
        return True
    
    def find_by_type(self, infra_type: str) -> list[Infrastructure]:
        """Find by infrastructure type."""
        return self.search({"infrastructure_type": infra_type})
    
    def find_by_status(self, status: str) -> list[Infrastructure]:
        """Find by status."""
        return self.search({"status": status})
    
    def find_by_role(self, role: str) -> list[Infrastructure]:
        """Find by role."""
        return self.search({"role": role})
    
    def find_by_actor(self, actor_id: str) -> list[Infrastructure]:
        """Find by associated actor."""
        return self.search({"associated_actors": actor_id})
    
    def find_by_malware(self, malware_id: str) -> list[Infrastructure]:
        """Find by associated malware."""
        return self.search({"associated_malware": malware_id})
    
    def find_by_campaign(self, campaign_id: str) -> list[Infrastructure]:
        """Find by associated campaign."""
        return self.search({"associated_campaigns": campaign_id})
    
    def count(self) -> int:
        """Count infrastructure."""
        return len(_storage._infrastructure)
