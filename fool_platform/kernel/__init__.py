"""
platform/kernel/__init__.py

FOOL Platform Kernel.

The kernel is the central runtime component that manages:
- Lifecycle (startup, running, shutdown)
- Application context
- Dependency injection container
- Health checks
- Registry access
- Event bus

This module provides the foundation for Phase 2 platform services.
"""
from .app_context import AppContext
from .bootstrapper import KernelBootstrapper
from .execution_context import (
    ExecutionContext,
    ExecutionContextManager,
    get_current_context,
    set_current_context,
)
from .health import (
    HealthCheckRegistry,
    HealthDiagnostics,
    HealthDiagnosticsCollector,
    HealthReport,
)
from .health_manager import HealthManager
from .kernel_config import Environment, KernelConfig
from .kernel_events import KernelEvent, KernelEventBus, KernelEventType
from .kernel_exceptions import (
    BootstrapError,
    CircularDependencyError,
    ConfigurationError,
    ConfigurationNotFoundError,
    ConfigurationValidationError,
    HealthCheckError,
    KernelAlreadyStartedError,
    KernelError,
    KernelNotStartedError,
    KernelShuttingDownError,
    KernelStateError,
    LivenessCheckFailedError,
    ReadinessCheckFailedError,
    RegistryError,
    RegistryLoadError,
    RegistryNotFoundError,
    ServiceNotFoundError,
    ServiceResolutionError,
    ShutdownCheckFailedError,
    StartupCheckFailedError,
)
from .kernel_interfaces import (
    Disposable,
    HealthCheck,
    Initializable,
    KernelComponent,
    Service,
    Startable,
)
from .kernel_state import KernelState, KernelStateManager
from .lifecycle import LifecycleManager
from .registry_manager import RegistryManager
from .runtime import Kernel

__all__ = [
    # Core
    "Kernel",
    "KernelBootstrapper",
    "KernelConfig",
    "KernelState",
    "KernelStateManager",
    "LifecycleManager",
    # Context
    "AppContext",
    "ExecutionContext",
    "ExecutionContextManager",
    "get_current_context",
    "set_current_context",
    # Config
    "Environment",
    # DI
    "CircularDependencyError",
    "ServiceNotFoundError",
    "ServiceResolutionError",
    # Events
    "KernelEvent",
    "KernelEventBus",
    "KernelEventType",
    # Exceptions
    "BootstrapError",
    "ConfigurationError",
    "ConfigurationNotFoundError",
    "ConfigurationValidationError",
    "HealthCheckError",
    "KernelAlreadyStartedError",
    "KernelError",
    "KernelNotStartedError",
    "KernelShuttingDownError",
    "KernelStateError",
    "LivenessCheckFailedError",
    "ReadinessCheckFailedError",
    "RegistryError",
    "RegistryLoadError",
    "RegistryNotFoundError",
    "ShutdownCheckFailedError",
    "StartupCheckFailedError",
    # Health
    "HealthCheck",
    "HealthCheckRegistry",
    "HealthDiagnostics",
    "HealthDiagnosticsCollector",
    "HealthManager",
    "HealthReport",
    # Interfaces
    "Disposable",
    "Initializable",
    "KernelComponent",
    "Service",
    "Startable",
    # Registry
    "RegistryManager",
]
