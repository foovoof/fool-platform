"""
fool_platform/events/subscriber.py

Event subscriber abstraction for the Event Bus.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.exceptions import EventSubscriberError


class HandlerStatus(str, Enum):
    """Status of a handler execution."""
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


@dataclass
class HandlerResult:
    """Result of a handler execution."""
    status: HandlerStatus
    subscriber_id: str
    event_id: str
    duration_ms: float
    error: str | None = None
    return_value: Any = None

    @classmethod
    def success(
        cls,
        subscriber_id: str,
        event_id: str,
        duration_ms: float,
        return_value: Any = None,
    ) -> "HandlerResult":
        """Create a successful handler result."""
        return cls(
            status=HandlerStatus.SUCCESS,
            subscriber_id=subscriber_id,
            event_id=event_id,
            duration_ms=duration_ms,
            error=None,
            return_value=return_value,
        )

    @classmethod
    def failure(
        cls,
        subscriber_id: str,
        event_id: str,
        duration_ms: float,
        error: str,
    ) -> "HandlerResult":
        """Create a failed handler result."""
        return cls(
            status=HandlerStatus.FAILURE,
            subscriber_id=subscriber_id,
            event_id=event_id,
            duration_ms=duration_ms,
            error=error,
            return_value=None,
        )

    @classmethod
    def skipped(
        cls,
        subscriber_id: str,
        event_id: str,
        reason: str,
    ) -> "HandlerResult":
        """Create a skipped handler result."""
        return cls(
            status=HandlerStatus.SKIPPED,
            subscriber_id=subscriber_id,
            event_id=event_id,
            duration_ms=0.0,
            error=reason,
            return_value=None,
        )


@dataclass
class SubscriptionResult:
    """Result of a subscription operation."""
    subscriber_id: str
    success: bool
    error: str | None = None
    registered_at: str | None = None

    @classmethod
    def success(cls, subscriber_id: str) -> "SubscriptionResult":
        """Create a successful subscription result."""
        return cls(
            subscriber_id=subscriber_id,
            success=True,
            error=None,
            registered_at=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def failure(cls, subscriber_id: str, error: str) -> "SubscriptionResult":
        """Create a failed subscription result."""
        return cls(
            subscriber_id=subscriber_id,
            success=False,
            error=error,
            registered_at=None,
        )


class EventSubscriber(ABC):
    """
    Abstract base class for event subscribers.
    
    Implement the handle() method to process events.
    """
    
    @property
    @abstractmethod
    def subscriber_id(self) -> str:
        """Unique identifier for this subscriber."""
        pass

    @property
    @abstractmethod
    def supported_event_types(self) -> list[str]:
        """
        List of event types this subscriber supports.
        
        Can include wildcard patterns like "case.*", "agent.*", etc.
        """
        pass

    @property
    def enabled(self) -> bool:
        """Whether this subscriber is enabled to receive events."""
        return getattr(self, "_enabled", True)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether this subscriber is enabled."""
        self._enabled = value

    @property
    def metadata(self) -> dict[str, Any]:
        """Additional metadata for this subscriber."""
        return getattr(self, "_metadata", {})

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None:
        """Set additional metadata for this subscriber."""
        self._metadata = value

    @abstractmethod
    def handle(self, event: EventEnvelope) -> HandlerResult:
        """
        Handle an incoming event.
        
        Args:
            event: The event envelope to process
            
        Returns:
            A HandlerResult indicating success or failure
            
        Raises:
            Exception: Subclasses may raise exceptions which will be caught
                       and converted to HandlerResult failures
        """
        pass

    def on_error(self, event: EventEnvelope, error: Exception) -> None:
        """
        Callback when event handling fails.
        
        Override this method to implement custom error handling.
        
        Args:
            event: The event that caused the error
            error: The exception that was raised
        """
        pass

    def supports_event(self, event_type: str) -> bool:
        """
        Check if this subscriber supports the given event type.
        
        Args:
            event_type: The event type to check
            
        Returns:
            True if this subscriber handles this event type
        """
        for pattern in self.supported_event_types:
            if pattern == "*" or pattern == event_type:
                return True
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(event_type, pattern):
                    return True
        return False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"subscriber_id={self.subscriber_id!r}, "
            f"supported_event_types={self.supported_event_types!r}, "
            f"enabled={self.enabled!r})"
        )


class FunctionalEventSubscriber(EventSubscriber):
    """
    Event subscriber that wraps a callable.
    
    Useful for simple subscribers without creating a full class.
    """
    
    def __init__(
        self,
        subscriber_id: str,
        handler: callable,
        supported_event_types: list[str],
        enabled: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self._subscriber_id = subscriber_id
        self._handler = handler
        self._supported_event_types = supported_event_types
        self._enabled = enabled
        self._metadata = metadata or {}

    @property
    def subscriber_id(self) -> str:
        return self._subscriber_id

    @property
    def supported_event_types(self) -> list[str]:
        return self._supported_event_types

    def handle(self, event: EventEnvelope) -> HandlerResult:
        start_time = datetime.now(timezone.utc)
        try:
            result = self._handler(event)
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            return HandlerResult.success(
                subscriber_id=self.subscriber_id,
                event_id=event.event_id,
                duration_ms=duration_ms,
                return_value=result,
            )
        except Exception as e:
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            return HandlerResult.failure(
                subscriber_id=self.subscriber_id,
                event_id=event.event_id,
                duration_ms=duration_ms,
                error=str(e),
            )
