"""
fool_platform/orchestration/models.py

Data models for the Orchestration layer.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class WorkflowExecutionStatus(str, Enum):
    """Status of a workflow execution."""
    CREATED = "created"
    INITIALIZED = "initialized"
    PLANNED = "planned"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TERMINATED = "terminated"


class StepStatus(str, Enum):
    """Status of a workflow step execution."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class WorkflowStepExecution:
    """Execution state for a single workflow step."""
    step_id: str
    agent_id: str | None
    capability_id: str | None
    status: StepStatus
    depends_on: frozenset[str] = field(default_factory=frozenset)
    attempts: int = 0
    max_attempts: int = 1
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_status(self, new_status: StepStatus) -> "WorkflowStepExecution":
        """Return a new instance with updated status."""
        return WorkflowStepExecution(
            step_id=self.step_id,
            agent_id=self.agent_id,
            capability_id=self.capability_id,
            status=new_status,
            depends_on=self.depends_on,
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            started_at=self.started_at,
            completed_at=self.completed_at,
            error=self.error,
            metadata=self.metadata,
        )

    def with_started(self, timestamp: str) -> "WorkflowStepExecution":
        """Return a new instance with started_at set and RUNNING status."""
        return WorkflowStepExecution(
            step_id=self.step_id,
            agent_id=self.agent_id,
            capability_id=self.capability_id,
            status=StepStatus.RUNNING,
            depends_on=self.depends_on,
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            started_at=timestamp,
            completed_at=self.completed_at,
            error=self.error,
            metadata=self.metadata,
        )

    def with_completed(self, timestamp: str) -> "WorkflowStepExecution":
        """Return a new instance with completed_at set."""
        return WorkflowStepExecution(
            step_id=self.step_id,
            agent_id=self.agent_id,
            capability_id=self.capability_id,
            status=self.status,
            depends_on=self.depends_on,
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            started_at=self.started_at,
            completed_at=timestamp,
            error=self.error,
            metadata=self.metadata,
        )

    def with_error(self, error: str) -> "WorkflowStepExecution":
        """Return a new instance with error set."""
        return WorkflowStepExecution(
            step_id=self.step_id,
            agent_id=self.agent_id,
            capability_id=self.capability_id,
            status=self.status,
            depends_on=self.depends_on,
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            started_at=self.started_at,
            completed_at=self.completed_at,
            error=error,
            metadata=self.metadata,
        )

    def increment_attempts(self) -> "WorkflowStepExecution":
        """Return a new instance with incremented attempts."""
        return WorkflowStepExecution(
            step_id=self.step_id,
            agent_id=self.agent_id,
            capability_id=self.capability_id,
            status=self.status,
            depends_on=self.depends_on,
            attempts=self.attempts + 1,
            max_attempts=self.max_attempts,
            started_at=self.started_at,
            completed_at=self.completed_at,
            error=self.error,
            metadata=self.metadata,
        )


@dataclass
class WorkflowExecution:
    """State of a workflow execution."""
    execution_id: str
    workflow_id: str
    workflow_version: str
    status: WorkflowExecutionStatus
    created_at: str
    updated_at: str
    started_at: str | None = None
    completed_at: str | None = None
    current_steps: dict[str, WorkflowStepExecution] = field(default_factory=dict)
    completed_steps: list[str] = field(default_factory=list)
    failed_steps: list[str] = field(default_factory=list)
    blocked_steps: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: WorkflowStepExecution) -> None:
        """Add a step to current steps."""
        self.current_steps[step.step_id] = step

    def update_step(self, step: WorkflowStepExecution) -> None:
        """Update a step in current steps."""
        self.current_steps[step.step_id] = step

    def mark_step_completed(self, step_id: str) -> None:
        """Move step from current to completed."""
        if step_id in self.current_steps:
            self.completed_steps.append(step_id)
            del self.current_steps[step_id]

    def mark_step_failed(self, step_id: str) -> None:
        """Move step from current to failed."""
        if step_id in self.current_steps:
            self.failed_steps.append(step_id)
            del self.current_steps[step_id]

    def mark_step_blocked(self, step_id: str) -> None:
        """Move step from current to blocked."""
        if step_id in self.current_steps:
            self.blocked_steps.append(step_id)
            del self.current_steps[step_id]

    @classmethod
    def create(
        cls,
        workflow_id: str,
        workflow_version: str,
    ) -> "WorkflowExecution":
        """Create a new workflow execution."""
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            execution_id=str(uuid4()),
            workflow_id=workflow_id,
            workflow_version=workflow_version,
            status=WorkflowExecutionStatus.CREATED,
            created_at=now,
            updated_at=now,
        )


@dataclass
class ExecutionSummary:
    """Summary of a workflow execution."""
    execution_id: str
    workflow_id: str
    status: WorkflowExecutionStatus
    runnable_steps: list[str]
    completed_steps: list[str]
    failed_steps: list[str]
    blocked_steps: list[str]
    events_emitted: int
    errors: list[str]
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class OrchestrationDecision:
    """Record of an orchestration decision."""
    decision_id: str
    execution_id: str
    decision_type: str
    rationale: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
