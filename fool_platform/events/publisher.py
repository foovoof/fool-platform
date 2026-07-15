"""
fool_platform/events/publisher.py

Event publisher abstraction for the Event Bus.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.exceptions import EventBusError
from fool_platform.events.validation import EventValidator

if TYPE_CHECKING:
    from fool_platform.events.dispatcher import EventDispatcher
    from fool_platform.events.history import EventHistory
    from fool_platform.events.lifecycle import EventBusLifecycle
    from fool_platform.events.metrics import EventMetrics


@dataclass
class PublishResult:
    """Result of a publish operation."""
    success: bool
    event_id: str
    event_type: str
    validated: bool
    stored_in_history: bool
    dispatched_count: int
    dispatched_at: str
    error: str | None

    @classmethod
    def create_success(
        cls,
        event: EventEnvelope,
        validated: bool = False,
        stored_in_history: bool = False,
        dispatched_count: int = 0,
    ) -> "PublishResult":
        """Create a successful publish result."""
        return cls(
            success=True,
            event_id=event.event_id,
            event_type=event.event_type,
            validated=validated,
            stored_in_history=stored_in_history,
            dispatched_count=dispatched_count,
            dispatched_at=datetime.now(timezone.utc).isoformat(),
            error=None,
        )

    @classmethod
    def create_failure(
        cls,
        event: EventEnvelope,
        error: str,
    ) -> "PublishResult":
        """Create a failed publish result."""
        return cls(
            success=False,
            event_id=event.event_id,
            event_type=event.event_type,
            validated=False,
            stored_in_history=False,
            dispatched_count=0,
            dispatched_at=datetime.now(timezone.utc).isoformat(),
            error=error,
        )


@dataclass
class EventPublisher:
    """
    Publishes events to the Event Bus.
    
    Coordinates validation, history storage, and dispatching.
    Thread-safe for concurrent publish operations.
    """
    _validate_before_publish: bool = False
    _store_in_history: bool = True
    _dispatcher: "EventDispatcher | None" = None
    _history: "EventHistory | None" = None
    _validator: "EventValidator | None" = None
    _lifecycle: "EventBusLifecycle | None" = None
    _metrics: "EventMetrics | None" = None

    def publish(self, event: EventEnvelope) -> PublishResult:
        """
        Publish a single event.
        
        Args:
            event: The event envelope to publish
            
        Returns:
            A PublishResult indicating success or failure
            
        Raises:
            EventBusError: If the Event Bus is not in a valid state
        """
        if self._lifecycle:
            self._lifecycle.ensure_can_publish()

        try:
            if self._validate_before_publish and self._validator:
                validation_result = self._validator.validate_envelope(event)
                if not validation_result.valid:
                    self._metrics.increment_validation_failures()
                    return PublishResult.create_failure(
                        event,
                        f"Validation failed: {validation_result.errors}",
                    )

            if self._store_in_history and self._history:
                self._history.append(event)

            self._metrics.increment_published()

            if self._dispatcher:
                result = self._dispatcher.dispatch(event)
                return PublishResult.create_success(
                    event=event,
                    validated=self._validate_before_publish,
                    stored_in_history=self._store_in_history,
                    dispatched_count=result.delivered_count,
                )

            return PublishResult.create_success(
                event=event,
                validated=self._validate_before_publish,
                stored_in_history=self._store_in_history,
                dispatched_count=0,
            )

        except Exception as e:
            self._metrics.increment_failed_dispatches()
            return PublishResult.create_failure(event, str(e))

    def publish_many(self, events: list[EventEnvelope]) -> list[PublishResult]:
        """
        Publish multiple events.
        
        Args:
            events: List of event envelopes to publish
            
        Returns:
            List of PublishResults in the same order as input events
        """
        results = []
        for event in events:
            results.append(self.publish(event))
        return results

    def set_validator(self, validator: "EventValidator | None") -> None:
        """Set or update the validator."""
        self._validator = validator

    def set_validate_before_publish(self, enabled: bool) -> None:
        """Enable or disable validation before publishing."""
        self._validate_before_publish = enabled

    def set_store_in_history(self, enabled: bool) -> None:
        """Enable or disable storing events in history."""
        self._store_in_history = enabled

    def configure(
        self,
        dispatcher: "EventDispatcher | None" = None,
        history: "EventHistory | None" = None,
        validator: "EventValidator | None" = None,
        lifecycle: "EventBusLifecycle | None" = None,
        metrics: "EventMetrics | None" = None,
        validate_before_publish: bool = False,
        store_in_history: bool = True,
    ) -> None:
        """
        Configure the publisher with all dependencies.
        
        Args:
            dispatcher: The event dispatcher
            history: The event history
            validator: The event validator
            lifecycle: The event bus lifecycle
            metrics: The event metrics
            validate_before_publish: Whether to validate before publishing
            store_in_history: Whether to store in history
        """
        self._dispatcher = dispatcher
        self._history = history
        self._validator = validator
        self._lifecycle = lifecycle
        self._metrics = metrics
        self._validate_before_publish = validate_before_publish
        self._store_in_history = store_in_history
