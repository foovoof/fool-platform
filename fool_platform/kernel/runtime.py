"""
platform/kernel/runtime.py

FOOL Platform Kernel runtime.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .app_context import AppContext
from .kernel_config import KernelConfig
from .kernel_events import KernelEventBus, KernelEventType
from .kernel_exceptions import (
    KernelAlreadyStartedError,
    KernelNotStartedError,
    KernelShuttingDownError,
)
from .kernel_interfaces import HealthCheck
from .kernel_state import KernelState, KernelStateManager
from .lifecycle import LifecycleManager

if TYPE_CHECKING:
    from .bootstrapper import KernelBootstrapper

logger = logging.getLogger(__name__)


class Kernel:
    """
    The FOOL Platform Kernel.
    
    The kernel is the central runtime component that manages:
    - Lifecycle (startup, running, shutdown)
    - Application context
    - Dependency injection container
    - Health checks
    - Registry access
    - Event bus
    
    The kernel is the foundation on which all platform services are built.
    """
    
    def __init__(
        self,
        config: KernelConfig,
        bootstrapper: "KernelBootstrapper | None" = None,
    ) -> None:
        """
        Initialize the kernel.
        
        Args:
            config: Kernel configuration
            bootstrapper: Optional bootstrapper for custom initialization
        """
        self._config = config
        self._kernel_id = config.kernel_id or _generate_kernel_id()
        self._event_bus = KernelEventBus()
        self._state_manager = KernelStateManager()
        self._lifecycle = LifecycleManager(self._state_manager, self._event_bus)
        self._context: AppContext | None = None
        self._bootstrapper = bootstrapper
        
        # Emit created event
        self._emit_event(
            KernelEventType.KERNEL_CREATED,
            {"config": _config_summary(config)}
        )
        logger.info(f"Kernel {self._kernel_id} created for environment: {config.environment}")
    
    @property
    def kernel_id(self) -> str:
        """Unique kernel identifier."""
        return self._kernel_id
    
    @property
    def config(self) -> KernelConfig:
        """Kernel configuration."""
        return self._config
    
    @property
    def state(self) -> KernelState:
        """Current kernel state."""
        return self._state_manager.state
    
    @property
    def is_running(self) -> bool:
        """Returns True if kernel is running."""
        return self._state_manager.is_running
    
    @property
    def event_bus(self) -> KernelEventBus:
        """Kernel event bus."""
        return self._event_bus
    
    @property
    def app_context(self) -> AppContext | None:
        """Kernel application context."""
        return self._context
    
    def start(self) -> None:
        """
        Start the kernel.
        
        Performs the full startup sequence:
        1. Bootstrap configuration and services
        2. Initialize registered services
        3. Transition to RUNNING state
        
        Raises:
            KernelAlreadyStartedError: If kernel is already running
            KernelShuttingDownError: If kernel is shutting down
        """
        if self._state_manager.is_running:
            raise KernelAlreadyStartedError("Kernel is already running")
        
        if self._state_manager.state == KernelState.STOPPING:
            raise KernelShuttingDownError("Kernel is shutting down")
        
        try:
            self._lifecycle.begin_startup(self)
            
            # Bootstrap the kernel
            if self._bootstrapper is None:
                from .bootstrapper import KernelBootstrapper
                self._bootstrapper = KernelBootstrapper(self)
            
            self._bootstrapper.bootstrap()
            
            # Create app context
            self._context = AppContext.create(
                environment=self._config.environment.value,
                version=self._config.version,
            )
            
            self._lifecycle.complete_startup(self)
            logger.info(f"Kernel {self._kernel_id} started successfully")
            
        except Exception as e:
            self._lifecycle.fail(self, str(e))
            raise
    
    def stop(self, reason: str | None = None) -> None:
        """
        Stop the kernel.
        
        Performs the full shutdown sequence:
        1. Transition to STOPPING state
        2. Dispose all registered services
        3. Transition to STOPPED state
        
        Raises:
            KernelNotStartedError: If kernel is not running
        """
        if not self._state_manager.is_running:
            raise KernelNotStartedError("Kernel is not running")
        
        try:
            self._lifecycle.begin_shutdown(self, reason)
            
            # Bootstrapper handles cleanup
            if self._bootstrapper is not None:
                self._bootstrapper.cleanup()
            
            self._context = None
            self._lifecycle.complete_shutdown(self)
            logger.info(f"Kernel {self._kernel_id} stopped: {reason or 'no reason'}")
            
        except Exception as e:
            self._lifecycle.fail(self, str(e))
            raise
    
    def __enter__(self) -> "Kernel":
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        if self.is_running:
            self.stop(reason="context manager exit")
    
    def _emit_event(self, event_type: KernelEventType, data: dict | None = None) -> None:
        """Emit a kernel event."""
        event = KernelEvent.create(event_type, self._kernel_id, data)
        self._event_bus.publish(event)


def _generate_kernel_id() -> str:
    """Generate a unique kernel identifier."""
    import uuid
    return f"kernel-{uuid.uuid4().hex[:8]}"


def _config_summary(config: KernelConfig) -> dict:
    """Create a summary of the kernel configuration for logging."""
    return {
        "environment": config.environment.value,
        "version": config.version,
        "startup_timeout": config.startup_timeout_seconds,
        "shutdown_timeout": config.shutdown_timeout_seconds,
        "health_checks_enabled": config.enable_health_checks,
        "event_bus_enabled": config.enable_event_bus,
    }


__all__ = [
    "Kernel",
]
