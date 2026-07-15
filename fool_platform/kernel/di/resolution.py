"""
platform/kernel/di/resolution.py

Service resolution logic for dependency injection.
"""
from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Type

from .lifetime import LifetimeManager, ServiceLifetime
from .registration import ServiceRegistration
from ..kernel_exceptions import CircularDependencyError, ServiceNotFoundError

if TYPE_CHECKING:
    from .container import DIContainer


class DependencyResolver:
    """
    Resolves service dependencies recursively.
    
    Handles:
    - Constructor injection
    - Factory-based resolution
    - Circular dependency detection
    - Lifetime management
    """
    
    def __init__(self, container: "DIContainer") -> None:
        self._container = container
        self._lifetime_manager = LifetimeManager(ServiceLifetime.SINGLETON)
        self._resolution_stack: list[str] = []
        self._current_scope_id: str | None = None
    
    def resolve(self, registration: ServiceRegistration) -> Any:
        """
        Resolve a service from its registration.
        
        Args:
            registration: The service registration
            
        Returns:
            The resolved service instance
            
        Raises:
            CircularDependencyError: If circular dependency detected
            ServiceNotFoundError: If dependency cannot be resolved
        """
        key = registration.key
        
        # Check for circular dependency
        if key in self._resolution_stack:
            raise CircularDependencyError(
                f"Circular dependency detected: {' -> '.join(self._resolution_stack + [key])}"
            )
        
        # Check for existing instance based on lifetime
        existing = self._get_existing_instance(registration, key)
        if existing is not None:
            return existing
        
        # Push to resolution stack for cycle detection
        self._resolution_stack.append(key)
        
        try:
            # Create new instance
            instance = self._create_instance(registration)
            
            # Store instance based on lifetime
            self._store_instance(registration, key, instance)
            
            return instance
            
        finally:
            # Pop from resolution stack
            self._resolution_stack.pop()
    
    def _get_existing_instance(
        self, registration: ServiceRegistration, key: str
    ) -> Any | None:
        """Get existing instance based on lifetime policy."""
        if registration.lifetime == ServiceLifetime.SINGLETON:
            return self._lifetime_manager.get_instance(key)
        elif registration.lifetime == ServiceLifetime.SCOPED and self._current_scope_id:
            return self._lifetime_manager.get_scoped_instance(
                self._current_scope_id, key
            )
        return None
    
    def _store_instance(
        self, registration: ServiceRegistration, key: str, instance: Any
    ) -> None:
        """Store instance based on lifetime policy."""
        if registration.lifetime == ServiceLifetime.SINGLETON:
            self._lifetime_manager.set_instance(key, instance)
        elif registration.lifetime == ServiceLifetime.SCOPED and self._current_scope_id:
            self._lifetime_manager.set_scoped_instance(
                self._current_scope_id, key, instance
            )
    
    def _create_instance(self, registration: ServiceRegistration) -> Any:
        """Create a new service instance."""
        if registration.factory is not None:
            # Use factory function with dependency injection
            return self._resolve_factory(registration)
        elif registration.implementation_type is not None:
            # Use constructor injection
            return self._resolve_constructor(registration)
        else:
            raise ServiceNotFoundError(
                f"Cannot create instance for {registration.service_type}"
            )
    
    def _resolve_factory(self, registration: ServiceRegistration) -> Any:
        """Resolve dependencies for a factory function."""
        deps = self._resolve_dependencies(registration.dependencies)
        
        if registration.factory:
            sig = inspect.signature(registration.factory)
            if len(sig.parameters) > 0:
                return registration.factory(*deps)
            return registration.factory()
        return deps
    
    def _resolve_constructor(self, registration: ServiceRegistration) -> Any:
        """Resolve dependencies for a constructor."""
        impl_type = registration.implementation_type
        if impl_type is None:
            raise ServiceNotFoundError("No implementation type specified")
        
        # Get constructor parameters
        try:
            sig = inspect.signature(impl_type)
        except (ValueError, TypeError):
            # Cannot inspect, try direct instantiation
            return impl_type()
        
        deps = self._resolve_dependencies(registration.dependencies)
        
        # Match dependencies to constructor parameters
        params = list(sig.parameters.keys())
        if not params:
            return impl_type()
        
        # Build keyword arguments from dependencies
        kwargs = {}
        for i, param_name in enumerate(params):
            if i < len(deps):
                kwargs[param_name] = deps[i]
            elif registration.dependencies and i < len(registration.dependencies):
                # Try to resolve by name
                dep_key = registration.dependencies[i]
                kwargs[param_name] = self._container.resolve_by_key(dep_key)
        
        return impl_type(**kwargs)
    
    def _resolve_dependencies(self, dependency_keys: tuple[str, ...]) -> list[Any]:
        """Resolve a list of dependencies."""
        deps = []
        for key in dependency_keys:
            dep = self._container.resolve_by_key(key)
            deps.append(dep)
        return deps
    
    def set_scope(self, scope_id: str | None) -> None:
        """Set the current scope for scoped services."""
        self._current_scope_id = scope_id
    
    def clear_scope(self, scope_id: str) -> None:
        """Clear all scoped instances for a scope."""
        self._lifetime_manager.clear_scope(scope_id)
    
    def clear_all(self) -> None:
        """Clear all cached instances."""
        self._lifetime_manager.clear_all()
        self._resolution_stack.clear()


__all__ = [
    "DependencyResolver",
]
