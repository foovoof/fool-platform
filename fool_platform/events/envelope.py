"""
fool_platform/events/envelope.py

Event envelope model for wrapping events with metadata and validation status.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ValidationStatus(str, Enum):
    """Validation status of an event envelope."""
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class EventEnvelope:
    """
    Immutable envelope wrapping an event with metadata and validation status.
    
    This is the core event representation used throughout the Event Bus.
    The payload remains generic to support any event type.
    """
    metadata: "EventMetadata"
    payload: dict[str, Any]
    schema_ref: str | None = None
    validation_status: ValidationStatus = ValidationStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def create(
        cls,
        metadata: "EventMetadata",
        payload: dict[str, Any],
        schema_ref: str | None = None,
        validation_status: ValidationStatus = ValidationStatus.PENDING,
    ) -> "EventEnvelope":
        """
        Create a new EventEnvelope.
        
        Args:
            metadata: The event metadata
            payload: The event payload (must be a dict)
            schema_ref: Optional reference to the event schema
            validation_status: The validation status (default: PENDING)
            
        Returns:
            A new EventEnvelope instance
        """
        if not isinstance(payload, dict):
            raise TypeError("Event payload must be a dictionary")
        return cls(
            metadata=metadata,
            payload=payload,
            schema_ref=schema_ref,
            validation_status=validation_status,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def create_with_metadata(
        cls,
        event_type: str,
        event_version: str,
        payload: dict[str, Any],
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
        schema_ref: str | None = None,
        validation_status: ValidationStatus = ValidationStatus.PENDING,
    ) -> "EventEnvelope":
        """
        Create a new EventEnvelope with auto-generated metadata.
        
        Convenience factory that creates both metadata and envelope.
        
        Args:
            event_type: The type of the event
            event_version: The version of the event schema
            payload: The event payload
            producer: The producer that created this event
            correlation_id: ID for correlating related events
            causation_id: ID of the event that caused this event
            trace_id: ID for distributed tracing
            source: Source system or component
            subject: Subject of the event
            case_id: Associated case ID
            workflow_id: Associated workflow ID
            agent_id: Associated agent ID
            idempotency_key: Key for idempotent event processing
            tags: List of tags for categorization
            attributes: Additional custom attributes
            schema_ref: Optional reference to the event schema
            validation_status: The validation status
            
        Returns:
            A new EventEnvelope instance
        """
        from fool_platform.events.metadata import EventMetadata
        
        metadata = EventMetadata.create(
            event_type=event_type,
            event_version=event_version,
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
            tags=tags,
            attributes=attributes,
        )
        return cls.create(
            metadata=metadata,
            payload=payload,
            schema_ref=schema_ref,
            validation_status=validation_status,
        )

    def with_validation_status(self, status: ValidationStatus) -> "EventEnvelope":
        """Return a new EventEnvelope with the specified validation status."""
        return EventEnvelope(
            metadata=self.metadata,
            payload=self.payload,
            schema_ref=self.schema_ref,
            validation_status=status,
            created_at=self.created_at,
        )

    @property
    def event_id(self) -> str:
        """Get the event ID from metadata."""
        return self.metadata.event_id

    @property
    def event_type(self) -> str:
        """Get the event type from metadata."""
        return self.metadata.event_type

    @property
    def event_version(self) -> str:
        """Get the event version from metadata."""
        return self.metadata.event_version

    @property
    def occurred_at(self) -> str:
        """Get the occurred_at timestamp from metadata."""
        return self.metadata.occurred_at
