"""
threat_intelligence/services/indicator_service.py

Indicator Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.models import (
    Indicator,
    IndicatorType,
    IndicatorStatus,
)
from threat_intelligence.repository import IndicatorRepository


class IndicatorService:
    """
    Service for managing indicators.
    
    Provides CRUD operations and business logic.
    """
    
    def __init__(self, repository: IndicatorRepository | None = None) -> None:
        self._repository = repository or IndicatorRepository()
    
    @property
    def repository(self) -> IndicatorRepository:
        """Get the repository."""
        return self._repository
    
    def create(
        self,
        name: str,
        value: str,
        indicator_type: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> Indicator:
        """
        Create a new indicator.
        
        Args:
            name: Indicator name
            value: Indicator value
            indicator_type: Type of indicator
            description: Description
            author: Author
            **kwargs: Additional fields
            
        Returns:
            Created indicator
        """
        indicator = Indicator(
            id=str(uuid4()),
            name=name,
            value=value,
            indicator_type=indicator_type,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(indicator)
    
    def get(self, indicator_id: str) -> Indicator | None:
        """Get indicator by ID."""
        return self._repository.get(indicator_id)
    
    def update(self, indicator: Indicator) -> Indicator:
        """Update an indicator."""
        updated = Indicator(
            id=indicator.id,
            name=indicator.name,
            value=indicator.value,
            indicator_type=indicator.indicator_type,
            description=indicator.description,
            status=indicator.status,
            threat_level=indicator.threat_level,
            first_seen=indicator.first_seen,
            last_seen=datetime.now(timezone.utc).isoformat(),
            observed_count=indicator.observed_count + 1,
            tags=indicator.tags,
            kill_chain_phases=indicator.kill_chain_phases,
            malware_family=indicator.malware_family,
            threat_actor=indicator.threat_actor,
            campaign=indicator.campaign,
            confidence_level=indicator.confidence_level,
            confidence_score=indicator.confidence_score,
            confidence_explanation=indicator.confidence_explanation,
            author=indicator.author,
            reason=indicator.reason,
            source=indicator.source,
            source_url=indicator.source_url,
            source_confidence=indicator.source_confidence,
            explanation=indicator.explanation,
            reasoning=indicator.reasoning,
            created_at=indicator.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            modified_by=indicator.modified_by,
            version=indicator.version + 1,
            metadata=indicator.metadata,
        )
        return self._repository.update(updated)
    
    def delete(self, indicator_id: str) -> bool:
        """Delete an indicator."""
        return self._repository.delete(indicator_id)
    
    def list_all(self) -> list[Indicator]:
        """List all indicators."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[Indicator]:
        """Search indicators."""
        return self._repository.search(query)
    
    def find_by_value(self, value: str) -> list[Indicator]:
        """Find indicators by value."""
        return self._repository.search({"value": value})
    
    def find_by_type(self, indicator_type: str) -> list[Indicator]:
        """Find indicators by type."""
        return self._repository.search({"indicator_type": indicator_type})
    
    def find_by_status(self, status: str) -> list[Indicator]:
        """Find indicators by status."""
        return self._repository.search({"status": status})
    
    def find_by_actor(self, actor_id: str) -> list[Indicator]:
        """Find indicators by threat actor."""
        return self._repository.search({"threat_actor": actor_id})
    
    def find_by_malware(self, malware_id: str) -> list[Indicator]:
        """Find indicators by malware."""
        return self._repository.search({"malware_family": malware_id})
    
    def count(self) -> int:
        """Count indicators."""
        return self._repository.count()
    
    def exists(self, indicator_id: str) -> bool:
        """Check if indicator exists."""
        return self._repository.exists(indicator_id)
