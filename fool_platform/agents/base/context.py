"""
fool_platform/agents/base/context.py

Agent Context for FOOL Platform.

Provides execution context for agent operations.
Must remain independent from orchestration.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class AgentContext:
    """
    Execution context for agent operations.
    
    Provides isolation and traceability for agent tasks.
    Does NOT depend on orchestration.
    """
    context_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    task_id: str | None = None
    case_id: str | None = None
    workflow_id: str | None = None
    execution_id: str | None = None
    step_id: str | None = None
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def create(
        cls,
        agent_id: str,
        task_id: str | None = None,
        case_id: str | None = None,
        workflow_id: str | None = None,
        execution_id: str | None = None,
        step_id: str | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "AgentContext":
        """
        Create a new agent context.
        
        Args:
            agent_id: The agent ID
            task_id: Optional task ID
            case_id: Optional case ID
            workflow_id: Optional workflow ID
            execution_id: Optional execution ID
            step_id: Optional step ID
            correlation_id: Optional correlation ID
            metadata: Optional metadata
            
        Returns:
            New AgentContext instance
        """
        return cls(
            agent_id=agent_id,
            task_id=task_id,
            case_id=case_id,
            workflow_id=workflow_id,
            execution_id=execution_id,
            step_id=step_id,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )

    def create_child_context(self, sub_context_id: str) -> "AgentContext":
        """
        Create a child context for nested operations.
        
        Args:
            sub_context_id: Identifier for the sub-context
            
        Returns:
            New child AgentContext
        """
        return AgentContext(
            agent_id=self.agent_id,
            task_id=self.task_id,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            execution_id=self.execution_id,
            step_id=self.step_id,
            trace_id=self.trace_id,
            correlation_id=self.correlation_id,
            metadata={
                **self.metadata,
                "parent_context_id": self.context_id,
                "sub_context_id": sub_context_id,
            },
        )

    def attach_metadata(self, key: str, value: Any) -> None:
        """
        Attach metadata to the context.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get metadata from the context.
        
        Args:
            key: Metadata key
            default: Default value if key not found
            
        Returns:
            Metadata value or default
        """
        return self.metadata.get(key, default)

    def with_task(self, task_id: str) -> "AgentContext":
        """
        Return a new context with the given task ID.
        
        Args:
            task_id: The task ID
            
        Returns:
            New AgentContext with task_id set
        """
        return AgentContext(
            context_id=str(uuid4()),
            agent_id=self.agent_id,
            task_id=task_id,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            execution_id=self.execution_id,
            step_id=self.step_id,
            trace_id=self.trace_id,
            correlation_id=self.correlation_id,
            metadata=self.metadata.copy(),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_event_context(self) -> dict[str, Any]:
        """
        Convert context to event-compatible format.
        
        Returns:
            Dictionary suitable for event metadata
        """
        return {
            "context_id": self.context_id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "case_id": self.case_id,
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "step_id": self.step_id,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
        }
