"""
platform/kernel/kernel_interfaces.py

Abstract interfaces for kernel components.
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


class Service(ABC):
    """
    Base interface for all kernel services.
    
    Services implement business logic and can be registered
    in the dependency injection container.
    """
    
    @property
    @abstractmethod
    def service_name(self) -> str:
        """Unique name for this service."""
        ...


class Initializable(ABC):
    """
    Interface for components that require initialization.
    
    Implement this interface if your component needs to perform
    setup logic before it can be used.
    """
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the component. Called once during startup."""
        ...


class Disposable(ABC):
    """
    Interface for components that require cleanup.
    
    Implement this interface if your component holds resources
    that must be released during shutdown.
    """
    
    @abstractmethod
    def dispose(self) -> None:
        """Release all resources held by this component."""
        ...


class Startable(ABC):
    """
    Interface for components that can be started and stopped.
    
    Implement this interface if your component has a lifecycle
    that includes explicit start and stop phases.
    """
    
    @abstractmethod
    def start(self) -> None:
        """Start the component."""
        ...
    
    @abstractmethod
    def stop(self) -> None:
        """Stop the component."""
        ...


class KernelComponent(Initializable, Disposable, ABC):
    """
    Base class for kernel components.
    
    Combines initialization and disposal into a single interface.
    """
    pass


class HealthCheck(ABC):
    """
    Interface for health check implementations.
    
    Health checks are used to verify that the kernel and its
    components are functioning correctly.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of this health check."""
        ...
    
    @abstractmethod
    def check(self) -> bool:
        """
        Perform the health check.
        
        Returns:
            True if healthy, False otherwise.
        """
        ...
    
    @abstractmethod
    def details(self) -> dict[str, Any]:
        """
        Return detailed information about the health check.
        
        Returns:
            Dictionary with check details, status, and any error messages.
        """
        ...


__all__ = [
    "Disposable",
    "HealthCheck",
    "Initializable",
    "KernelComponent",
    "Service",
    "Startable",
]
