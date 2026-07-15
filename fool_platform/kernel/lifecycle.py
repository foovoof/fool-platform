"""
platform/kernel/lifecycle.py

Kernel lifecycle management and startup/shutdown coordination.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .kernel_events import KernelEvent, KernelEventBus, KernelEventType
from .kernel_exceptions import (
    KernelAlreadyStartedError,
    KernelNotStartedError,
    KernelShuttingDownError,
)
from .kernel_state import KernelState, KernelStateManager

if TYPE_CHECKING:
    from .runtime import Kernel

logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Manages kernel lifecycle transitions and coordinates startup/shutdown.
    
    Responsible for:
    - Validating state transitions
    - Coordinating startup sequence
    - Coordinating shutdown sequence
    - Emitting lifecycle events
    """
    
    def __init__(self, state_manager: KernelStateManager, event_bus: KernelEventBus) -> None:
        self._state_manager = state_manager
        self._event_bus = event_bus
        self._startup_order: list[str] = []
        self._shutdown_order: list[str] = []
    
    def register_startup_order(self, phase: str) -> None:
        """Register a phase in the startup order."""
        if phase not in self._startup_order:
            self._startup_order.append(phase)
    
    def register_shutdown_order(self, phase: str) -> None:
        """Register a phase in the shutdown order."""
        if phase not in self._shutdown_order:
            self._shutdown_order.append(phase)
    
    def begin_startup(self, kernel: "Kernel") -> None:
        """
        Begin kernel startup sequence.
        
        Args:
            kernel: The kernel instance
            
        Raises:
            KernelAlreadyStartedError: If kernel is already running
        """
        if self._state_manager.is_running:
            raise KernelAlreadyStartedError("Kernel is already running")
        
        if self._state_manager.state == KernelState.STOPPING:
            raise KernelShuttingDownError("Kernel is shutting down")
        
        # Transition to STARTING
        self._state_manager.transition_to(KernelState.STARTING)
        self._emit_event(
            KernelEventType.KERNEL_STARTING,
            kernel.kernel_id,
            {"phases": self._startup_order}
        )
        logger.info("Kernel startup initiated")
    
    def complete_startup(self, kernel: "Kernel") -> None:
        """
        Complete kernel startup sequence.
        
        Args:
            kernel: The kernel instance
        """
        self._state_manager.transition_to(KernelState.RUNNING)
        self._emit_event(
            KernelEventType.KERNEL_STARTED,
            kernel.kernel_id,
            {"phases_completed": self._startup_order}
        )
        logger.info("Kernel startup completed")
    
    def begin_shutdown(self, kernel: "Kernel", reason: str | None = None) -> None:
        """
        Begin kernel shutdown sequence.
        
        Args:
            kernel: The kernel instance
            reason: Optional reason for shutdown
            
        Raises:
            KernelNotStartedError: If kernel is not running
        """
        if not self._state_manager.is_running:
            raise KernelNotStartedError("Kernel is not running")
        
        # Transition to STOPPING
        self._state_manager.transition_to(KernelState.STOPPING)
        self._emit_event(
            KernelEventType.KERNEL_STOPPING,
            kernel.kernel_id,
            {"reason": reason, "phases": self._shutdown_order}
        )
        logger.info(f"Kernel shutdown initiated: {reason or 'no reason provided'}")
    
    def complete_shutdown(self, kernel: "Kernel") -> None:
        """
        Complete kernel shutdown sequence.
        
        Args:
            kernel: The kernel instance
        """
        self._state_manager.transition_to(KernelState.STOPPED)
        self._emit_event(
            KernelEventType.KERNEL_STOPPED,
            kernel.kernel_id,
            {"phases_completed": self._shutdown_order}
        )
        logger.info("Kernel shutdown completed")
    
    def fail(self, kernel: "Kernel", reason: str) -> None:
        """
        Transition kernel to failed state.
        
        Args:
            kernel: The kernel instance
            reason: Reason for failure
        """
        self._state_manager.transition_to(KernelState.FAILED, reason)
        self._emit_event(
            KernelEventType.KERNEL_FAILED,
            kernel.kernel_id,
            {"reason": reason}
        )
        logger.error(f"Kernel failed: {reason}")
    
    def _emit_event(self, event_type: KernelEventType, source: str, data: dict | None = None) -> None:
        """Emit a lifecycle event."""
        event = KernelEvent.create(event_type, source, data)
        self._event_bus.publish(event)
    
    @property
    def startup_phases(self) -> list[str]:
        """Return the registered startup phases in order."""
        return self._startup_order.copy()
    
    @property
    def shutdown_phases(self) -> list[str]:
        """Return the registered shutdown phases in order."""
        return self._shutdown_order.copy()


__all__ = [
    "LifecycleManager",
]
