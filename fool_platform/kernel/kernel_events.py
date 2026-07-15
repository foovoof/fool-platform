"""
platform/kernel/kernel_events.py

Kernel lifecycle events.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .kernel_state import KernelState


class KernelEventType(Enum):
    """Types of kernel lifecycle events."""
    KERNEL_CREATED = "kernel.created"
    KERNEL_STARTING = "kernel.starting"
    KERNEL_STARTED = "kernel.started"
    KERNEL_STOPPING = "kernel.stopping"
    KERNEL_STOPPED = "kernel.stopped"
    KERNEL_FAILED = "kernel.failed"
    SERVICE_REGISTERED = "kernel.service.registered"
    SERVICE_UNREGISTERED = "kernel.service.unregistered"
    CONFIG_LOADED = "kernel.config.loaded"
    HEALTH_CHECKED = "kernel.health.checked"


@dataclass(frozen=True)
class KernelEvent:
    """
    Immutable kernel lifecycle event.
    
    Events are emitted during kernel lifecycle transitions
    for monitoring, logging, and debugging purposes.
    """
    event_type: KernelEventType
    timestamp: str
    source: str
    data: dict = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        event_type: KernelEventType,
        source: str,
        data: dict | None = None,
        timestamp: str | None = None,
    ) -> "KernelEvent":
        """Factory method to create a kernel event."""
        return cls(
            event_type=event_type,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
            source=source,
            data=data or {},
        )


class KernelEventBus:
    """
    Simple event bus for kernel lifecycle events.
    
    Provides publish-subscribe pattern for kernel events.
    Used by health checks, diagnostics, and monitoring.
    """
    
    def __init__(self) -> None:
        self._handlers: dict[KernelEventType, list[callable]] = {}
    
    def subscribe(self, event_type: KernelEventType, handler: callable) -> None:
        """Subscribe a handler to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: KernelEventType, handler: callable) -> None:
        """Unsubscribe a handler from an event type."""
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h != handler
            ]
    
    def publish(self, event: KernelEvent) -> None:
        """Publish an event to all subscribed handlers."""
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass  # Log but don't fail on handler errors
    
    def clear(self) -> None:
        """Clear all subscriptions."""
        self._handlers.clear()


__all__ = [
    "KernelEvent",
    "KernelEventType",
    "KernelEventBus",
]
