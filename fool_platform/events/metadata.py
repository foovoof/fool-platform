"""
fool_platform/events/metadata.py

Event metadata model for the Event Bus layer.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class EventMetadata:
    """
    Immutable metadata for all events in the platform.
    
    Contains tracing, correlation, causation, and idempotency information.
    All fields are optional except event_id, event_type, event_version, and occurred_at.
    """
    event_id: str
    event_type: str
    event_version: str
    occurred_at: str
    correlation_id: str | None = None
    causation_id: str | None = None
    trace_id: str | None = None
    producer: str | None = None
    source: str | None = None
    subject: str | None = None
    case_id: str | None = None
    workflow_id: str | None = None
    agent_id: str | None = None
    idempotency_key: str | None = None
    tags: frozenset[str] = field(default_factory=frozenset)
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: str,
        event_version: str,
        producer: str | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        trace_id: str | None = None,
        source: str | None = None,
        subject: str | None = None,
        case_id: str | None = None,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        idempotency_key: str | None = None,
        tags: list[str] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> "EventMetadata":
        """
        Create a new EventMetadata instance with auto-generated event_id and occurred_at.
        
        Args:
            event_type: The type of the event (required)
            event_version: The version of the event schema (required)
            producer: The producer that created this event
            correlation_id: ID for correlating related events
            causation_id: ID of the event that caused this event
            trace_id: ID for distributed tracing
            source: Source system or component
            subject: Subject of the event
            case_id: Associated case ID (optional)
            workflow_id: Associated workflow ID (optional)
            agent_id: Associated agent ID (optional)
            idempotency_key: Key for idempotent event processing (optional)
            tags: List of tags for categorization
            attributes: Additional custom attributes
            
        Returns:
            A new EventMetadata instance
        """
        return cls(
            event_id=str(uuid4()),
            event_type=event_type,
            event_version=event_version,
            occurred_at=datetime.now(timezone.utc).isoformat(),
            producer=producer,
            correlation_id=correlation_id,
            causation_id=causation_id,
            trace_id=trace_id,
            source=source,
            subject=subject,
            case_id=case_id,
            workflow_id=workflow_id,
            agent_id=agent_id,
            idempotency_key=idempotency_key,
            tags=frozenset(tags) if tags else frozenset(),
            attributes=attributes if attributes else {},
        )

    def with_correlation_id(self, correlation_id: str) -> "EventMetadata":
        """Return a new EventMetadata with the specified correlation_id."""
        return EventMetadata(
            event_id=self.event_id,
            event_type=self.event_type,
            event_version=self.event_version,
            occurred_at=self.occurred_at,
            correlation_id=correlation_id,
            causation_id=self.causation_id,
            trace_id=self.trace_id,
            producer=self.producer,
            source=self.source,
            subject=self.subject,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            idempotency_key=self.idempotency_key,
            tags=self.tags,
            attributes=self.attributes,
        )

    def with_causation_id(self, causation_id: str) -> "EventMetadata":
        """Return a new EventMetadata with the specified causation_id."""
        return EventMetadata(
            event_id=self.event_id,
            event_type=self.event_type,
            event_version=self.event_version,
            occurred_at=self.occurred_at,
            correlation_id=self.correlation_id,
            causation_id=causation_id,
            trace_id=self.trace_id,
            producer=self.producer,
            source=self.source,
            subject=self.subject,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            idempotency_key=self.idempotency_key,
            tags=self.tags,
            attributes=self.attributes,
        )

    def with_trace_id(self, trace_id: str) -> "EventMetadata":
        """Return a new EventMetadata with the specified trace_id."""
        return EventMetadata(
            event_id=self.event_id,
            event_type=self.event_type,
            event_version=self.event_version,
            occurred_at=self.occurred_at,
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            trace_id=trace_id,
            producer=self.producer,
            source=self.source,
            subject=self.subject,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            idempotency_key=self.idempotency_key,
            tags=self.tags,
            attributes=self.attributes,
        )
