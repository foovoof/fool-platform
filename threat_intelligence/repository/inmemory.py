"""
threat_intelligence/repository/inmemory.py

In-Memory Repository Implementations.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypeVar

from threat_intelligence.repository.base import RepositoryBase

T = TypeVar("T")


class InMemoryRepository(RepositoryBase[T]):
    """
    In-memory repository implementation.
    
    No persistence. Data is lost on restart.
    """
    
    def __init__(self) -> None:
        self._storage: dict[str, T] = {}
        self._history: dict[str, list[T]] = {}
    
    def create(self, entity: T) -> T:
        """Create a new entity."""
        entity_id = getattr(entity, "id", None)
        if not entity_id:
            raise ValueError("Entity must have an id")
        
        if entity_id in self._storage:
            raise ValueError(f"Entity with id {entity_id} already exists")
        
        self._storage[entity_id] = entity
        self._history[entity_id] = [entity]
        return entity
    
    def get(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        return self._storage.get(entity_id)
    
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        entity_id = getattr(entity, "id", None)
        if not entity_id:
            raise ValueError("Entity must have an id")
        
        if entity_id not in self._storage:
            raise ValueError(f"Entity with id {entity_id} not found")
        
        self._storage[entity_id] = entity
        
        if entity_id in self._history:
            self._history[entity_id].append(entity)
        
        return entity
    
    def delete(self, entity_id: str) -> bool:
        """Delete an entity."""
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def list_all(self) -> list[T]:
        """List all entities."""
        return list(self._storage.values())
    
    def search(self, query: dict[str, Any]) -> list[T]:
        """Search entities by query."""
        results = []
        for entity in self._storage.values():
            if self._matches_query(entity, query):
                results.append(entity)
        return results
    
    def _matches_query(self, entity: T, query: dict[str, Any]) -> bool:
        """Check if entity matches query."""
        for key, value in query.items():
            entity_value = getattr(entity, key, None)
            if entity_value is None:
                return False
            if isinstance(value, (list, tuple)):
                if entity_value not in value:
                    return False
            elif entity_value != value:
                return False
        return True
    
    def count(self) -> int:
        """Count entities."""
        return len(self._storage)
    
    def exists(self, entity_id: str) -> bool:
        """Check if entity exists."""
        return entity_id in self._storage
    
    def clear(self) -> None:
        """Clear all entities."""
        self._storage.clear()
        self._history.clear()
    
    def get_history(self, entity_id: str) -> list[T]:
        """Get version history for an entity."""
        return list(self._history.get(entity_id, []))


class IndicatorRepository(InMemoryRepository):
    """Repository for indicators."""
    pass


class ThreatActorRepository(InMemoryRepository):
    """Repository for threat actors."""
    pass


class CampaignRepository(InMemoryRepository):
    """Repository for campaigns."""
    pass


class MalwareRepository(InMemoryRepository):
    """Repository for malware."""
    pass


class InfrastructureRepository(InMemoryRepository):
    """Repository for infrastructure."""
    pass


class VulnerabilityRepository(InMemoryRepository):
    """Repository for vulnerabilities."""
    pass


class ToolRepository(InMemoryRepository):
    """Repository for tools."""
    pass


class RelationshipRepository(InMemoryRepository):
    """Repository for relationships."""
    pass


class EvidenceRepository(InMemoryRepository):
    """Repository for evidence."""
    pass


class FindingRepository(InMemoryRepository):
    """Repository for findings."""
    pass


class ReportRepository(InMemoryRepository):
    """Repository for reports."""
    pass


class PackageRepository(InMemoryRepository):
    """Repository for threat packages."""
    pass
