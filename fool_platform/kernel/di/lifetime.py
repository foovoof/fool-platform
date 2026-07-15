"""
platform/kernel/di/lifetime.py

Service lifetime policies for dependency injection.
"""
from enum import Enum, auto


class ServiceLifetime(Enum):
    """
    Service lifetime policies.
    
    Determines when services are created and disposed.
    """
    TRANSIENT = auto()
    """New instance created each time the service is resolved."""
    
    SINGLETON = auto()
    """Single instance created and shared across all resolutions."""
    
    SCOPED = auto()
    """One instance per scope (e.g., per request or per operation)."""


class LifetimeManager:
    """
    Manages instances for a given lifetime policy.
    
    Tracks created instances and provides lifecycle management.
    """
    
    def __init__(self, lifetime: ServiceLifetime) -> None:
        self._lifetime = lifetime
        self._instances: dict[str, object] = {}
        self._scopes: dict[str, dict[str, object]] = {}
    
    @property
    def lifetime(self) -> ServiceLifetime:
        """The lifetime policy for this manager."""
        return self._lifetime
    
    def get_instance(self, key: str) -> object | None:
        """Get an existing instance for singleton lifetime."""
        if self._lifetime == ServiceLifetime.SINGLETON:
            return self._instances.get(key)
        return None
    
    def set_instance(self, key: str, instance: object) -> None:
        """Store an instance for singleton lifetime."""
        if self._lifetime == ServiceLifetime.SINGLETON:
            self._instances[key] = instance
    
    def remove_instance(self, key: str) -> None:
        """Remove an instance from storage."""
        if self._lifetime == ServiceLifetime.SINGLETON:
            self._instances.pop(key, None)
    
    def get_scoped_instance(self, scope_id: str, key: str) -> object | None:
        """Get an instance for scoped lifetime."""
        if self._lifetime == ServiceLifetime.SCOPED:
            scope = self._scopes.get(scope_id, {})
            return scope.get(key)
        return None
    
    def set_scoped_instance(self, scope_id: str, key: str, instance: object) -> None:
        """Store an instance for scoped lifetime."""
        if self._lifetime == ServiceLifetime.SCOPED:
            if scope_id not in self._scopes:
                self._scopes[scope_id] = {}
            self._scopes[scope_id][key] = instance
    
    def clear_scope(self, scope_id: str) -> None:
        """Clear all instances for a scope."""
        if scope_id in self._scopes:
            del self._scopes[scope_id]
    
    def clear_all(self) -> None:
        """Clear all stored instances."""
        self._instances.clear()
        self._scopes.clear()


__all__ = [
    "LifetimeManager",
    "ServiceLifetime",
]
