"""
fool_platform/events/tests/test_event_bus.py

Comprehensive tests for the Event Bus foundation.
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pytest

from fool_platform.events import (
    EventBus,
    EventBusLifecycle,
    EventBusState,
    EventContext,
    EventDispatcher,
    EventEnvelope,
    EventHistory,
    EventMetrics,
    EventMetadata,
    EventPublisher,
    EventRegistry,
    EventRouter,
    EventSerializer,
    EventSubscriber,
    EventValidator,
    FunctionalEventSubscriber,
    HandlerResult,
    HandlerStatus,
    InMemoryEventHistory,
    InMemoryEventReplay,
    InvalidStateTransitionError,
    PublishResult,
    ValidationResult,
    ValidationStatus,
)
from fool_platform.events.dispatcher import DispatchResult
from fool_platform.events.envelope import EventEnvelope
from fool_platform.events.history import EventHistory
from fool_platform.events.replay import ReplayResult


class TestEventMetadata:
    """Tests for EventMetadata creation and manipulation."""

    def test_create_metadata(self):
        """Test EventMetadata creation."""
        metadata = EventMetadata.create(
            event_type="case.created",
            event_version="1.0.0",
            producer="test-producer",
            correlation_id="corr-123",
        )
        
        assert metadata.event_type == "case.created"
        assert metadata.event_version == "1.0.0"
        assert metadata.producer == "test-producer"
        assert metadata.correlation_id == "corr-123"
        assert metadata.event_id is not None
        assert metadata.occurred_at is not None

    def test_metadata_is_immutable(self):
        """Test that EventMetadata is immutable."""
        metadata = EventMetadata.create(
            event_type="test",
            event_version="1.0.0",
        )
        with pytest.raises(AttributeError):
            metadata.event_type = "other"

    def test_metadata_with_correlation_id(self):
        """Test adding correlation ID to metadata."""
        metadata = EventMetadata.create(
            event_type="test",
            event_version="1.0.0",
        )
        new_metadata = metadata.with_correlation_id("new-corr-id")
        
        assert new_metadata.correlation_id == "new-corr-id"
        assert new_metadata.event_type == metadata.event_type


class TestEventEnvelope:
    """Tests for EventEnvelope creation and manipulation."""

    def test_create_envelope(self):
        """Test EventEnvelope creation."""
        metadata = EventMetadata.create(
            event_type="test.event",
            event_version="1.0.0",
        )
        envelope = EventEnvelope.create(
            metadata=metadata,
            payload={"key": "value"},
        )
        
        assert envelope.metadata == metadata
        assert envelope.payload == {"key": "value"}
        assert envelope.validation_status == ValidationStatus.PENDING

    def test_create_envelope_with_factory(self):
        """Test EventEnvelope creation with factory method."""
        envelope = EventEnvelope.create_with_metadata(
            event_type="test.event",
            event_version="1.0.0",
            payload={"data": 123},
            producer="factory-test",
        )
        
        assert envelope.event_type == "test.event"
        assert envelope.payload == {"data": 123}
        assert envelope.metadata.producer == "factory-test"

    def test_envelope_requires_dict_payload(self):
        """Test that envelope requires dict payload."""
        metadata = EventMetadata.create(
            event_type="test",
            event_version="1.0.0",
        )
        with pytest.raises(TypeError):
            EventEnvelope.create(metadata=metadata, payload="not-a-dict")


class TestEventContext:
    """Tests for EventContext creation and manipulation."""

    def test_create_context(self):
        """Test EventContext creation."""
        context = EventContext.create(
            correlation_id="corr-123",
            case_id="case-456",
        )
        
        assert context.correlation_id == "corr-123"
        assert context.case_id == "case-456"

    def test_context_merge(self):
        """Test merging two contexts."""
        context1 = EventContext.create(correlation_id="corr-1", actor_id="actor-1")
        context2 = EventContext.create(correlation_id="corr-2", case_id="case-1")
        
        merged = context1.merge(context2)
        
        assert merged.correlation_id == "corr-1"
        assert merged.actor_id == "actor-1"
        assert merged.case_id == "case-1"


class TestEventLifecycle:
    """Tests for Event Bus lifecycle."""

    def test_initial_state(self):
        """Test initial lifecycle state."""
        lifecycle = EventBusLifecycle()
        assert lifecycle.state == EventBusState.UNINITIALIZED
        assert not lifecycle.is_initialized

    def test_initialize(self):
        """Test initialization."""
        lifecycle = EventBusLifecycle()
        lifecycle.initialize()
        
        assert lifecycle.state == EventBusState.INITIALIZED
        assert lifecycle.is_initialized

    def test_start(self):
        """Test starting."""
        lifecycle = EventBusLifecycle()
        lifecycle.initialize()
        lifecycle.start()
        
        assert lifecycle.state == EventBusState.RUNNING
        assert lifecycle.is_running

    def test_stop(self):
        """Test stopping."""
        lifecycle = EventBusLifecycle()
        lifecycle.initialize()
        lifecycle.start()
        lifecycle.stop()
        
        assert lifecycle.state == EventBusState.STOPPED
        assert lifecycle.is_stopped

    def test_invalid_transition(self):
        """Test invalid state transition."""
        lifecycle = EventBusLifecycle()
        
        with pytest.raises(InvalidStateTransitionError):
            lifecycle.start()

    def test_dispose(self):
        """Test disposal."""
        lifecycle = EventBusLifecycle()
        lifecycle.initialize()
        lifecycle.dispose()
        
        assert lifecycle.state == EventBusState.DISPOSED
        assert lifecycle.is_disposed


class TestEventSerializer:
    """Tests for JSON serialization."""

    def test_serialize_deserialize_roundtrip(self):
        """Test serialization round-trip."""
        envelope = EventEnvelope.create_with_metadata(
            event_type="test.event",
            event_version="1.0.0",
            payload={"data": "value", "number": 42},
            correlation_id="corr-123",
            idempotency_key="idem-123",
        )
        
        serializer = EventSerializer()
        json_str = serializer.serialize_event(envelope)
        restored = serializer.deserialize_event(json_str)
        
        assert restored.event_id == envelope.event_id
        assert restored.event_type == envelope.event_type
        assert restored.payload == envelope.payload
        assert restored.metadata.correlation_id == envelope.metadata.correlation_id
        assert restored.metadata.idempotency_key == envelope.metadata.idempotency_key

    def test_deserialize_invalid_json(self):
        """Test deserialization of invalid JSON."""
        from fool_platform.events.exceptions import EventSerializationError
        
        serializer = EventSerializer()
        with pytest.raises(EventSerializationError):
            serializer.deserialize_event("not valid json {")


class TestEventValidation:
    """Tests for event validation."""

    def test_validation_success(self):
        """Test successful validation."""
        validator = EventValidator()
        envelope = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={"key": "value"},
        )
        
        result = validator.validate_envelope(envelope)
        assert result.valid

    def test_validation_missing_event_id(self):
        """Test validation failure for missing event_id."""
        validator = EventValidator()
        metadata = EventMetadata(
            event_id="",
            event_type="test",
            event_version="1.0.0",
            occurred_at=datetime.now(timezone.utc).isoformat(),
        )
        envelope = EventEnvelope.create(metadata=metadata, payload={})
        
        result = validator.validate_envelope(envelope)
        assert not result.valid
        assert any("event_id" in str(e) for e in result.errors)

    def test_validation_missing_event_type(self):
        """Test validation failure for missing event_type."""
        validator = EventValidator()
        metadata = EventMetadata(
            event_id="test-id",
            event_type="",
            event_version="1.0.0",
            occurred_at=datetime.now(timezone.utc).isoformat(),
        )
        envelope = EventEnvelope.create(metadata=metadata, payload={})
        
        result = validator.validate_envelope(envelope)
        assert not result.valid

    def test_validation_invalid_idempotency_key_type(self):
        """Test validation of idempotency key type."""
        validator = EventValidator()
        metadata = EventMetadata.create(
            event_type="test",
            event_version="1.0.0",
            idempotency_key=123,  # Should be string
        )
        envelope = EventEnvelope.create(metadata=metadata, payload={})
        
        result = validator.validate_metadata(metadata)
        assert not result.valid


class TestEventRouter:
    """Tests for event routing."""

    def test_exact_match(self):
        """Test exact event type matching."""
        router = EventRouter()
        subscriber = FunctionalEventSubscriber(
            subscriber_id="sub-1",
            handler=lambda e: HandlerResult.success("sub-1", e.event_id, 0.0),
            supported_event_types=["case.created"],
        )
        router.register(subscriber, "case.created")
        
        matches = router.route("case.created")
        assert len(matches) == 1
        assert matches[0].subscriber_id == "sub-1"

    def test_wildcard_match(self):
        """Test wildcard pattern matching."""
        router = EventRouter()
        subscriber = FunctionalEventSubscriber(
            subscriber_id="sub-all",
            handler=lambda e: HandlerResult.success("sub-all", e.event_id, 0.0),
            supported_event_types=["case.*"],
        )
        router.register(subscriber, "case.*")
        
        matches = router.route("case.created")
        assert len(matches) == 1
        
        matches = router.route("case.updated")
        assert len(matches) == 1

    def test_no_match(self):
        """Test no matching subscribers."""
        router = EventRouter()
        matches = router.route("unknown.event")
        assert len(matches) == 0

    def test_priority_ordering(self):
        """Test subscriber priority ordering."""
        router = EventRouter()
        
        sub1 = FunctionalEventSubscriber(
            subscriber_id="sub-1",
            handler=lambda e: HandlerResult.success("sub-1", e.event_id, 0.0),
            supported_event_types=["test"],
        )
        sub2 = FunctionalEventSubscriber(
            subscriber_id="sub-2",
            handler=lambda e: HandlerResult.success("sub-2", e.event_id, 0.0),
            supported_event_types=["test"],
        )
        
        router.register(sub1, "test", priority=10)
        router.register(sub2, "test", priority=20)
        
        matches = router.route("test")
        assert matches[0].subscriber_id == "sub-2"


class TestEventDispatcher:
    """Tests for event dispatching."""

    def test_dispatch_to_one_subscriber(self):
        """Test dispatch to a single subscriber."""
        dispatcher = EventDispatcher()
        received = []
        
        def handler(event):
            received.append(event)
            return HandlerResult.success("sub-1", event.event_id, 0.0)
        
        subscriber = FunctionalEventSubscriber(
            subscriber_id="sub-1",
            handler=handler,
            supported_event_types=["test.event"],
        )
        dispatcher.register_subscriber(subscriber)
        
        envelope = EventEnvelope.create_with_metadata(
            event_type="test.event",
            event_version="1.0.0",
            payload={},
        )
        result = dispatcher.dispatch(envelope)
        
        assert result.success
        assert result.delivered_count == 1
        assert len(received) == 1

    def test_dispatch_to_multiple_subscribers(self):
        """Test dispatch to multiple subscribers."""
        dispatcher = EventDispatcher()
        received = []
        
        for i in range(3):
            def make_handler(n):
                def handler(event):
                    received.append(n)
                    return HandlerResult.success(f"sub-{n}", event.event_id, 0.0)
                return handler
            
            subscriber = FunctionalEventSubscriber(
                subscriber_id=f"sub-{i}",
                handler=make_handler(i),
                supported_event_types=["test.event"],
            )
            dispatcher.register_subscriber(subscriber)
        
        envelope = EventEnvelope.create_with_metadata(
            event_type="test.event",
            event_version="1.0.0",
            payload={},
        )
        result = dispatcher.dispatch(envelope)
        
        assert result.success
        assert result.delivered_count == 3
        assert len(received) == 3

    def test_subscriber_error_isolation(self):
        """Test that subscriber errors don't crash dispatcher."""
        dispatcher = EventDispatcher()
        
        def failing_handler(event):
            raise ValueError("Handler failed")
        
        def success_handler(event):
            return HandlerResult.success("sub-success", event.event_id, 0.0)
        
        dispatcher.register_subscriber(FunctionalEventSubscriber(
            subscriber_id="sub-fail",
            handler=failing_handler,
            supported_event_types=["test"],
        ))
        dispatcher.register_subscriber(FunctionalEventSubscriber(
            subscriber_id="sub-success",
            handler=success_handler,
            supported_event_types=["test"],
        ))
        
        envelope = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
        )
        result = dispatcher.dispatch(envelope)
        
        assert result.partial_failure
        assert result.delivered_count == 1
        assert result.failed_count == 1


class TestEventHistory:
    """Tests for event history."""

    def test_append_preserves_order(self):
        """Test that append preserves insertion order."""
        history = InMemoryEventHistory()
        
        events = [
            EventEnvelope.create_with_metadata(
                event_type="test",
                event_version="1.0.0",
                payload={"n": i},
            )
            for i in range(5)
        ]
        
        for event in events:
            history.append(event)
        
        stored = history.list_events()
        assert len(stored) == 5
        for i, event in enumerate(stored):
            assert event.payload["n"] == i

    def test_find_by_type(self):
        """Test finding events by type."""
        history = InMemoryEventHistory()
        
        history.append(EventEnvelope.create_with_metadata(
            event_type="case.created",
            event_version="1.0.0",
            payload={},
        ))
        history.append(EventEnvelope.create_with_metadata(
            event_type="case.updated",
            event_version="1.0.0",
            payload={},
        ))
        history.append(EventEnvelope.create_with_metadata(
            event_type="agent.started",
            event_version="1.0.0",
            payload={},
        ))
        
        case_events = history.find_by_type("case.created")
        assert len(case_events) == 1
        assert case_events[0].event_type == "case.created"

    def test_find_by_correlation_id(self):
        """Test finding events by correlation ID."""
        history = InMemoryEventHistory()
        
        event1 = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
            correlation_id="corr-123",
        )
        event2 = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
            correlation_id="corr-123",
        )
        
        history.append(event1)
        history.append(event2)
        
        found = history.find_by_correlation_id("corr-123")
        assert len(found) == 2

    def test_find_by_idempotency_key(self):
        """Test finding events by idempotency key."""
        history = InMemoryEventHistory()
        
        event = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
            idempotency_key="idem-unique",
        )
        history.append(event)
        
        found = history.find_by_idempotency_key("idem-unique")
        assert len(found) == 1
        assert found[0].event_id == event.event_id

    def test_duplicate_event_detection(self):
        """Test duplicate detection using event_id."""
        history = InMemoryEventHistory()
        
        event = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
        )
        history.append(event)
        
        assert history.has_event(event.event_id)
        assert not history.has_event("non-existent-id")

    def test_clear_history(self):
        """Test clearing history."""
        history = InMemoryEventHistory()
        
        history.append(EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
        ))
        
        assert history.count() == 1
        history.clear()
        assert history.count() == 0


class TestEventReplay:
    """Tests for event replay."""

    def test_replay_all(self):
        """Test replaying all events."""
        history = InMemoryEventHistory()
        dispatcher = EventDispatcher()
        replayed = []
        
        def capture_handler(event):
            replayed.append(event)
            return HandlerResult.success("sub", event.event_id, 0.0)
        
        subscriber = FunctionalEventSubscriber(
            subscriber_id="sub",
            handler=capture_handler,
            supported_event_types=["*"],
        )
        dispatcher.register_subscriber(subscriber)
        
        for i in range(3):
            event = EventEnvelope.create_with_metadata(
                event_type="test",
                event_version="1.0.0",
                payload={"n": i},
            )
            history.append(event)
        
        replay = InMemoryEventReplay(history, dispatcher)
        result = replay.replay_all()
        
        assert result.replayed_count == 3
        assert result.failed_count == 0
        assert len(replayed) == 3

    def test_replay_preserves_order(self):
        """Test that replay preserves event ordering."""
        history = InMemoryEventHistory()
        dispatcher = EventDispatcher()
        replayed_order = []
        
        def capture_handler(event):
            replayed_order.append(event.payload["n"])
            return HandlerResult.success("sub", event.event_id, 0.0)
        
        subscriber = FunctionalEventSubscriber(
            subscriber_id="sub",
            handler=capture_handler,
            supported_event_types=["*"],
        )
        dispatcher.register_subscriber(subscriber)
        
        for i in [2, 0, 1]:
            event = EventEnvelope.create_with_metadata(
                event_type="test",
                event_version="1.0.0",
                payload={"n": i},
            )
            history.append(event)
        
        replay = InMemoryEventReplay(history, dispatcher)
        replay.replay_all()
        
        assert replayed_order == [2, 0, 1]


class TestEventBus:
    """Tests for integrated Event Bus."""

    def test_integrated_publish_subscribe(self):
        """Test integrated publish/subscribe flow."""
        bus = EventBus.create()
        received = []
        
        def handler(event):
            received.append(event)
            return HandlerResult.success("sub", event.event_id, 0.0)
        
        bus.subscribe(FunctionalEventSubscriber(
            subscriber_id="sub",
            handler=handler,
            supported_event_types=["test.*"],
        ))
        
        bus.initialize()
        bus.start()
        
        event = EventEnvelope.create_with_metadata(
            event_type="test.event",
            event_version="1.0.0",
            payload={"data": "value"},
        )
        result = bus.publish(event)
        
        assert result.success
        assert len(received) == 1
        assert received[0].payload["data"] == "value"
        
        bus.stop()
        bus.dispose()

    def test_metrics_increment(self):
        """Test that metrics are incremented correctly."""
        bus = EventBus.create()
        
        bus.subscribe(FunctionalEventSubscriber(
            subscriber_id="sub",
            handler=lambda e: HandlerResult.success("sub", e.event_id, 0.0),
            supported_event_types=["test"],
        ))
        
        bus.initialize()
        bus.start()
        
        event = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
        )
        bus.publish(event)
        
        metrics = bus.get_metrics()
        assert metrics["published_events"] == 1
        assert metrics["dispatched_events"] >= 1
        
        bus.stop()
        bus.dispose()

    def test_reject_publishing_after_disposal(self):
        """Test that publishing is rejected after disposal."""
        bus = EventBus.create()
        bus.initialize()
        bus.start()
        bus.stop()
        bus.dispose()
        
        event = EventEnvelope.create_with_metadata(
            event_type="test",
            event_version="1.0.0",
            payload={},
        )
        
        with pytest.raises(InvalidStateTransitionError):
            bus.publish(event)


class TestConcurrentSafety:
    """Tests for thread safety."""

    def test_concurrent_publish(self):
        """Test concurrent publishing."""
        bus = EventBus.create()
        received_count = [0]
        lock = threading.Lock()
        
        def handler(event):
            with lock:
                received_count[0] += 1
            return HandlerResult.success("sub", event.event_id, 0.0)
        
        bus.subscribe(FunctionalEventSubscriber(
            subscriber_id="sub",
            handler=handler,
            supported_event_types=["*"],
        ))
        
        bus.initialize()
        bus.start()
        
        def publish_events():
            for _ in range(10):
                event = EventEnvelope.create_with_metadata(
                    event_type="test",
                    event_version="1.0.0",
                    payload={},
                )
                bus.publish(event)
        
        threads = [threading.Thread(target=publish_events) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert received_count[0] == 50
        
        bus.stop()
        bus.dispose()

    def test_concurrent_subscribe(self):
        """Test concurrent subscriber registration."""
        bus = EventBus.create()
        bus.initialize()
        bus.start()
        
        def register_subscribers():
            for i in range(10):
                bus.subscribe(FunctionalEventSubscriber(
                    subscriber_id=f"sub-{threading.current_thread().name}-{i}",
                    handler=lambda e: HandlerResult.success("sub", e.event_id, 0.0),
                    supported_event_types=["test"],
                ))
        
        threads = [threading.Thread(target=register_subscribers, name=f"t{i}") for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        metrics = bus.get_metrics()
        assert metrics["registered_subscribers"] == 50
        
        bus.stop()
        bus.dispose()


class TestEventRegistry:
    """Tests for event registry."""

    def test_register_and_lookup(self):
        """Test registering and looking up event definitions."""
        registry = EventRegistry(auto_load=False)
        
        registry.register_standard_event(
            event_type="case.created",
            event_version="1.0.0",
            description="A case was created",
        )
        
        assert registry.has_event_type("case.created")
        assert not registry.has_event_type("nonexistent")
        
        definition = registry.get_event_definition("case.created", "1.0.0")
        assert definition is not None
        assert definition.event_type == "case.created"
        assert definition.description == "A case was created"

    def test_list_event_types(self):
        """Test listing all event types."""
        registry = EventRegistry(auto_load=False)
        
        registry.register_standard_event("event.a", "1.0.0")
        registry.register_standard_event("event.b", "1.0.0")
        registry.register_standard_event("event.c", "1.0.0")
        
        types = registry.list_event_types()
        assert len(types) == 3
        assert "event.a" in types

    def test_latest_version(self):
        """Test getting latest version."""
        registry = EventRegistry(auto_load=False)
        
        registry.register_standard_event("test", "1.0.0")
        registry.register_standard_event("test", "2.0.0")
        registry.register_standard_event("test", "1.5.0")
        
        latest = registry.get_latest_version("test")
        assert latest == "2.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
