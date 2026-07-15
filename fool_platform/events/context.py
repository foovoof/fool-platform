"""
fool_platform/events/context.py

Event context model for propagating execution context through events.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EventContext:
    """
    Immutable context for event propagation through the system.
    
    Used to carry execution context from producers to subscribers.
    """
    correlation_id: str | None = None
    causation_id: str | None = None
    trace_id: str | None = None
    actor_id: str | None = None
    case_id: str | None = None
    workflow_id: str | None = None
    agent_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        trace_id: str | None = None,
        actor_id: str | None = None,
        case_id: str | None = None,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "EventContext":
        """
        Create a new EventContext instance.
        
        Args:
            correlation_id: ID for correlating related events
            causation_id: ID of the event that caused the current operation
            trace_id: ID for distributed tracing
            actor_id: ID of the actor performing the operation
            case_id: Associated case ID
            workflow_id: Associated workflow ID
            agent_id: Associated agent ID
            metadata: Additional context metadata
            
        Returns:
            A new EventContext instance
        """
        return cls(
            correlation_id=correlation_id,
            causation_id=causation_id,
            trace_id=trace_id,
            actor_id=actor_id,
            case_id=case_id,
            workflow_id=workflow_id,
            agent_id=agent_id,
            metadata=metadata if metadata else {},
        )

    @classmethod
    def from_metadata(
        cls,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        trace_id: str | None = None,
        case_id: str | None = None,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "EventContext":
        """
        Create an EventContext from existing metadata fields.
        
        Convenience factory for creating context from extracted metadata.
        """
        return cls.create(
            correlation_id=correlation_id,
            causation_id=causation_id,
            trace_id=trace_id,
            case_id=case_id,
            workflow_id=workflow_id,
            agent_id=agent_id,
            metadata=metadata,
        )

    def with_actor_id(self, actor_id: str) -> "EventContext":
        """Return a new EventContext with the specified actor_id."""
        return EventContext(
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            trace_id=self.trace_id,
            actor_id=actor_id,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            metadata=self.metadata,
        )

    def with_correlation_id(self, correlation_id: str) -> "EventContext":
        """Return a new EventContext with the specified correlation_id."""
        return EventContext(
            correlation_id=correlation_id,
            causation_id=self.causation_id,
            trace_id=self.trace_id,
            actor_id=self.actor_id,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            metadata=self.metadata,
        )

    def with_trace_id(self, trace_id: str) -> "EventContext":
        """Return a new EventContext with the specified trace_id."""
        return EventContext(
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            trace_id=trace_id,
            actor_id=self.actor_id,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            metadata=self.metadata,
        )

    def merge(self, other: "EventContext") -> "EventContext":
        """
        Merge this context with another, preferring non-None values from self.
        
        Args:
            other: Another EventContext to merge with
            
        Returns:
            A new EventContext with merged values
        """
        return EventContext(
            correlation_id=self.correlation_id or other.correlation_id,
            causation_id=self.causation_id or other.causation_id,
            trace_id=self.trace_id or other.trace_id,
            actor_id=self.actor_id or other.actor_id,
            case_id=self.case_id or other.case_id,
            workflow_id=self.workflow_id or other.workflow_id,
            agent_id=self.agent_id or other.agent_id,
            metadata={**other.metadata, **self.metadata},
        )
