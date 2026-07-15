"""
fool_platform/events/metrics.py

In-memory metrics for the Event Bus layer.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Iterator


@dataclass
class EventMetrics:
    """Thread-safe in-memory metrics container for the Event Bus."""
    published_events: int = 0
    dispatched_events: int = 0
    failed_dispatches: int = 0
    subscriber_errors: int = 0
    replay_operations: int = 0
    validation_failures: int = 0
    serialization_failures: int = 0
    registered_subscribers: int = 0
    routed_events: int = 0
    last_published_at: str | None = None
    last_dispatched_at: str | None = None
    last_failure_at: str | None = None
    _lock: Lock = field(default_factory=Lock, repr=False)

    def increment_published(self) -> None:
        """Increment published events counter."""
        with self._lock:
            self.published_events += 1
            self.last_published_at = datetime.now(timezone.utc).isoformat()

    def increment_dispatched(self, count: int = 1) -> None:
        """Increment dispatched events counter."""
        with self._lock:
            self.dispatched_events += count
            self.last_dispatched_at = datetime.now(timezone.utc).isoformat()

    def increment_failed_dispatches(self, count: int = 1) -> None:
        """Increment failed dispatches counter."""
        with self._lock:
            self.failed_dispatches += count
            self.last_failure_at = datetime.now(timezone.utc).isoformat()

    def increment_subscriber_errors(self, count: int = 1) -> None:
        """Increment subscriber errors counter."""
        with self._lock:
            self.subscriber_errors += count

    def increment_replay_operations(self, count: int = 1) -> None:
        """Increment replay operations counter."""
        with self._lock:
            self.replay_operations += count

    def increment_validation_failures(self, count: int = 1) -> None:
        """Increment validation failures counter."""
        with self._lock:
            self.validation_failures += count

    def increment_serialization_failures(self, count: int = 1) -> None:
        """Increment serialization failures counter."""
        with self._lock:
            self.serialization_failures += count

    def increment_subscribers(self, count: int = 1) -> None:
        """Increment registered subscribers counter."""
        with self._lock:
            self.registered_subscribers += count

    def decrement_subscribers(self, count: int = 1) -> None:
        """Decrement registered subscribers counter."""
        with self._lock:
            self.registered_subscribers = max(0, self.registered_subscribers - count)

    def increment_routed_events(self, count: int = 1) -> None:
        """Increment routed events counter."""
        with self._lock:
            self.routed_events += count

    def get_snapshot(self) -> dict:
        """Get a read-only snapshot of current metrics."""
        with self._lock:
            return {
                "published_events": self.published_events,
                "dispatched_events": self.dispatched_events,
                "failed_dispatches": self.failed_dispatches,
                "subscriber_errors": self.subscriber_errors,
                "replay_operations": self.replay_operations,
                "validation_failures": self.validation_failures,
                "serialization_failures": self.serialization_failures,
                "registered_subscribers": self.registered_subscribers,
                "routed_events": self.routed_events,
                "last_published_at": self.last_published_at,
                "last_dispatched_at": self.last_dispatched_at,
                "last_failure_at": self.last_failure_at,
            }

    def reset(self) -> None:
        """Reset all metrics to zero."""
        with self._lock:
            self.published_events = 0
            self.dispatched_events = 0
            self.failed_dispatches = 0
            self.subscriber_errors = 0
            self.replay_operations = 0
            self.validation_failures = 0
            self.serialization_failures = 0
            self.registered_subscribers = 0
            self.routed_events = 0
            self.last_published_at = None
            self.last_dispatched_at = None
            self.last_failure_at = None

    def __iter__(self) -> Iterator[tuple[str, int | str | None]]:
        """Iterate over metric name-value pairs."""
        for name, value in self.get_snapshot().items():
            yield name, value


class EventMetricsSnapshot:
    """Read-only snapshot of EventMetrics at a point in time."""
    
    def __init__(self, metrics: EventMetrics) -> None:
        self._data = metrics.get_snapshot()
        self._captured_at = datetime.now(timezone.utc).isoformat()

    @property
    def captured_at(self) -> str:
        """Get the timestamp when the snapshot was captured."""
        return self._captured_at

    def get(self, name: str) -> int | str | None:
        """Get a specific metric value by name."""
        return self._data.get(name)

    def __getitem__(self, name: str) -> int | str | None:
        """Get a specific metric value using bracket notation."""
        return self._data[name]

    def __contains__(self, name: str) -> bool:
        """Check if a metric exists in this snapshot."""
        return name in self._data

    def __iter__(self) -> Iterator[tuple[str, int | str | None]]:
        """Iterate over metric name-value pairs."""
        return iter(self._data.items())

    def __repr__(self) -> str:
        return f"EventMetricsSnapshot(captured_at={self._captured_at!r}, metrics={self._data!r})"
