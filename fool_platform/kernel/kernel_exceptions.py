"""
platform/kernel/kernel_exceptions.py

Kernel exception hierarchy for the FOOL Platform.
"""


class KernelError(Exception):
    """Base exception for all kernel errors."""
    pass


class KernelStateError(KernelError):
    """Raised when an operation is invalid for the current kernel state."""
    pass


class KernelNotStartedError(KernelStateError):
    """Raised when the kernel is not started."""
    pass


class KernelAlreadyStartedError(KernelStateError):
    """Raised when the kernel is already started."""
    pass


class KernelShuttingDownError(KernelStateError):
    """Raised when the kernel is shutting down."""
    pass


class ServiceResolutionError(KernelError):
    """Raised when a service cannot be resolved."""
    pass


class ServiceNotFoundError(ServiceResolutionError):
    """Raised when a requested service is not registered."""
    pass


class CircularDependencyError(ServiceResolutionError):
    """Raised when a circular dependency is detected during resolution."""
    pass


class ConfigurationError(KernelError):
    """Base exception for configuration errors."""
    pass


class ConfigurationValidationError(ConfigurationError):
    """Raised when configuration validation fails."""
    pass


class ConfigurationNotFoundError(ConfigurationError):
    """Raised when a required configuration is not found."""
    pass


class HealthCheckError(KernelError):
    """Base exception for health check failures."""
    pass


class LivenessCheckFailedError(HealthCheckError):
    """Raised when a liveness check fails."""
    pass


class ReadinessCheckFailedError(HealthCheckError):
    """Raised when a readiness check fails."""
    pass


class StartupCheckFailedError(HealthCheckError):
    """Raised when a startup check fails."""
    pass


class ShutdownCheckFailedError(HealthCheckError):
    """Raised when a shutdown check fails."""
    pass


class RegistryError(KernelError):
    """Base exception for registry errors."""
    pass


class RegistryLoadError(RegistryError):
    """Raised when registry loading fails."""
    pass


class RegistryNotFoundError(RegistryError):
    """Raised when a registry entry is not found."""
    pass


class BootstrapError(KernelError):
    """Raised when bootstrap fails."""
    pass


__all__ = [
    "BootstrapError",
    "CircularDependencyError",
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
    "ServiceNotFoundError",
    "ServiceResolutionError",
    "ShutdownCheckFailedError",
    "StartupCheckFailedError",
]
