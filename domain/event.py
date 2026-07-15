"""
domain/event.py

Event domain model - immutable state change records.
Mirrors contracts/domain/event.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum

from .common import (
    EMPTY_METADATA,
    Metadata,
    Reference,
    new_id,
    utc_now,
)


class EventType(str, Enum):
    """Types of platform events."""
    IDENTITY_CREATED = "identity.created"
    IDENTITY_UPDATED = "identity.updated"
    ENTITY_CREATED = "entity.created"
    ENTITY_UPDATED = "entity.updated"
    EVIDENCE_COLLECTED = "evidence.collected"
    EVIDENCE_ANNOTATED = "evidence.annotated"
    FINDING_CREATED = "finding.created"
    FINDING_UPDATED = "finding.updated"
    RELATIONSHIP_CREATED = "relationship.created"
    CASE_OPENED = "case.opened"
    CASE_UPDATED = "case.updated"
    CASE_CLOSED = "case.closed"
    REPORT_DRAFTED = "report.drafted"
    REPORT_REVIEWED = "report.reviewed"
    REPORT_PUBLISHED = "report.published"
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"
    AGENT_TASK_STARTED = "agent.task.started"
    AGENT_TASK_COMPLETED = "agent.task.completed"
    AGENT_TASK_FAILED = "agent.task.failed"


@dataclass(frozen=True)
class Event:
    """
    Event is an immutable record of a state change.
    
    Per the Event-Driven Language principle, state changes are described
    as dotted, namespaced, versioned Events rather than ad hoc strings.
    """
    id: str
    version: str
    event_type: str
    occurred_at: str
    recorded_at: str
    correlation_id: str | None = None
    causation_id: str | None = None
    subject_ref: Reference | None = None
    actor: str | None = None
    payload: dict = field(default_factory=dict)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        event_type: str,
        occurred_at: str | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        subject_ref: Reference | None = None,
        actor: str | None = None,
        payload: dict | None = None,
        metadata: Metadata | None = None,
    ) -> "Event":
        """Create a new Event."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            version="1.0.0",
            event_type=event_type,
            occurred_at=occurred_at or timestamp,
            recorded_at=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            subject_ref=subject_ref,
            actor=actor,
            payload=payload or {},
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )

    def with_causation(self, causation_id: str) -> "Event":
        """Return a new Event with causation context."""
        return Event(
            id=self.id,
            version=self.version,
            event_type=self.event_type,
            occurred_at=self.occurred_at,
            recorded_at=self.recorded_at,
            correlation_id=self.correlation_id,
            causation_id=causation_id,
            subject_ref=self.subject_ref,
            actor=self.actor,
            payload=self.payload,
            metadata=self.metadata,
        )

    def with_correlation(self, correlation_id: str) -> "Event":
        """Return a new Event with correlation context."""
        return Event(
            id=self.id,
            version=self.version,
            event_type=self.event_type,
            occurred_at=self.occurred_at,
            recorded_at=self.recorded_at,
            correlation_id=correlation_id,
            causation_id=self.causation_id,
            subject_ref=self.subject_ref,
            actor=self.actor,
            payload=self.payload,
            metadata=self.metadata,
        )


__all__ = [
    "Event",
    "EventType",
]
