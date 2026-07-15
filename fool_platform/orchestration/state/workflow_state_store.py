"""
fool_platform/orchestration/state/workflow_state_store.py

In-memory workflow state store.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4

from fool_platform.orchestration.execution_context import ExecutionContext
from fool_platform.orchestration.models import (
    StepStatus,
    WorkflowExecution,
    WorkflowExecutionStatus,
    WorkflowStepExecution,
)
from fool_platform.orchestration.orchestration_exceptions import (
    WorkflowStateError,
    WorkflowTransitionError,
)


class WorkflowStateStore:
    """
    In-memory store for workflow execution state.
    
    Thread-safe for concurrent access.
    """

    def __init__(self) -> None:
        self._executions: dict[str, WorkflowExecution] = {}
        self._lock = Lock()

    def create_execution(
        self,
        workflow_id: str,
        workflow_version: str,
        context: ExecutionContext,
    ) -> WorkflowExecution:
        """
        Create a new workflow execution.
        
        Args:
            workflow_id: The workflow ID
            workflow_version: The workflow version
            context: The execution context
            
        Returns:
            The created WorkflowExecution
        """
        execution = WorkflowExecution.create(workflow_id, workflow_version)
        
        with self._lock:
            self._executions[execution.execution_id] = execution
        
        return execution

    def get_execution(self, execution_id: str) -> WorkflowExecution | None:
        """
        Get a workflow execution by ID.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            WorkflowExecution or None if not found
        """
        with self._lock:
            return self._executions.get(execution_id)

    def update_status(
        self,
        execution_id: str,
        status: WorkflowExecutionStatus,
    ) -> WorkflowExecution:
        """
        Update workflow execution status.
        
        Args:
            execution_id: The execution ID
            status: The new status
            
        Returns:
            The updated WorkflowExecution
            
        Raises:
            WorkflowTransitionError: If transition is invalid
        """
        with self._lock:
            execution = self._executions.get(execution_id)
            if not execution:
                raise WorkflowStateError(
                    execution_id=execution_id,
                    message="Execution not found",
                )

            valid_transitions = self._get_valid_workflow_transitions(execution.status)
            if status not in valid_transitions:
                raise WorkflowTransitionError(
                    execution_id=execution_id,
                    current_status=execution.status.value,
                    target_status=status.value,
                )

            execution.status = status
            execution.updated_at = datetime.now(timezone.utc).isoformat()
            
            if status == WorkflowExecutionStatus.RUNNING:
                execution.started_at = datetime.now(timezone.utc).isoformat()
            elif status in (WorkflowExecutionStatus.COMPLETED, WorkflowExecutionStatus.FAILED, WorkflowExecutionStatus.CANCELLED, WorkflowExecutionStatus.TERMINATED):
                execution.completed_at = datetime.now(timezone.utc).isoformat()

            return execution

    def update_step_status(
        self,
        execution_id: str,
        step_id: str,
        status: StepStatus,
    ) -> WorkflowStepExecution | None:
        """
        Update step execution status.
        
        Args:
            execution_id: The execution ID
            step_id: The step ID
            status: The new status
            
        Returns:
            The updated WorkflowStepExecution or None
        """
        with self._lock:
            execution = self._executions.get(execution_id)
            if not execution:
                raise WorkflowStateError(
                    execution_id=execution_id,
                    message="Execution not found",
                )

            step = execution.current_steps.get(step_id)
            if not step:
                return None

            valid_transitions = self._get_valid_step_transitions(step.status)
            if status not in valid_transitions:
                raise WorkflowTransitionError(
                    execution_id=execution_id,
                    current_status=step.status.value,
                    target_status=status.value,
                )

            now = datetime.now(timezone.utc).isoformat()
            
            if status == StepStatus.RUNNING:
                step = step.with_started(now)
            elif status == StepStatus.COMPLETED:
                step = step.with_completed(now)
                execution.mark_step_completed(step_id)
            elif status == StepStatus.FAILED:
                step = step.with_completed(now)
                execution.mark_step_failed(step_id)
            elif status == StepStatus.BLOCKED:
                execution.mark_step_blocked(step_id)
            elif status == StepStatus.SKIPPED:
                execution.mark_step_completed(step_id)
            else:
                step = step.with_status(status)

            if status not in (StepStatus.COMPLETED, StepStatus.FAILED, StepStatus.BLOCKED, StepStatus.SKIPPED):
                execution.update_step(step)

            execution.updated_at = now
            
            return step

    def add_step(
        self,
        execution_id: str,
        step: WorkflowStepExecution,
    ) -> None:
        """
        Add a step to workflow execution.
        
        Args:
            execution_id: The execution ID
            step: The step to add
        """
        with self._lock:
            execution = self._executions.get(execution_id)
            if not execution:
                raise WorkflowStateError(
                    execution_id=execution_id,
                    message="Execution not found",
                )
            execution.add_step(step)

    def list_executions(self) -> list[WorkflowExecution]:
        """
        List all workflow executions.
        
        Returns:
            List of all executions
        """
        with self._lock:
            return list(self._executions.values())

    def clear(self) -> None:
        """Clear all executions."""
        with self._lock:
            self._executions.clear()

    def _get_valid_workflow_transitions(
        self,
        current: WorkflowExecutionStatus,
    ) -> set[WorkflowExecutionStatus]:
        """Get valid workflow status transitions."""
        transitions = {
            WorkflowExecutionStatus.CREATED: {WorkflowExecutionStatus.INITIALIZED},
            WorkflowExecutionStatus.INITIALIZED: {WorkflowExecutionStatus.PLANNED},
            WorkflowExecutionStatus.PLANNED: {WorkflowExecutionStatus.RUNNING},
            WorkflowExecutionStatus.RUNNING: {
                WorkflowExecutionStatus.WAITING,
                WorkflowExecutionStatus.COMPLETED,
                WorkflowExecutionStatus.FAILED,
                WorkflowExecutionStatus.CANCELLED,
                WorkflowExecutionStatus.TERMINATED,
            },
            WorkflowExecutionStatus.WAITING: {
                WorkflowExecutionStatus.RUNNING,
                WorkflowExecutionStatus.COMPLETED,
                WorkflowExecutionStatus.FAILED,
                WorkflowExecutionStatus.CANCELLED,
                WorkflowExecutionStatus.TERMINATED,
            },
            WorkflowExecutionStatus.COMPLETED: set(),
            WorkflowExecutionStatus.FAILED: set(),
            WorkflowExecutionStatus.CANCELLED: set(),
            WorkflowExecutionStatus.TERMINATED: set(),
        }
        return transitions.get(current, set())

    def _get_valid_step_transitions(
        self,
        current: StepStatus,
    ) -> set[StepStatus]:
        """Get valid step status transitions."""
        transitions = {
            StepStatus.PENDING: {StepStatus.READY, StepStatus.BLOCKED},
            StepStatus.READY: {StepStatus.RUNNING, StepStatus.SKIPPED},
            StepStatus.RUNNING: {
                StepStatus.COMPLETED,
                StepStatus.FAILED,
                StepStatus.SKIPPED,
            },
            StepStatus.COMPLETED: set(),
            StepStatus.FAILED: set(),
            StepStatus.SKIPPED: set(),
            StepStatus.BLOCKED: {StepStatus.READY, StepStatus.PENDING},
        }
        return transitions.get(current, set())
