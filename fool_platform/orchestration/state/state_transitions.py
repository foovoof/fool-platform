"""
fool_platform/orchestration/state/state_transitions.py

State transition validation and application.
"""
from fool_platform.orchestration.models import (
    StepStatus,
    WorkflowExecution,
    WorkflowExecutionStatus,
    WorkflowStepExecution,
)
from fool_platform.orchestration.orchestration_exceptions import (
    WorkflowTransitionError,
)


class StateTransitions:
    """
    Validates and applies state transitions for workflows and steps.
    """

    VALID_WORKFLOW_TRANSITIONS: dict[WorkflowExecutionStatus, set[WorkflowExecutionStatus]] = {
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

    VALID_STEP_TRANSITIONS: dict[StepStatus, set[StepStatus]] = {
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

    def validate_workflow_transition(
        self,
        current_status: WorkflowExecutionStatus,
        next_status: WorkflowExecutionStatus,
    ) -> bool:
        """
        Validate a workflow status transition.
        
        Args:
            current_status: Current workflow status
            next_status: Desired next status
            
        Returns:
            True if transition is valid
            
        Raises:
            WorkflowTransitionError: If transition is invalid
        """
        valid_next = self.VALID_WORKFLOW_TRANSITIONS.get(current_status, set())
        
        if next_status not in valid_next:
            raise WorkflowTransitionError(
                execution_id="unknown",
                current_status=current_status.value,
                target_status=next_status.value,
            )
        
        return True

    def validate_step_transition(
        self,
        current_status: StepStatus,
        next_status: StepStatus,
    ) -> bool:
        """
        Validate a step status transition.
        
        Args:
            current_status: Current step status
            next_status: Desired next status
            
        Returns:
            True if transition is valid
            
        Raises:
            WorkflowTransitionError: If transition is invalid
        """
        valid_next = self.VALID_STEP_TRANSITIONS.get(current_status, set())
        
        if next_status not in valid_next:
            raise WorkflowTransitionError(
                execution_id="unknown",
                current_status=current_status.value,
                target_status=next_status.value,
            )
        
        return True

    def apply_workflow_transition(
        self,
        execution: WorkflowExecution,
        next_status: WorkflowExecutionStatus,
    ) -> WorkflowExecution:
        """
        Apply a workflow status transition.
        
        Args:
            execution: The workflow execution
            next_status: The desired next status
            
        Returns:
            The updated WorkflowExecution
            
        Raises:
            WorkflowTransitionError: If transition is invalid
        """
        self.validate_workflow_transition(execution.status, next_status)
        
        execution.status = next_status
        
        from datetime import datetime, timezone
        execution.updated_at = datetime.now(timezone.utc).isoformat()
        
        if next_status == WorkflowExecutionStatus.RUNNING:
            execution.started_at = datetime.now(timezone.utc).isoformat()
        elif next_status in (
            WorkflowExecutionStatus.COMPLETED,
            WorkflowExecutionStatus.FAILED,
            WorkflowExecutionStatus.CANCELLED,
            WorkflowExecutionStatus.TERMINATED,
        ):
            execution.completed_at = datetime.now(timezone.utc).isoformat()
        
        return execution

    def apply_step_transition(
        self,
        step_execution: WorkflowStepExecution,
        next_status: StepStatus,
    ) -> WorkflowStepExecution:
        """
        Apply a step status transition.
        
        Args:
            step_execution: The step execution
            next_status: The desired next status
            
        Returns:
            The updated WorkflowStepExecution
            
        Raises:
            WorkflowTransitionError: If transition is invalid
        """
        self.validate_step_transition(step_execution.status, next_status)
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        
        if next_status == StepStatus.RUNNING:
            step_execution = step_execution.with_started(now)
        elif next_status == StepStatus.COMPLETED:
            step_execution = step_execution.with_completed(now)
        elif next_status == StepStatus.FAILED:
            step_execution = step_execution.with_completed(now)
        else:
            step_execution = step_execution.with_status(next_status)
        
        return step_execution
