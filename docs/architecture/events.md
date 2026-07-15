# Event Bus Architecture

## Overview

The Event Bus is the internal communication backbone of FOOL Platform, implementing a contract-aware, version-aware, deterministic, in-memory event distribution system.

## Canonical Architecture

```
Standards
    ↓
Contracts
    ↓
Domain (Python)
    ↓
Knowledge
    ↓
Intelligence
    ↓
Platform ← Event Bus
    ↓
Applications
```

## Event-Driven Architecture

Events are first-class citizens in FOOL Platform:

1. **Events are Contracts**: Event types, versions, and schemas are defined in `contracts/events/`
2. **Events Flow Through Platform**: Event Bus is part of Platform infrastructure
3. **Events Enable Decoupling**: Publishers and subscribers are independent
4. **Events Enable Tracing**: Correlation, causation, and trace IDs

## Event Versioning

### Requirements

- `event_version` is mandatory
- Registry resolves event definitions by `event_type` and `event_version`
- Unknown versions must fail validation
- Version compatibility rules from Contracts

### Version Lookup

```python
# Get specific version
definition = registry.get_event_definition("case.created", "1.0.0")

# Get latest version
latest = registry.get_latest_version("case.created")
```

## Idempotency

Duplicate detection using:
- `event_id` - Always unique
- `idempotency_key` - Optional business key

```python
# Publish with idempotency key
event = EventEnvelope.create_with_metadata(
    event_type="case.created",
    event_version="1.0.0",
    payload={},
    idempotency_key="business-key-123",
)

# Check in history
if history.has_idempotency_key("business-key-123"):
    # Skip duplicate
```

## Event Ordering

### Requirements

- History preserves publication order
- Replay preserves original ordering
- Dispatch to subscribers is deterministic

### Implementation

```python
class InMemoryEventHistory:
    _events: OrderedDict[str, EventEnvelope]  # Preserves insertion order
    
    def list_events(self) -> list[EventEnvelope]:
        return list(self._events.values())  # Ordered
```

## Thread Safety

### Protected Operations

- Subscriber registry mutations
- Event history append/read
- Metrics updates

### Not Protected

- Dispatcher dispatch operations (subscriber handles should be thread-safe)
- Historical replay

### Implementation

```python
from threading import Lock

class EventDispatcher:
    _router: EventRouter
    _lock: Lock
    
    def register_subscriber(self, subscriber):
        with self._lock:
            self._router.register(subscriber)
```

## Performance

### Complexity

- **Publish**: O(1) + O(matching_subscribers) for dispatch
- **History append**: O(1)
- **Replayer**: O(n) for n events

### Design Decisions

- Avoid repeated full registry scans during dispatch
- Use indexed lookups for history queries
- No background worker threads

## Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         EventBus                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                      Publisher                          │ │
│  │  - validate_before_publish                              │ │
│  │  - store_in_history                                     │ │
│  │  - dispatch to dispatcher                              │ │
│  └────────────────────────────┬─────────────────────────────┘ │
│                               │                               │
│  ┌────────────────────────────▼─────────────────────────────┐ │
│  │                      Dispatcher                          │ │
│  │  - route to subscribers                                 │ │
│  │  - isolate errors                                       │ │
│  │  - collect results                                       │ │
│  └────────────────────────────┬─────────────────────────────┘ │
│                               │                               │
│  ┌────────────────────────────▼─────────────────────────────┐ │
│  │                       Router                             │ │
│  │  - exact match                                          │ │
│  │  - wildcard match (*, case.*)                           │ │
│  │  - priority ordering                                    │ │
│  └────────────────────────────┬─────────────────────────────┘ │
│                               │                               │
│  ┌──────────────┐  ┌──────────▼──────────┐  ┌────────────┐ │
│  │   Registry   │  │     Subscribers     │  │  History   │ │
│  │  (contracts) │  │  (HandlerResult)   │  │ (in-memory)│ │
│  └──────────────┘  └─────────────────────┘  └────────────┘ │
│                                                                 │
│  ┌──────────┐  ┌─────────┐  ┌─────────┐  ┌────────────────┐   │
│  │ Metrics  │  │Lifecycle│  │ Replay  │  │ Serialization │   │
│  └──────────┘  └─────────┘  └─────────┘  └────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Exception Hierarchy

```
EventBusError
├── EventValidationError
├── EventDispatchError
├── EventSerializationError
├── EventReplayError
├── EventRegistryError
├── EventSubscriberError
└── EventRoutingError
```

## Metrics

| Metric | Description |
|--------|-------------|
| `published_events` | Total events published |
| `dispatched_events` | Total dispatch operations |
| `failed_dispatches` | Failed dispatch count |
| `subscriber_errors` | Subscriber error count |
| `replay_operations` | Replay operation count |
| `validation_failures` | Validation failure count |
| `serialization_failures` | Serialization failure count |
| `registered_subscribers` | Current subscriber count |
| `routed_events` | Total routing operations |

## Lifecycle States

```
UNINITIALIZED → INITIALIZED → RUNNING → STOPPING → STOPPED
     ↑              ↓           ↓         ↓          ↓
     └──────────────┴───────────┴─────────┴──────────┘
                        DISPOSED
```

| Transition | Method | Valid From |
|------------|--------|------------|
| →INITIALIZED | initialize() | UNINITIALIZED, STOPPED |
| →RUNNING | start() | INITIALIZED |
| →STOPPING | stop() | RUNNING |
| →STOPPED | stop() | STOPPING |
| →UNINITIALIZED | reset() | STOPPED |
| →DISPOSED | dispose() | INITIALIZED, STOPPED |

## Architecture Rules

### Platform/Events May Depend On

- contracts
- standards
- domain interfaces (if absolutely necessary)
- Python standard library

### Platform/Events Must NOT Depend On

- orchestration
- intelligence
- applications
- web
- ai
- connectors
- infrastructure
- external brokers
- databases

### Domain Must NOT Import

- platform/events

## Intentional Limitations (Phase 2B)

1. **No External Brokers**: Pure in-memory implementation
2. **No Persistence**: History exists only during process lifetime
3. **No Network Transport**: No gRPC, HTTP, or message queue integration
4. **No Async**: Synchronous implementation only

## Future Phases

- **Phase 2C**: Orchestration Foundation (uses Event Bus for workflows)
- **Phase 3**: Persistence Layer (database event store)
- **Phase 4**: External Integrations (Kafka, RabbitMQ adapters)
- **Phase 5**: Distributed Tracing (OpenTelemetry integration)
