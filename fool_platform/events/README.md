# FOOL Platform Event Bus

## Overview

The Event Bus is the internal communication backbone of FOOL Platform, implementing a contract-aware, version-aware, deterministic, in-memory event distribution system.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Event Bus                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌───────────┐  ┌──────────┐  ┌─────────────────┐  │
│  │ Publisher│  │ Dispatcher│  │  Router  │  │ Event Registry  │  │
│  └────┬────┘  └─────┬─────┘  └────┬─────┘  └────────┬────────┘  │
│       │            │             │                  │           │
│       ▼            ▼             ▼                  ▼           │
│  ┌─────────┐  ┌──────────┐  ┌─────────────────────────────┐   │
│  │Validator│  │Subscriber│  │       Event History           │   │
│  └─────────┘  └──────────┘  └─────────────────────────────┘   │
│                                                                 │
│  ┌──────────┐  ┌─────────┐  ┌─────────┐  ┌────────────────┐  │
│  │ Metrics   │  │Lifecycle│  │Replay   │  │ Serialization   │  │
│  └──────────┘  └─────────┘  └─────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Event Model

### EventEnvelope

The core event representation wrapping metadata and payload:

```python
from fool_platform.events import EventEnvelope, EventMetadata

envelope = EventEnvelope.create_with_metadata(
    event_type="case.created",
    event_version="1.0.0",
    payload={"case_id": "case-123", "title": "Investigation"},
    correlation_id="corr-123",
    producer="workflow-engine",
)
```

### EventMetadata

Immutable metadata containing:

- `event_id` - Unique identifier (auto-generated UUID)
- `event_type` - Event type (e.g., "case.created")
- `event_version` - Schema version (e.g., "1.0.0")
- `occurred_at` - ISO 8601 timestamp
- `correlation_id` - For correlating related events
- `causation_id` - ID of the event that caused this one
- `trace_id` - For distributed tracing
- `producer` - Producer system/component
- `source` - Source system
- `subject` - Event subject
- `case_id` - Associated case (optional)
- `workflow_id` - Associated workflow (optional)
- `agent_id` - Associated agent (optional)
- `idempotency_key` - For duplicate detection (optional)
- `tags` - Categorization tags
- `attributes` - Custom attributes

## Event Versioning

The Event Bus supports event versions:

```python
# Events must specify a version
envelope = EventEnvelope.create_with_metadata(
    event_type="case.created",
    event_version="1.0.0",  # Required
    payload={},
)

# Registry can resolve event definitions
registry = EventRegistry(contracts_path=Path("contracts/events"))
registry.list_event_types()  # ["case.created", "agent.started", ...]
```

## Publisher/Subscriber Model

### Publishing Events

```python
from fool_platform.events import EventBus, EventEnvelope

bus = EventBus.create()
bus.initialize()
bus.start()

event = EventEnvelope.create_with_metadata(
    event_type="case.created",
    event_version="1.0.0",
    payload={"case_id": "123"},
)
result = bus.publish(event)

bus.dispose()
```

### Subscribing to Events

```python
from fool_platform.events import EventBus, FunctionalEventSubscriber, HandlerResult

bus = EventBus.create()

def handle_case_created(event):
    print(f"Case created: {event.payload}")
    return HandlerResult.success("handler", event.event_id, 0.0)

bus.subscribe(FunctionalEventSubscriber(
    subscriber_id="case-handler",
    handler=handle_case_created,
    supported_event_types=["case.created", "case.updated"],
))

# Supports wildcard patterns
bus.subscribe(FunctionalEventSubscriber(
    subscriber_id="all-case",
    handler=handle_case_created,
    supported_event_types=["case.*"],  # Matches all case events
))
```

## Routing

Events are routed to subscribers based on event type patterns:

- **Exact match**: `case.created` matches `case.created`
- **Wildcard prefix**: `case.*` matches `case.created`, `case.updated`, etc.
- **Universal**: `*` matches all events

```python
# Pattern examples
"case.created"        # Exact match only
"case.*"             # All case events
"agent.*"            # All agent events
"*"                  # All events
```

## Dispatcher

The dispatcher delivers events to matching subscribers:

- **Isolates subscriber errors** - A failing subscriber doesn't crash others
- **Deterministic ordering** - Subscribers receive events in priority order
- **Collects results** - Returns detailed dispatch results

```python
result = bus.publish(event)
print(f"Delivered to {result.dispatched_count} subscribers")
```

## Event History

In-memory event history with O(1) append:

```python
history = bus.get_history()

# Store events automatically (enabled by default)
bus.publish(event)

# Query history
all_events = history.list_events()
case_events = history.find_by_type("case.created")
related = history.find_by_correlation_id("corr-123")
idempotent = history.find_by_idempotency_key("idem-key")
```

## Event Replay

Replay events from history:

```python
# Replay all events
result = bus.replay_all()

# Replay by type
result = bus.replay_by_type("case.created")

# Replay by correlation
result = bus.replay_by_correlation_id("corr-123")
```

Replay characteristics:
- Preserves original event IDs
- Maintains event ordering
- Updates metrics

## Validation

Structural validation before publishing:

```python
bus = EventBus.create(validate_before_publish=True)

# Validation checks:
# - event_id exists
# - event_type exists
# - event_version exists
# - occurred_at exists
# - payload is dict
# - idempotency_key is string when provided
```

## Serialization

JSON serialization with round-trip support:

```python
from fool_platform.events import EventSerializer

serializer = EventSerializer()

# Serialize
json_str = serializer.serialize_event(envelope)

# Deserialize
restored = serializer.deserialize_event(json_str)
assert restored.event_id == envelope.event_id
```

## Metrics

In-memory metrics tracking:

```python
metrics = bus.get_metrics()

print(f"Published: {metrics['published_events']}")
print(f"Dispatched: {metrics['dispatched_events']}")
print(f"Failed: {metrics['failed_dispatches']}")
print(f"Subscribers: {metrics['registered_subscribers']}")
```

## Lifecycle

Event Bus lifecycle management:

```python
bus = EventBus.create()
bus.initialize()    # Prepare for operation
bus.start()         # Enable publishing/dispatching
bus.stop()          # Stop new dispatches, preserve history
bus.reset()         # Clear in-memory state
bus.dispose()       # Permanent shutdown
```

## Thread Safety

The Event Bus is thread-safe:

- Subscriber registration/unregistration
- Publishing
- History append/read
- Metrics updates

## Exceptions

Dedicated exception hierarchy:

```python
from fool_platform.events import (
    EventBusError,
    EventValidationError,
    EventDispatchError,
    EventSerializationError,
    EventReplayError,
    EventRegistryError,
    EventSubscriberError,
    EventRoutingError,
)
```

## What Phase 2B Includes

✅ In-memory Event Bus foundation  
✅ Event envelope and metadata model  
✅ Event context model  
✅ Publisher abstraction  
✅ Subscriber abstraction  
✅ Dispatcher with error isolation  
✅ Router with wildcard support  
✅ Event registry (contracts-aware)  
✅ Event validation  
✅ JSON serialization  
✅ Event history (in-memory)  
✅ Event replay (in-memory)  
✅ Event lifecycle  
✅ In-memory metrics  
✅ Thread safety  
✅ 30+ tests  
✅ Architecture enforcement  

## What Phase 2B Does NOT Include

❌ Kafka, RabbitMQ, NATS, Redis, Celery  
❌ Database persistence  
❌ External message broker  
❌ Event sourcing database  
❌ Network transport  
❌ Workflow execution engine  
❌ Real agents  
❌ APIs  
❌ AI/LLM integrations  
❌ Connectors  

## Next Phase: Phase 2C Orchestration Foundation

The Event Bus will be used by Phase 2C Orchestration to:

- Publish workflow state change events
- Subscribe to agent events
- Coordinate multi-step workflows
- Implement saga patterns
- Enable event-driven saga choreography
