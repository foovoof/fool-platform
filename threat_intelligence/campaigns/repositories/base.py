"""
threat_intelligence/campaigns/repositories/base.py

Repository Base.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class RepositoryBase(ABC, Generic[T]):
    """
    Base repository interface.
    
    Provides CRUD operations and query capabilities.
    No persistence - in-memory only.
    """
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity."""
        pass
    
    @abstractmethod
    def list_all(self) -> list[T]:
        """List all entities."""
        pass
    
    @abstractmethod
    def search(self, query: dict[str, Any]) -> list[T]:
        """Search entities by query."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count entities."""
        pass
    
    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """Check if entity exists."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all entities."""
        pass
