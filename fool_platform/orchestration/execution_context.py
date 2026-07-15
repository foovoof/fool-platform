"""
fool_platform/orchestration/execution_context.py

Execution context for workflow orchestration.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fool_platform.orchestration.orchestration_exceptions import ExecutionContextError


@dataclass
class ExecutionContext:
    """
    Context for workflow execution.
    
    Carries execution metadata and allows attachment of additional data.
    """
    execution_id: str
    workflow_id: str
    workflow_version: str
    case_id: str | None
    trace_id: str
    correlation_id: str
    initiated_by: str | None
    input_payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def create(
        cls,
        workflow_id: str,
        workflow_version: str,
        case_id: str | None = None,
        initiated_by: str | None = None,
        input_payload: dict[str, Any] | None = None,
        trace_id: str | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ExecutionContext":
        """
        Create a new execution context.
        
        Args:
            workflow_id: The workflow ID
            workflow_version: The workflow version
            case_id: Optional case ID
            initiated_by: Who initiated the execution
            input_payload: Input data for the workflow
            trace_id: Optional trace ID (generated if not provided)
            correlation_id: Optional correlation ID (generated if not provided)
            metadata: Optional initial metadata
            
        Returns:
            A new ExecutionContext instance
        """
        return cls(
            execution_id=str(uuid4()),
            workflow_id=workflow_id,
            workflow_version=workflow_version,
            case_id=case_id,
            trace_id=trace_id or str(uuid4()),
            correlation_id=correlation_id or str(uuid4()),
            initiated_by=initiated_by,
            input_payload=input_payload or {},
            metadata=metadata or {},
        )

    def create_child_context(self, step_id: str) -> "ExecutionContext":
        """
        Create a child context for a step.
        
        Args:
            step_id: The step ID
            
        Returns:
            A new ExecutionContext for the step
        """
        child_metadata = {
            **self.metadata,
            "parent_execution_id": self.execution_id,
            "step_id": step_id,
        }
        
        return ExecutionContext(
            execution_id=self.execution_id,
            workflow_id=self.workflow_id,
            workflow_version=self.workflow_version,
            case_id=self.case_id,
            trace_id=self.trace_id,
            correlation_id=self.correlation_id,
            initiated_by=self.initiated_by,
            input_payload=self.input_payload,
            metadata=child_metadata,
        )

    def attach_metadata(self, key: str, value: Any) -> None:
        """
        Attach metadata to the context.
        
        Args:
            key: Metadata key
            value: Metadata value
            
        Raises:
            ExecutionContextError: If context is frozen
        """
        if hasattr(self, "_frozen") and self._frozen:
            raise ExecutionContextError(
                f"Cannot attach metadata to frozen context",
                execution_id=self.execution_id,
            )
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

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "workflow_version": self.workflow_version,
            "case_id": self.case_id,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "initiated_by": self.initiated_by,
            "input_payload": self.input_payload,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
