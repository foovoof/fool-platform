"""
fool_platform/agents/base/memory.py

Agent Memory for FOOL Platform.

Provides in-memory storage for agent execution context.
"""
from abc import ABC, abstractmethod
from typing import Any


class AgentMemory(ABC):
    """
    Abstract base class for agent memory.
    
    Defines the interface for agent memory operations.
    """

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in memory.
        
        Args:
            key: Memory key
            value: Value to store
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """
        Get a value from memory.
        
        Args:
            key: Memory key
            
        Returns:
            Value or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete a value from memory.
        
        Args:
            key: Memory key
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all values from memory.
        """
        raise NotImplementedError

    @abstractmethod
    def list_keys(self) -> list[str]:
        """
        List all keys in memory.
        
        Returns:
            List of memory keys
        """
        raise NotImplementedError


class InMemoryAgentMemory(AgentMemory):
    """
    In-memory implementation of agent memory.
    
    Provides simple key-value storage with no persistence.
    
    Rules:
    - In-memory only
    - No persistence
    - No vector database
    - No embeddings
    - No external memory providers
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""
        self._storage: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in memory.
        
        Args:
            key: Memory key
            value: Value to store
        """
        self._storage[key] = value

    def get(self, key: str) -> Any | None:
        """
        Get a value from memory.
        
        Args:
            key: Memory key
            
        Returns:
            Value or None if not found
        """
        return self._storage.get(key)

    def delete(self, key: str) -> bool:
        """
        Delete a value from memory.
        
        Args:
            key: Memory key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self._storage:
            del self._storage[key]
            return True
        return False

    def clear(self) -> None:
        """
        Clear all values from memory.
        """
        self._storage.clear()

    def list_keys(self) -> list[str]:
        """
        List all keys in memory.
        
        Returns:
            List of memory keys
        """
        return list(self._storage.keys())

    def __len__(self) -> int:
        """Return the number of items in memory."""
        return len(self._storage)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in memory."""
        return key in self._storage
