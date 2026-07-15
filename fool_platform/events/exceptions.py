"""
fool_platform/events/exceptions.py

Dedicated exceptions for the Event Bus layer.
"""
from typing import Any


class EventBusError(Exception):
    """Base exception for all Event Bus errors."""
    pass


class EventValidationError(EventBusError):
    """Raised when event validation fails."""

    def __init__(
        self,
        message: str,
        event_id: str | None = None,
        event_type: str | None = None,
        errors: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.event_id = event_id
        self.event_type = event_type
        self.errors = errors or []

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.event_id:
            parts.append(f"event_id={self.event_id}")
        if self.event_type:
            parts.append(f"event_type={self.event_type}")
        if self.errors:
            parts.append(f"errors={self.errors}")
        return ", ".join(parts)


class EventDispatchError(EventBusError):
    """Raised when event dispatch fails."""

    def __init__(
        self,
        message: str,
        event_id: str | None = None,
        subscriber_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.event_id = event_id
        self.subscriber_id = subscriber_id
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.event_id:
            parts.append(f"event_id={self.event_id}")
        if self.subscriber_id:
            parts.append(f"subscriber_id={self.subscriber_id}")
        return ", ".join(parts)


class EventSerializationError(EventBusError):
    """Raised when event serialization or deserialization fails."""

    def __init__(
        self,
        message: str,
        event_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.event_id = event_id
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.event_id:
            parts.append(f"event_id={self.event_id}")
        return ", ".join(parts)


class EventReplayError(EventBusError):
    """Raised when event replay fails."""

    def __init__(
        self,
        message: str,
        replay_type: str | None = None,
        events_replayed: int = 0,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.replay_type = replay_type
        self.events_replayed = events_replayed
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.replay_type:
            parts.append(f"replay_type={self.replay_type}")
        parts.append(f"events_replayed={self.events_replayed}")
        return ", ".join(parts)


class EventRegistryError(EventBusError):
    """Raised when event registry operations fail."""

    def __init__(
        self,
        message: str,
        event_type: str | None = None,
        event_version: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.event_type = event_type
        self.event_version = event_version
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.event_type:
            parts.append(f"event_type={self.event_type}")
        if self.event_version:
            parts.append(f"event_version={self.event_version}")
        return ", ".join(parts)


class EventSubscriberError(EventBusError):
    """Raised when event subscriber operations fail."""

    def __init__(
        self,
        message: str,
        subscriber_id: str | None = None,
        event_type: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.subscriber_id = subscriber_id
        self.event_type = event_type
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.subscriber_id:
            parts.append(f"subscriber_id={self.subscriber_id}")
        if self.event_type:
            parts.append(f"event_type={self.event_type}")
        return ", ".join(parts)


class EventRoutingError(EventBusError):
    """Raised when event routing fails."""

    def __init__(
        self,
        message: str,
        event_type: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.event_type = event_type
        self.cause = cause

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.event_type:
            parts.append(f"event_type={self.event_type}")
        return ", ".join(parts)
