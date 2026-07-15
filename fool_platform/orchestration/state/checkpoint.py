"""
fool_platform/orchestration/state/checkpoint.py

Checkpoint management for workflow execution state.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4

from fool_platform.orchestration.models import WorkflowExecution
from fool_platform.orchestration.orchestration_exceptions import CheckpointError


@dataclass
class Checkpoint:
    """Snapshot of workflow execution state."""
    checkpoint_id: str
    execution_id: str
    workflow_id: str
    status_snapshot: str
    step_snapshot: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_execution(cls, execution: WorkflowExecution) -> "Checkpoint":
        """Create a checkpoint from a workflow execution."""
        step_snapshots = []
        for step in execution.current_steps.values():
            step_snapshots.append({
                "step_id": step.step_id,
                "agent_id": step.agent_id,
                "capability_id": step.capability_id,
                "status": step.status.value,
                "depends_on": list(step.depends_on),
                "attempts": step.attempts,
                "max_attempts": step.max_attempts,
                "started_at": step.started_at,
                "completed_at": step.completed_at,
                "error": step.error,
                "metadata": step.metadata,
            })

        return cls(
            checkpoint_id=str(uuid4()),
            execution_id=execution.execution_id,
            workflow_id=execution.workflow_id,
            status_snapshot=execution.status.value,
            step_snapshot=step_snapshots,
        )


class CheckpointStore:
    """
    In-memory checkpoint store.
    
    Stores snapshots of workflow execution state for recovery.
    """

    def __init__(self) -> None:
        self._checkpoints: dict[str, list[Checkpoint]] = {}
        self._checkpoint_index: dict[str, Checkpoint] = {}
        self._lock = Lock()

    def create_checkpoint(self, execution: WorkflowExecution) -> Checkpoint:
        """
        Create a checkpoint for a workflow execution.
        
        Args:
            execution: The workflow execution to checkpoint
            
        Returns:
            The created Checkpoint
        """
        checkpoint = Checkpoint.from_execution(execution)
        
        with self._lock:
            if execution.execution_id not in self._checkpoints:
                self._checkpoints[execution.execution_id] = []
            self._checkpoints[execution.execution_id].append(checkpoint)
            self._checkpoint_index[checkpoint.checkpoint_id] = checkpoint
        
        return checkpoint

    def get_checkpoint(self, checkpoint_id: str) -> Checkpoint | None:
        """
        Get a checkpoint by ID.
        
        Args:
            checkpoint_id: The checkpoint ID
            
        Returns:
            Checkpoint or None if not found
        """
        with self._lock:
            return self._checkpoint_index.get(checkpoint_id)

    def list_checkpoints(self, execution_id: str) -> list[Checkpoint]:
        """
        List all checkpoints for an execution.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            List of checkpoints in creation order
        """
        with self._lock:
            return self._checkpoints.get(execution_id, []).copy()

    def restore_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        """
        Restore a checkpoint (returns it for restoration).
        
        Args:
            checkpoint_id: The checkpoint ID to restore
            
        Returns:
            The Checkpoint to restore
            
        Raises:
            CheckpointError: If checkpoint not found
        """
        checkpoint = self.get_checkpoint(checkpoint_id)
        if not checkpoint:
            raise CheckpointError(
                message=f"Checkpoint not found: {checkpoint_id}",
                checkpoint_id=checkpoint_id,
            )
        return checkpoint

    def clear_for_execution(self, execution_id: str) -> int:
        """
        Clear all checkpoints for an execution.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            Number of checkpoints cleared
        """
        with self._lock:
            checkpoints = self._checkpoints.pop(execution_id, [])
            for cp in checkpoints:
                self._checkpoint_index.pop(cp.checkpoint_id, None)
            return len(checkpoints)

    def clear(self) -> None:
        """Clear all checkpoints."""
        with self._lock:
            self._checkpoints.clear()
            self._checkpoint_index.clear()
