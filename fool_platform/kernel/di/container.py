"""
platform/kernel/di/container.py

Dependency injection container for the FOOL Platform.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Type

from .hooks import HookExecutor, HookRegistry, HookType
from .lifetime import ServiceLifetime
from .registration import ServiceRegistration, ServiceRegistrationBuilder
from .resolution import DependencyResolver
from .validation import ContainerValidator
from ..kernel_exceptions import ServiceNotFoundError

logger = logging.getLogger(__name__)


class DIContainer:
    """
    Dependency Injection Container.
    
    Provides:
    - Service registration (singleton, transient, scoped)
    - Service resolution with dependency injection
    - Lifecycle hooks
    - Circular dependency detection
    - Scoped instances with explicit scope management
    """
    
    def __init__(self) -> None:
        self._registrations: dict[str, ServiceRegistration] = {}
        self._resolver = DependencyResolver(self)
        self._hook_registry = HookRegistry()
        self._hook_executor = HookExecutor(self._hook_registry)
        self._scopes: dict[str, list[str]] = {}
        self._current_scope: str | None = None
    
    # Registration methods
    
    def register(
        self,
        service_type: Type,
        implementation: Type | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        name: str | None = None,
    ) -> ServiceRegistrationBuilder:
        """
        Begin fluent registration of a service.
        
        Args:
            service_type: The service interface/type
            implementation: Optional concrete implementation type
            lifetime: Service lifetime (default: singleton)
            name: Optional named registration
            
        Returns:
            Builder for fluent configuration
        """
        builder = ServiceRegistrationBuilder(service_type)
        if implementation is not None:
            builder.to(implementation)
        return builder
    
    def register_singleton(
        self,
        service_type: Type,
        implementation: Type | None = None,
    ) -> ServiceRegistration:
        """Register a singleton service."""
        reg = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation,
            factory=None,
            lifetime=ServiceLifetime.SINGLETON,
            name=None,
            dependencies=(),
        )
        self._add_registration(reg)
        return reg
    
    def register_transient(
        self,
        service_type: Type,
        implementation: Type | None = None,
    ) -> ServiceRegistration:
        """Register a transient service (new instance each time)."""
        reg = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation,
            factory=None,
            lifetime=ServiceLifetime.TRANSIENT,
            name=None,
            dependencies=(),
        )
        self._add_registration(reg)
        return reg
    
    def register_scoped(
        self,
        service_type: Type,
        implementation: Type | None = None,
    ) -> ServiceRegistration:
        """Register a scoped service (one instance per scope)."""
        reg = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation,
            factory=None,
            lifetime=ServiceLifetime.SCOPED,
            name=None,
            dependencies=(),
        )
        self._add_registration(reg)
        return reg
    
    def _add_registration(self, registration: ServiceRegistration) -> None:
        """Add a registration to the container."""
        key = registration.key
        self._registrations[key] = registration
        logger.debug(f"Registered service: {key} ({registration.lifetime.name})")
    
    # Resolution methods
    
    def resolve(self, service_type: Type) -> Any:
        """
        Resolve a service by its type.
        
        Args:
            service_type: The service type to resolve
            
        Returns:
            The resolved service instance
            
        Raises:
            ServiceNotFoundError: If service is not registered
        """
        return self.resolve_named(service_type, None)
    
    def resolve_named(self, service_type: Type, name: str | None) -> Any:
        """
        Resolve a named service registration.
        
        Args:
            service_type: The service type to resolve
            name: Optional name for named registrations
            
        Returns:
            The resolved service instance
        """
        key = self._build_key(service_type, name)
        return self.resolve_by_key(key)
    
    def resolve_by_key(self, key: str) -> Any:
        """
        Resolve a service by its registration key.
        
        Args:
            key: The registration key
            
        Returns:
            The resolved service instance
            
        Raises:
            ServiceNotFoundError: If service is not registered
        """
        registration = self._registrations.get(key)
        if registration is None:
            raise ServiceNotFoundError(f"Service not registered: {key}")
        
        self._hook_executor.before_resolve(self, registration.service_type, registration.name)
        
        try:
            instance = self._resolver.resolve(registration)
            self._hook_executor.after_resolve(self, instance, key)
            return instance
        except Exception as e:
            self._hook_executor.on_error(
                self, registration.service_type, key, e
            )
            raise
    
    # Scope management
    
    def begin_scope(self, scope_id: str) -> None:
        """
        Begin a new scope for scoped services.
        
        Args:
            scope_id: Unique identifier for the scope
        """
        self._resolver.set_scope(scope_id)
        self._current_scope = scope_id
        if scope_id not in self._scopes:
            self._scopes[scope_id] = []
        logger.debug(f"Scope started: {scope_id}")
    
    def end_scope(self, scope_id: str) -> None:
        """
        End a scope and release all scoped services.
        
        Args:
            scope_id: The scope to end
        """
        if scope_id in self._scopes:
            # Release all services created in this scope
            for key in self._scopes[scope_id]:
                pass  # Would call release here
            del self._scopes[scope_id]
        
        self._resolver.clear_scope(scope_id)
        if self._current_scope == scope_id:
            self._current_scope = None
        logger.debug(f"Scope ended: {scope_id}")
    
    # Hooks
    
    def add_hook(
        self,
        hook_type: HookType,
        callback: Any,
        service_type: Type | None = None,
        name: str | None = None,
    ) -> None:
        """Add a lifecycle hook."""
        self._hook_registry.register(hook_type, callback, service_type, name)
    
    def remove_hook(
        self,
        hook_type: HookType,
        callback: Any,
    ) -> None:
        """Remove a lifecycle hook."""
        self._hook_registry.unregister(hook_type, callback)
    
    # Validation
    
    def validate(self) -> dict[str, list[str]]:
        """
        Validate the container configuration.
        
        Returns:
            Dictionary mapping registration keys to validation errors
        """
        validator = ContainerValidator(self)
        return validator.validate_all()
    
    # Utilities
    
    def _build_key(self, service_type: Type, name: str | None) -> str:
        """Build a registration key from type and name."""
        if name:
            return f"{service_type.__name__}:{name}"
        return service_type.__name__
    
    def is_registered(self, service_type: Type, name: str | None = None) -> bool:
        """Check if a service is registered."""
        key = self._build_key(service_type, name)
        return key in self._registrations
    
    def clear(self) -> None:
        """Clear all registrations and cached instances."""
        self._registrations.clear()
        self._resolver.clear_all()
        self._scopes.clear()
        self._current_scope = None


__all__ = [
    "DIContainer",
]
