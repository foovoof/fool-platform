"""
fool_platform/events/bus.py

Integrated Event Bus facade.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from fool_platform.events.dispatcher import EventDispatcher
from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.event_registry import EventRegistry
from fool_platform.events.exceptions import EventBusError
from fool_platform.events.lifecycle import InvalidStateTransitionError
from fool_platform.events.history import EventHistory, InMemoryEventHistory
from fool_platform.events.lifecycle import EventBusLifecycle, EventBusState
from fool_platform.events.metrics import EventMetrics, EventMetricsSnapshot
from fool_platform.events.publisher import EventPublisher
from fool_platform.events.replay import EventReplay, InMemoryEventReplay
from fool_platform.events.router import EventRouter
from fool_platform.events.subscriber import EventSubscriber
from fool_platform.events.validation import EventValidator

if TYPE_CHECKING:
    from fool_platform.events.serialization import EventSerializer


@dataclass
class EventBus:
    """
    Integrated in-memory Event Bus for FOOL Platform.
    
    Coordinates all event bus components:
    - Registry: Event type definitions
    - Validator: Event validation
    - Router: Event routing to subscribers
    - Dispatcher: Event delivery to subscribers
    - History: Event storage
    - Replay: Event replay functionality
    - Metrics: In-memory metrics
    - Lifecycle: State management
    
    Thread-safe for concurrent publish and subscribe operations.
    Dependency injection friendly.
    No hidden global singleton.
    """
    _registry: EventRegistry | None = field(default=None)
    _validator: EventValidator = field(default_factory=EventValidator)
    _router: EventRouter = field(default_factory=EventRouter)
    _dispatcher: EventDispatcher = field(default_factory=EventDispatcher)
    _history: EventHistory = field(default_factory=InMemoryEventHistory)
    _replay: InMemoryEventReplay = field(default=None)
    _metrics: EventMetrics = field(default_factory=EventMetrics)
    _lifecycle: EventBusLifecycle = field(default_factory=EventBusLifecycle)
    _publisher: EventPublisher = field(default=None)
    _serializer: "EventSerializer | None" = field(default=None)
    _validate_before_publish: bool = False
    _store_in_history: bool = True

    def __post_init__(self) -> None:
        """Initialize derived components."""
        self._replay = InMemoryEventReplay(
            _history=self._history,
            _dispatcher=self._dispatcher,
            _metrics=self._metrics,
        )
        self._publisher = EventPublisher()
        self._publisher.configure(
            dispatcher=self._dispatcher,
            history=self._history,
            validator=self._validator if self._validate_before_publish else None,
            lifecycle=self._lifecycle,
            metrics=self._metrics,
            validate_before_publish=self._validate_before_publish,
            store_in_history=self._store_in_history,
        )
        self._validator.set_registry(self._registry)
        self._dispatcher.set_metrics(self._metrics)

    @classmethod
    def create(
        cls,
        contracts_path: Path | None = None,
        standards_path: Path | None = None,
        validate_before_publish: bool = False,
        store_in_history: bool = True,
    ) -> "EventBus":
        """
        Create a new EventBus instance.
        
        Args:
            contracts_path: Path to contracts/events/ directory
            standards_path: Path to standards/events/ directory
            validate_before_publish: Whether to validate before publishing
            store_in_history: Whether to store events in history
            
        Returns:
            A new EventBus instance
        """
        registry = None
        if contracts_path or standards_path:
            registry = EventRegistry(
                contracts_path=contracts_path,
                standards_path=standards_path,
            )
        
        validator = EventValidator()
        if registry:
            validator.set_registry(registry)
        
        bus = cls(
            _registry=registry,
            _validator=validator,
            _validate_before_publish=validate_before_publish,
            _store_in_history=store_in_history,
        )
        return bus

    def publish(self, event: EventEnvelope) -> "EventPublisher":
        """
        Publish an event.
        
        Args:
            event: The event to publish
            
        Returns:
            A PublishResult indicating success or failure
            
        Raises:
            InvalidStateTransitionError: If the Event Bus cannot accept events
        """
        self._lifecycle.ensure_can_publish()
        return self._publisher.publish(event)

    def publish_many(self, events: list[EventEnvelope]) -> list:
        """
        Publish multiple events.
        
        Args:
            events: The events to publish
            
        Returns:
            List of PublishResults
        """
        self._lifecycle.ensure_can_publish()
        return self._publisher.publish_many(events)

    def subscribe(
        self,
        subscriber: EventSubscriber,
        pattern: str | None = None,
    ) -> None:
        """
        Subscribe to events.
        
        Args:
            subscriber: The subscriber to register
            pattern: Optional event type pattern
        """
        self._dispatcher.register_subscriber(subscriber, pattern)

    def unsubscribe(self, subscriber_id: str) -> bool:
        """
        Unsubscribe from events.
        
        Args:
            subscriber_id: The subscriber ID to unregister
            
        Returns:
            True if the subscriber was found
        """
        return self._dispatcher.unregister_subscriber(subscriber_id)

    def replay_all(self) -> "EventReplay":
        """
        Replay all events.
        
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay.replay_all()

    def replay_by_type(self, event_type: str) -> "EventReplay":
        """
        Replay events by type.
        
        Args:
            event_type: The event type to replay
            
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay.replay_by_type(event_type)

    def replay_by_correlation_id(self, correlation_id: str) -> "EventReplay":
        """
        Replay events by correlation ID.
        
        Args:
            correlation_id: The correlation ID to replay
            
        Returns:
            A ReplayResult with the outcome
        """
        return self._replay.replay_by_correlation_id(correlation_id)

    def get_history(self) -> EventHistory:
        """Get the event history."""
        return self._history

    def get_metrics(self) -> EventMetricsSnapshot:
        """Get a snapshot of current metrics."""
        return EventMetricsSnapshot(self._metrics)

    def list_event_types(self) -> list[str]:
        """
        List all registered event types.
        
        Returns:
            List of event type names
        """
        if self._registry:
            return self._registry.list_event_types()
        return []

    def validate_event(
        self,
        event: EventEnvelope,
    ) -> "EventValidator":
        """
        Validate an event.
        
        Args:
            event: The event to validate
            
        Returns:
            A ValidationResult
        """
        return self._validator.validate_envelope(event)

    def initialize(self) -> None:
        """
        Initialize the Event Bus.
        
        Required before start(). Can be called after stop() to reinitialize.
        """
        self._lifecycle.initialize()

    def start(self) -> None:
        """
        Start the Event Bus.
        
        Enables publishing and dispatching.
        """
        self._lifecycle.start()

    def stop(self) -> None:
        """
        Stop the Event Bus.
        
        Prevents new dispatches but preserves history.
        """
        self._lifecycle.stop()

    def reset(self) -> None:
        """
        Reset the Event Bus.
        
        Clears in-memory state including history.
        """
        self._lifecycle.reset()
        self._history.clear()
        self._metrics.reset()

    def dispose(self) -> None:
        """
        Dispose the Event Bus permanently.
        
        After disposal, the Event Bus cannot accept new events.
        """
        self._lifecycle.dispose()

    @property
    def state(self) -> EventBusState:
        """Get the current lifecycle state."""
        return self._lifecycle.state

    @property
    def is_running(self) -> bool:
        """Check if the Event Bus is running."""
        return self._lifecycle.is_running

    @property
    def is_disposed(self) -> bool:
        """Check if the Event Bus is disposed."""
        return self._lifecycle.is_disposed

    def __repr__(self) -> str:
        return (
            f"EventBus("
            f"state={self.state.value}, "
            f"subscribers={self._dispatcher.get_subscriber_count()}, "
            f"history_size={self._history.count()})"
        )
