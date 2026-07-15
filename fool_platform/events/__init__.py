"""
fool_platform/events/__init__.py

FOOL Platform Event Bus - In-memory event communication backbone.

Phase 2B: Event Bus Foundation

This module provides the internal event communication infrastructure for FOOL Platform.
It is:
- contract-aware (reads event definitions from contracts/)
- version-aware (validates event versions)
- deterministic (preserves event ordering)
- thread-safe (protects concurrent operations)
- replayable (supports event replay from history)
- observable (in-memory metrics)
- lifecycle-aware (initialize/start/stop/reset/dispose)

This module intentionally does NOT include:
- External brokers (Kafka, RabbitMQ, NATS)
- Database persistence
- Network transport
- Real agents
- Workflow execution engine
- AI/LLM integrations
"""

from fool_platform.events.bus import EventBus
from fool_platform.events.context import EventContext
from fool_platform.events.dispatcher import (
    DispatchError,
    DispatchResult,
    EventDispatcher,
)
from fool_platform.events.envelope import EventEnvelope, ValidationStatus
from fool_platform.events.event_registry import EventDefinition, EventRegistry
from fool_platform.events.exceptions import (
    EventBusError,
    EventDispatchError,
    EventRegistryError,
    EventReplayError,
    EventRoutingError,
    EventSerializationError,
    EventSubscriberError,
    EventValidationError,
)
from fool_platform.events.history import EventHistory, InMemoryEventHistory
from fool_platform.events.lifecycle import (
    EventBusLifecycle,
    EventBusState,
    InvalidStateTransitionError,
)
from fool_platform.events.metadata import EventMetadata
from fool_platform.events.metrics import EventMetrics, EventMetricsSnapshot
from fool_platform.events.publisher import EventPublisher, PublishResult
from fool_platform.events.replay import EventReplay, InMemoryEventReplay, ReplayResult
from fool_platform.events.router import EventRouter, RoutingRule
from fool_platform.events.serialization import EventSerializer
from fool_platform.events.subscriber import (
    EventSubscriber,
    FunctionalEventSubscriber,
    HandlerResult,
    HandlerStatus,
    SubscriptionResult,
)
from fool_platform.events.validation import (
    EventValidator,
    ValidationError,
    ValidationResult,
)

__all__ = [
    # Core Bus
    "EventBus",
    
    # Envelope and Metadata
    "EventEnvelope",
    "EventMetadata",
    "EventContext",
    "ValidationStatus",
    
    # Dispatcher and Publisher
    "EventDispatcher",
    "EventPublisher",
    "PublishResult",
    "DispatchResult",
    "DispatchError",
    
    # Subscriber
    "EventSubscriber",
    "FunctionalEventSubscriber",
    "HandlerResult",
    "HandlerStatus",
    "SubscriptionResult",
    
    # Router
    "EventRouter",
    "RoutingRule",
    
    # Registry
    "EventRegistry",
    "EventDefinition",
    
    # Validation
    "EventValidator",
    "ValidationResult",
    "ValidationError",
    
    # Serialization
    "EventSerializer",
    
    # History
    "EventHistory",
    "InMemoryEventHistory",
    
    # Replay
    "EventReplay",
    "InMemoryEventReplay",
    "ReplayResult",
    
    # Lifecycle
    "EventBusLifecycle",
    "EventBusState",
    "InvalidStateTransitionError",
    
    # Metrics
    "EventMetrics",
    "EventMetricsSnapshot",
    
    # Exceptions
    "EventBusError",
    "EventValidationError",
    "EventDispatchError",
    "EventSerializationError",
    "EventReplayError",
    "EventRegistryError",
    "EventSubscriberError",
    "EventRoutingError",
]
