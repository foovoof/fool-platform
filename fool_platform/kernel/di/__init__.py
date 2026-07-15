"""
platform/kernel/di/__init__.py

Dependency Injection container and related components.
"""
from .container import DIContainer
from .hooks import HookExecutor, HookRegistry, HookType, LifecycleHook
from .lifetime import LifetimeManager, ServiceLifetime
from .registration import (
    ServiceFactory,
    ServiceRegistration,
    ServiceRegistrationBuilder,
)
from .resolution import DependencyResolver
from .validation import ContainerValidator, RegistrationValidator

__all__ = [
    "ContainerValidator",
    "DIContainer",
    "DependencyResolver",
    "HookExecutor",
    "HookRegistry",
    "HookType",
    "LifetimeManager",
    "LifecycleHook",
    "RegistrationValidator",
    "ServiceFactory",
    "ServiceLifetime",
    "ServiceRegistration",
    "ServiceRegistrationBuilder",
]
