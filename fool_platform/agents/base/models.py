"""
fool_platform/agents/base/models.py

Agent Runtime data models for FOOL Platform.

This module provides the core data structures for agent tasks, results,
capabilities, and execution records.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class AgentStatus(Enum):
    """Agent lifecycle status."""
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


class AgentTaskStatus(Enum):
    """Agent task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentResultStatus(Enum):
    """Agent result status."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class AgentTask:
    """
    Represents a task to be executed by an agent.
    
    This is the input to agent execution.
    """
    task_id: str = field(default_factory=lambda: str(uuid4()))
    task_type: str = ""
    objective: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
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

    def with_trace_id(self, trace_id: str) -> "AgentTask":
        """Return a new instance with the given trace_id."""
        return AgentTask(
            task_id=self.task_id,
            task_type=self.task_type,
            objective=self.objective,
            inputs=self.inputs,
            case_id=self.case_id,
            workflow_id=self.workflow_id,
            execution_id=self.execution_id,
            step_id=self.step_id,
            trace_id=trace_id,
            correlation_id=self.correlation_id,
            metadata=self.metadata,
            created_at=self.created_at,
        )


@dataclass
class AgentResult:
    """
    Represents the result of an agent execution.
    
    This is the output from agent execution.
    """
    result_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    agent_id: str = ""
    status: AgentResultStatus = AgentResultStatus.SUCCESS
    outputs: dict[str, Any] = field(default_factory=dict)
    confidence: float | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    completed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    duration_ms: int = 0

    @property
    def is_success(self) -> bool:
        """Check if the result is successful."""
        return self.status == AgentResultStatus.SUCCESS

    @property
    def is_failure(self) -> bool:
        """Check if the result is a failure."""
        return self.status == AgentResultStatus.FAILURE


@dataclass
class AgentCapability:
    """
    Represents a capability that an agent can perform.
    
    This defines what an agent can do.
    """
    capability_id: str = ""
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def matches_capability_id(self, capability_id: str) -> bool:
        """Check if this capability matches the given ID."""
        return self.capability_id == capability_id


@dataclass
class AgentExecutionRecord:
    """
    Record of an agent execution for auditing and tracking.
    
    This is immutable once created.
    """
    execution_record_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    agent_id: str = ""
    status: AgentTaskStatus = AgentTaskStatus.PENDING
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    result_id: str | None = None
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def mark_completed(self, result_id: str) -> "AgentExecutionRecord":
        """Return a new instance marked as completed."""
        return AgentExecutionRecord(
            execution_record_id=self.execution_record_id,
            task_id=self.task_id,
            agent_id=self.agent_id,
            status=AgentTaskStatus.COMPLETED,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            result_id=result_id,
            errors=self.errors,
            metadata=self.metadata,
        )

    def mark_failed(self, errors: list[str]) -> "AgentExecutionRecord":
        """Return a new instance marked as failed."""
        return AgentExecutionRecord(
            execution_record_id=self.execution_record_id,
            task_id=self.task_id,
            agent_id=self.agent_id,
            status=AgentTaskStatus.FAILED,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            result_id=self.result_id,
            errors=errors,
            metadata=self.metadata,
        )
