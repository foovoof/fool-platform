"""
platform/kernel/bootstrapper.py

Kernel bootstrapper for initializing kernel services.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .kernel_events import KernelEventType
from .kernel_exceptions import BootstrapError
from .kernel_state import KernelState

if TYPE_CHECKING:
    from .runtime import Kernel

logger = logging.getLogger(__name__)


class KernelBootstrapper:
    """
    Bootstraps the kernel by initializing all required services.
    
    The bootstrapper follows a defined phase order:
    1. Configuration loading
    2. Registry initialization
    3. Health system initialization
    4. DI container setup
    5. Service initialization
    """
    
    def __init__(self, kernel: "Kernel") -> None:
        self._kernel = kernel
        self._phases: list[str] = []
        self._initialized = False
        self._disposed = False
    
    def bootstrap(self) -> None:
        """
        Perform full kernel bootstrap sequence.
        
        Raises:
            BootstrapError: If any bootstrap phase fails
        """
        if self._initialized:
            logger.warning("Kernel already bootstrapped")
            return
        
        try:
            logger.info("Starting kernel bootstrap sequence")
            
            # Phase 1: Initialize configuration
            self._init_configuration()
            
            # Phase 2: Initialize registries
            self._init_registries()
            
            # Phase 3: Initialize health system
            self._init_health()
            
            # Phase 4: Initialize DI container
            self._init_di_container()
            
            # Phase 5: Initialize services
            self._init_services()
            
            self._initialized = True
            logger.info("Kernel bootstrap sequence completed successfully")
            
        except Exception as e:
            logger.error(f"Bootstrap failed: {e}")
            raise BootstrapError(f"Kernel bootstrap failed: {e}") from e
    
    def cleanup(self) -> None:
        """
        Cleanup kernel services during shutdown.
        
        Disposes services in reverse order of initialization.
        """
        if self._disposed:
            logger.warning("Kernel already disposed")
            return
        
        logger.info("Starting kernel cleanup sequence")
        
        try:
            # Dispose services in reverse order
            # (implementation would iterate through registered disposables)
            
            self._disposed = True
            logger.info("Kernel cleanup sequence completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            raise BootstrapError(f"Kernel cleanup failed: {e}") from e
    
    def _init_configuration(self) -> None:
        """Initialize configuration loading."""
        self._phases.append("configuration")
        logger.debug("Bootstrap phase: configuration")
        
        # Configuration is already loaded from KernelConfig
        self._emit_event("configuration_loaded", {
            "environment": self._kernel.config.environment.value
        })
    
    def _init_registries(self) -> None:
        """Initialize registry loaders."""
        self._phases.append("registries")
        logger.debug("Bootstrap phase: registries")
        
        from .registry_manager import RegistryManager
        registry_manager = RegistryManager(self._kernel.config)
        registry_manager.initialize()
        
        self._emit_event("registries_initialized", {
            "registry_paths": list(self._kernel.config.registry_paths.keys())
        })
    
    def _init_health(self) -> None:
        """Initialize health check system."""
        self._phases.append("health")
        logger.debug("Bootstrap phase: health")
        
        from .health_manager import HealthManager
        health_manager = HealthManager()
        health_manager.initialize()
        
        self._emit_event("health_system_initialized", {})
    
    def _init_di_container(self) -> None:
        """Initialize dependency injection container."""
        self._phases.append("di_container")
        logger.debug("Bootstrap phase: di_container")
        
        from .di.container import DIContainer
        container = DIContainer()
        
        self._emit_event("di_container_initialized", {})
    
    def _init_services(self) -> None:
        """Initialize registered services."""
        self._phases.append("services")
        logger.debug("Bootstrap phase: services")
        
        self._emit_event("services_initialized", {
            "services": []
        })
    
    def _emit_event(self, phase: str, data: dict) -> None:
        """Emit a bootstrap event."""
        event = KernelEventType.KERNEL_STARTED
        self._kernel.event_bus.publish(
            type(event).create(event, self._kernel.kernel_id, data)
        )
    
    @property
    def phases_completed(self) -> list[str]:
        """Return list of bootstrap phases that completed."""
        return self._phases.copy()


__all__ = [
    "KernelBootstrapper",
]
