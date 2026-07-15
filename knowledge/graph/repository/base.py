"""
knowledge/graph/repository/base.py

Base repository abstraction for the Knowledge Layer.

Provides the common interface for all repositories.
Storage-agnostic design.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Optional

T = TypeVar("T")


class KnowledgeRepository(ABC, Generic[T]):
    """
    Abstract base class for knowledge repositories.
    
    Defines the common interface for CRUD operations.
    Concrete implementations handle storage (in-memory, database, etc.)
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new entity.
        
        Args:
            entity: The entity to create
            
        Returns:
            The created entity
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Update an existing entity.
        
        Args:
            entity: The entity to update
            
        Returns:
            The updated entity
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by ID.
        
        Args:
            entity_id: The ID of the entity to delete
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Get an entity by ID.
        
        Args:
            entity_id: The ID of the entity
            
        Returns:
            The entity or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    def list(self, **kwargs: Any) -> list[T]:
        """
        List all entities with optional filtering.
        
        Args:
            **kwargs: Optional filter parameters
            
        Returns:
            List of matching entities
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, **kwargs: Any) -> list[T]:
        """
        Search for entities.
        
        Args:
            query: Search query
            **kwargs: Optional search parameters
            
        Returns:
            List of matching entities
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists.
        
        Args:
            entity_id: The ID to check
            
        Returns:
            True if exists
        """
        raise NotImplementedError

    @abstractmethod
    def count(self, **kwargs: Any) -> int:
        """
        Count entities matching criteria.
        
        Args:
            **kwargs: Optional filter parameters
            
        Returns:
            Count of matching entities
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Clear all entities from the repository."""
        raise NotImplementedError
