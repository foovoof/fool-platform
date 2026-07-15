"""
fool_platform/events/dispatcher.py

Event dispatcher for delivering events to subscribers.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.exceptions import EventDispatchError
from fool_platform.events.router import EventRouter
from fool_platform.events.subscriber import EventSubscriber, HandlerResult, HandlerStatus

if TYPE_CHECKING:
    from fool_platform.events.metrics import EventMetrics


@dataclass
class DispatchError:
    """Error information from a failed dispatch."""
    subscriber_id: str
    event_id: str
    error: str

    def __str__(self) -> str:
        return f"{self.subscriber_id}: {self.error}"


@dataclass
class DispatchResult:
    """Result of a dispatch operation."""
    event_id: str
    event_type: str
    delivered_count: int
    failed_count: int
    handler_results: list[HandlerResult] = field(default_factory=list)
    errors: list[DispatchError] = field(default_factory=list)
    dispatched_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def success(self) -> bool:
        """Check if dispatch was completely successful."""
        return self.failed_count == 0

    @property
    def partial_failure(self) -> bool:
        """Check if dispatch had partial failures."""
        return self.delivered_count > 0 and self.failed_count > 0

    @classmethod
    def from_handler_results(
        cls,
        event: EventEnvelope,
        handler_results: list[HandlerResult],
    ) -> "DispatchResult":
        """Create a dispatch result from handler results."""
        errors = [
            DispatchError(
                subscriber_id=r.subscriber_id,
                event_id=r.event_id,
                error=r.error or "Unknown error",
            )
            for r in handler_results
            if r.status == HandlerStatus.FAILURE
        ]
        
        return cls(
            event_id=event.event_id,
            event_type=event.event_type,
            delivered_count=len([r for r in handler_results if r.status == HandlerStatus.SUCCESS]),
            failed_count=len([r for r in handler_results if r.status == HandlerStatus.FAILURE]),
            handler_results=handler_results,
            errors=errors,
        )


@dataclass
class EventDispatcher:
    """
    Dispatches events to registered subscribers.
    
    Thread-safe for concurrent dispatch and subscriber operations.
    Isolates subscriber errors to prevent cascade failures.
    """
    _router: EventRouter = field(default_factory=EventRouter)
    _metrics: "EventMetrics | None" = field(default=None, repr=False)
    _isolate_subscriber_errors: bool = True

    def register_subscriber(
        self,
        subscriber: EventSubscriber,
        pattern: str | None = None,
    ) -> None:
        """
        Register a subscriber for events.
        
        Args:
            subscriber: The subscriber to register
            pattern: Optional event type pattern (defaults to first supported type)
        """
        self._router.register(subscriber, pattern)
        if self._metrics:
            self._metrics.increment_subscribers()

    def unregister_subscriber(self, subscriber_id: str) -> bool:
        """
        Unregister a subscriber by ID.
        
        Args:
            subscriber_id: The subscriber ID to unregister
            
        Returns:
            True if the subscriber was found and removed
        """
        result = self._router.unregister(subscriber_id)
        if result and self._metrics:
            self._metrics.decrement_subscribers()
        return result

    def unregister_all_subscribers(self) -> int:
        """
        Unregister all subscribers.
        
        Returns:
            The number of subscribers unregistered
        """
        count = self._router.unregister_all()
        if self._metrics:
            self._metrics.registered_subscribers = 0
        return count

    def dispatch(self, event: EventEnvelope) -> DispatchResult:
        """
        Dispatch an event to all matching subscribers.
        
        A failing subscriber will not prevent other subscribers from receiving
        the event, unless _isolate_subscriber_errors is False.
        
        Args:
            event: The event to dispatch
            
        Returns:
            A DispatchResult with delivery information
        """
        subscribers = self._router.route(event.event_type)
        
        if self._metrics:
            self._metrics.increment_routed_events(len(subscribers))

        handler_results: list[HandlerResult] = []

        for subscriber in subscribers:
            result = self._deliver_to_subscriber(subscriber, event)
            handler_results.append(result)

        if self._metrics:
            success_count = len([r for r in handler_results if r.status == HandlerStatus.SUCCESS])
            self._metrics.increment_dispatched(success_count)
            
            failure_count = len([r for r in handler_results if r.status == HandlerStatus.FAILURE])
            if failure_count > 0:
                self._metrics.increment_failed_dispatches(failure_count)
                self._metrics.increment_subscriber_errors(failure_count)

        return DispatchResult.from_handler_results(event, handler_results)

    def dispatch_many(self, events: list[EventEnvelope]) -> list[DispatchResult]:
        """
        Dispatch multiple events.
        
        Args:
            events: The events to dispatch
            
        Returns:
            List of DispatchResults in the same order as input events
        """
        results = []
        for event in events:
            results.append(self.dispatch(event))
        return results

    def _deliver_to_subscriber(
        self,
        subscriber: EventSubscriber,
        event: EventEnvelope,
    ) -> HandlerResult:
        """
        Deliver an event to a single subscriber.
        
        Args:
            subscriber: The subscriber to deliver to
            event: The event to deliver
            
        Returns:
            A HandlerResult indicating success or failure
        """
        if not subscriber.enabled:
            return HandlerResult.skipped(
                subscriber_id=subscriber.subscriber_id,
                event_id=event.event_id,
                reason="Subscriber is disabled",
            )

        start_time = datetime.now(timezone.utc)

        try:
            result = subscriber.handle(event)
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            return HandlerResult(
                status=result.status if hasattr(result, 'status') else HandlerStatus.SUCCESS,
                subscriber_id=subscriber.subscriber_id,
                event_id=event.event_id,
                duration_ms=duration_ms,
                error=result.error if hasattr(result, 'error') else None,
                return_value=result.return_value if hasattr(result, 'return_value') else None,
            )

        except Exception as e:
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            subscriber.on_error(event, e)
            
            return HandlerResult.failure(
                subscriber_id=subscriber.subscriber_id,
                event_id=event.event_id,
                duration_ms=duration_ms,
                error=str(e),
            )

    def get_subscriber_count(self) -> int:
        """Get the number of registered subscribers."""
        return self._router.get_unique_subscriber_count()

    def has_subscribers(self) -> bool:
        """Check if any subscribers are registered."""
        return self._router.has_subscribers()

    def set_metrics(self, metrics: "EventMetrics | None") -> None:
        """Set or update the metrics."""
        self._metrics = metrics

    def set_isolate_subscriber_errors(self, isolate: bool) -> None:
        """Set whether to isolate subscriber errors."""
        self._isolate_subscriber_errors = isolate
