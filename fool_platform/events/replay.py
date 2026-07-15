"""
fool_platform/events/replay.py

Event replay functionality for the Event Bus.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Iterator

from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.exceptions import EventReplayError
from fool_platform.events.history import EventHistory

if TYPE_CHECKING:
    from fool_platform.events.dispatcher import EventDispatcher
    from fool_platform.events.metrics import EventMetrics


@dataclass
class ReplayResult:
    """Result of a replay operation."""
    replayed_count: int
    failed_count: int
    errors: list[str] = field(default_factory=list)
    replayed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    replay_type: str = "unknown"

    @classmethod
    def success(
        cls,
        replayed_count: int,
        replay_type: str = "unknown",
    ) -> "ReplayResult":
        """Create a successful replay result."""
        return cls(
            replayed_count=replayed_count,
            failed_count=0,
            errors=[],
            replayed_at=datetime.now(timezone.utc).isoformat(),
            replay_type=replay_type,
        )

    @classmethod
    def failure(
        cls,
        errors: list[str],
        replayed_count: int = 0,
        replay_type: str = "unknown",
    ) -> "ReplayResult":
        """Create a failed replay result."""
        return cls(
            replayed_count=replayed_count,
            failed_count=len(errors),
            errors=errors,
            replayed_at=datetime.now(timezone.utc).isoformat(),
            replay_type=replay_type,
        )


class EventReplay(ABC):
    """
    Abstract interface for event replay.
    
    Implement this interface for different replay strategies.
    """
    
    @abstractmethod
    def replay_all(self) -> ReplayResult:
        """Replay all events from history."""
        pass

    @abstractmethod
    def replay_by_type(self, event_type: str) -> ReplayResult:
        """Replay events by type."""
        pass

    @abstractmethod
    def replay_by_correlation_id(self, correlation_id: str) -> ReplayResult:
        """Replay events by correlation ID."""
        pass


@dataclass
class InMemoryEventReplay(EventReplay):
    """
    In-memory event replay implementation.
    
    Replays events from history while preserving original metadata and ordering.
    """
    _history: EventHistory
    _dispatcher: "EventDispatcher | None" = field(default=None, repr=False)
    _metrics: "EventMetrics | None" = field(default=None, repr=False)
    _preserve_order: bool = True

    def replay_all(self) -> ReplayResult:
        """
        Replay all events from history.
        
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay(
            self._history.list_events(),
            "all",
        )

    def replay_by_type(self, event_type: str) -> ReplayResult:
        """
        Replay events by type.
        
        Args:
            event_type: The event type to replay
            
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay(
            self._history.find_by_type(event_type),
            f"type:{event_type}",
        )

    def replay_by_correlation_id(self, correlation_id: str) -> ReplayResult:
        """
        Replay events by correlation ID.
        
        Args:
            correlation_id: The correlation ID to replay
            
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay(
            self._history.find_by_correlation_id(correlation_id),
            f"correlation:{correlation_id}",
        )

    def replay_events(self, events: list[EventEnvelope]) -> ReplayResult:
        """
        Replay a specific list of events.
        
        Args:
            events: The events to replay
            
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay(events, "custom")

    def _replay(
        self,
        events: list[EventEnvelope],
        replay_type: str,
    ) -> ReplayResult:
        """
        Internal replay implementation.
        
        Args:
            events: The events to replay
            replay_type: The type of replay for reporting
            
        Returns:
            A ReplayResult with the outcome
        """
        if self._dispatcher is None:
            return ReplayResult.failure(
                errors=["No dispatcher configured"],
                replay_type=replay_type,
            )

        errors: list[str] = []
        replayed_count = 0

        for event in events:
            try:
                dispatch_result = self._dispatcher.dispatch(event)
                replayed_count += 1
            except Exception as e:
                errors.append(f"Event {event.event_id}: {str(e)}")

        if self._metrics:
            self._metrics.increment_replay_operations()

        if errors:
            return ReplayResult.failure(
                errors=errors,
                replayed_count=replayed_count,
                replay_type=replay_type,
            )

        return ReplayResult.success(
            replayed_count=replayed_count,
            replay_type=replay_type,
        )

    def set_dispatcher(self, dispatcher: "EventDispatcher | None") -> None:
        """Set or update the dispatcher."""
        self._dispatcher = dispatcher

    def set_metrics(self, metrics: "EventMetrics | None") -> None:
        """Set or update the metrics."""
        self._metrics = metrics

    def set_preserve_order(self, preserve: bool) -> None:
        """Set whether to preserve event order during replay."""
        self._preserve_order = preserve
