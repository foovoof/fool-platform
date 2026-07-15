"""
platform/kernel/di/validation.py

Validation logic for dependency injection.
"""
from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Type

from .lifetime import ServiceLifetime
from .registration import ServiceRegistration

if TYPE_CHECKING:
    from .container import DIContainer


class RegistrationValidator:
    """
    Validates service registrations.
    
    Ensures registrations are well-formed and compatible
    with the DI container's capabilities.
    """
    
    @staticmethod
    def validate(registration: ServiceRegistration) -> list[str]:
        """
        Validate a service registration.
        
        Args:
            registration: The registration to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors: list[str] = []
        
        # Check service type
        if registration.service_type is None:
            errors.append("Service type is required")
        elif not isinstance(registration.service_type, type):
            errors.append("Service type must be a type/class")
        
        # Check implementation
        if registration.implementation_type is None and registration.factory is None:
            errors.append("Either implementation type or factory is required")
        
        if registration.implementation_type is not None:
            if not isinstance(registration.implementation_type, type):
                errors.append("Implementation type must be a type/class")
            
            # Check implementation is compatible with service type
            if registration.service_type is not None:
                if not issubclass(registration.implementation_type, registration.service_type):
                    errors.append(
                        f"Implementation {registration.implementation_type.__name__} "
                        f"is not a subclass of service type {registration.service_type.__name__}"
                    )
        
        # Check factory signature
        if registration.factory is not None:
            if not callable(registration.factory):
                errors.append("Factory must be callable")
        
        # Check lifetime
        if registration.lifetime is None:
            errors.append("Lifetime is required")
        
        return errors
    
    @staticmethod
    def validate_cycle(
        registrations: dict[str, ServiceRegistration],
        registration: ServiceRegistration,
    ) -> list[str]:
        """
        Check for circular dependencies.
        
        Args:
            registrations: All registrations in the container
            registration: The registration to check
            
        Returns:
            List of cycle errors (empty if no cycles)
        """
        errors: list[str] = []
        visited: set[str] = set()
        path: list[str] = []
        
        def visit(reg: ServiceRegistration) -> None:
            key = reg.key
            if key in path:
                cycle = " -> ".join(path + [key])
                errors.append(f"Circular dependency detected: {cycle}")
                return
            
            if key in visited:
                return
            
            path.append(key)
            visited.add(key)
            
            # Visit dependencies
            for dep_key in reg.dependencies:
                if dep_key in registrations:
                    visit(registrations[dep_key])
            
            path.pop()
        
        visit(registration)
        return errors


class ContainerValidator:
    """
    Validates the overall DI container configuration.
    """
    
    def __init__(self, container: "DIContainer") -> None:
        self._container = container
    
    def validate_all(self) -> dict[str, list[str]]:
        """
        Validate all registrations in the container.
        
        Returns:
            Dictionary mapping registration keys to validation errors
        """
        results: dict[str, list[str]] = {}
        registrations = self._container._registrations
        
        for key, reg in registrations.items():
            errors: list[str] = []
            
            # Validate registration itself
            errors.extend(RegistrationValidator.validate(reg))
            
            # Check for cycles
            errors.extend(
                RegistrationValidator.validate_cycle(dict(registrations), reg)
            )
            
            if errors:
                results[key] = errors
        
        return results
    
    def validate_resolvability(self) -> list[str]:
        """
        Validate that all registrations can be resolved.
        
        Returns:
            List of unresolved dependency errors
        """
        errors: list[str] = []
        registrations = self._container._registrations
        
        for key, reg in registrations.items():
            for dep_key in reg.dependencies:
                if dep_key not in registrations:
                    errors.append(
                        f"{key}: Unresolved dependency '{dep_key}'"
                    )
        
        return errors


__all__ = [
    "ContainerValidator",
    "RegistrationValidator",
]
