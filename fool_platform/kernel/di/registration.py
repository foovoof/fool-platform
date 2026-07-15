"""
platform/kernel/di/registration.py

Service registration for dependency injection.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Type

if TYPE_CHECKING:
    from .lifetime import ServiceLifetime

ServiceFactory = Callable[..., Any]
"""Type alias for service factory functions."""


@dataclass(frozen=True)
class ServiceRegistration:
    """
    Immutable registration of a service in the DI container.
    
    Contains all information needed to create and manage service instances.
    """
    service_type: Type
    implementation_type: Type | None
    factory: ServiceFactory | None
    lifetime: "ServiceLifetime"
    name: str | None
    dependencies: tuple[str, ...]
    is_alias: bool = False
    
    def __post_init__(self) -> None:
        # Validate that either implementation_type or factory is provided
        if self.implementation_type is None and self.factory is None:
            raise ValueError(
                "Service registration must have either implementation_type or factory"
            )
    
    @property
    def key(self) -> str:
        """The key used to identify this registration."""
        if self.name:
            return f"{self.service_type.__name__}:{self.name}"
        return self.service_type.__name__


class ServiceRegistrationBuilder:
    """
    Builder for creating service registrations.
    
    Provides a fluent API for configuring service registration.
    """
    
    def __init__(self, service_type: Type) -> None:
        self._service_type = service_type
        self._implementation_type: Type | None = None
        self._factory: ServiceFactory | None = None
        self._lifetime: ServiceLifetime | None = None
        self._name: str | None = None
        self._dependencies: list[str] = []
    
    def to(self, implementation_type: Type) -> "ServiceRegistrationBuilder":
        """Specify the concrete implementation type."""
        self._implementation_type = implementation_type
        return self
    
    def factory(self, factory: ServiceFactory) -> "ServiceRegistrationBuilder":
        """Specify a factory function to create the service."""
        self._factory = factory
        return self
    
    def named(self, name: str) -> "ServiceRegistrationBuilder":
        """Specify a name for named registration."""
        self._name = name
        return self
    
    def depends_on(self, *dependencies: Type) -> "ServiceRegistrationBuilder":
        """Specify dependencies for this service."""
        self._dependencies = [d.__name__ for d in dependencies]
        return self
    
    def build(self, lifetime: "ServiceLifetime") -> ServiceRegistration:
        """Build the service registration."""
        if self._lifetime is None:
            self._lifetime = lifetime
        
        return ServiceRegistration(
            service_type=self._service_type,
            implementation_type=self._implementation_type,
            factory=self._factory,
            lifetime=self._lifetime,
            name=self._name,
            dependencies=tuple(self._dependencies),
        )
    
    def singleton(self) -> ServiceRegistration:
        """Build registration as singleton."""
        from .lifetime import ServiceLifetime
        return self.build(ServiceLifetime.SINGLETON)
    
    def transient(self) -> ServiceRegistration:
        """Build registration as transient."""
        from .lifetime import ServiceLifetime
        return self.build(ServiceLifetime.TRANSIENT)
    
    def scoped(self) -> ServiceRegistration:
        """Build registration as scoped."""
        from .lifetime import ServiceLifetime
        return self.build(ServiceLifetime.SCOPED)


__all__ = [
    "ServiceFactory",
    "ServiceRegistration",
    "ServiceRegistrationBuilder",
]
