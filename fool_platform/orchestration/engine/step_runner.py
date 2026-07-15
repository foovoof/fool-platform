"""
fool_platform/orchestration/engine/step_runner.py

Step runner skeleton for workflow orchestration.

IMPORTANT: This does NOT execute real agents.
It only changes state and returns structured results.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fool_platform.orchestration.execution_context import ExecutionContext
from fool_platform.orchestration.models import StepStatus, WorkflowStepExecution
from fool_platform.orchestration.registry.workflow_registry import StepDefinition


@dataclass
class StepPreparation:
    """Result of step preparation."""
    step_execution: WorkflowStepExecution
    execution_context: ExecutionContext
    agent_id: str | None
    capability_id: str | None


@dataclass
class StepResult:
    """Result of step state change."""
    step_execution: WorkflowStepExecution
    success: bool
    message: str
    output: dict[str, Any] | None = None


class StepRunner:
    """
    Skeleton step runner for workflow orchestration.
    
    IMPORTANT: Does NOT execute real agents.
    Only manages step state transitions and returns structured results.
    """

    def prepare_step(
        self,
        step: StepDefinition,
        execution_context: ExecutionContext,
        agent_id: str | None = None,
        capability_id: str | None = None,
        max_attempts: int = 1,
    ) -> StepPreparation:
        """
        Prepare a step for execution.
        
        Args:
            step: The step definition
            execution_context: The execution context
            agent_id: Optional agent ID override
            capability_id: Optional capability ID override
            max_attempts: Maximum retry attempts
            
        Returns:
            StepPreparation with step execution and context
        """
        step_execution = WorkflowStepExecution(
            step_id=step.step_id,
            agent_id=agent_id or step.agent_type,
            capability_id=capability_id or step.capability,
            status=StepStatus.PENDING,
            depends_on=frozenset(step.depends_on),
            attempts=0,
            max_attempts=max_attempts,
        )
        
        child_context = execution_context.create_child_context(step.step_id)
        
        return StepPreparation(
            step_execution=step_execution,
            execution_context=child_context,
            agent_id=agent_id or step.agent_type,
            capability_id=capability_id or step.capability,
        )

    def mark_step_ready(self, step_execution: WorkflowStepExecution) -> StepResult:
        """
        Mark a step as ready to run.
        
        Args:
            step_execution: The step execution state
            
        Returns:
            StepResult with updated state
        """
        step_execution = step_execution.with_status(StepStatus.READY)
        
        return StepResult(
            step_execution=step_execution,
            success=True,
            message=f"Step {step_execution.step_id} is ready",
        )

    def mark_step_running(self, step_execution: WorkflowStepExecution) -> StepResult:
        """
        Mark a step as running.
        
        Args:
            step_execution: The step execution state
            
        Returns:
            StepResult with updated state
        """
        now = datetime.now(timezone.utc).isoformat()
        step_execution = step_execution.with_started(now)
        step_execution = step_execution.with_status(StepStatus.RUNNING)
        
        return StepResult(
            step_execution=step_execution,
            success=True,
            message=f"Step {step_execution.step_id} is running",
        )

    def mark_step_completed(
        self,
        step_execution: WorkflowStepExecution,
        output: dict[str, Any] | None = None,
    ) -> StepResult:
        """
        Mark a step as completed.
        
        Args:
            step_execution: The step execution state
            output: Optional output from step
            
        Returns:
            StepResult with updated state
        """
        now = datetime.now(timezone.utc).isoformat()
        step_execution = step_execution.with_completed(now)
        step_execution = step_execution.with_status(StepStatus.COMPLETED)
        
        if output:
            step_execution.metadata["output"] = output
        
        return StepResult(
            step_execution=step_execution,
            success=True,
            message=f"Step {step_execution.step_id} completed successfully",
            output=output,
        )

    def mark_step_failed(
        self,
        step_execution: WorkflowStepExecution,
        error: str,
    ) -> StepResult:
        """
        Mark a step as failed.
        
        Args:
            step_execution: The step execution state
            error: The error message
            
        Returns:
            StepResult with updated state
        """
        now = datetime.now(timezone.utc).isoformat()
        step_execution = step_execution.with_completed(now)
        step_execution = step_execution.with_error(error)
        step_execution = step_execution.with_status(StepStatus.FAILED)
        step_execution = step_execution.increment_attempts()
        
        return StepResult(
            step_execution=step_execution,
            success=False,
            message=f"Step {step_execution.step_id} failed: {error}",
        )

    def mark_step_skipped(self, step_execution: WorkflowStepExecution) -> StepResult:
        """
        Mark a step as skipped.
        
        Args:
            step_execution: The step execution state
            
        Returns:
            StepResult with updated state
        """
        step_execution = step_execution.with_status(StepStatus.SKIPPED)
        
        return StepResult(
            step_execution=step_execution,
            success=True,
            message=f"Step {step_execution.step_id} was skipped",
        )

    def mark_step_blocked(self, step_execution: WorkflowStepExecution) -> StepResult:
        """
        Mark a step as blocked.
        
        Args:
            step_execution: The step execution state
            
        Returns:
            StepResult with updated state
        """
        step_execution = step_execution.with_status(StepStatus.BLOCKED)
        
        return StepResult(
            step_execution=step_execution,
            success=True,
            message=f"Step {step_execution.step_id} is blocked",
        )
