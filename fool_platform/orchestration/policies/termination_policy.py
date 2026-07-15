"""
fool_platform/orchestration/policies/termination_policy.py

Termination policy evaluation.
"""
from dataclasses import dataclass

from fool_platform.orchestration.models import WorkflowExecution
from fool_platform.orchestration.registry.policy_registry import TerminationCondition


@dataclass
class TerminationDecision:
    """Result of termination policy evaluation."""
    is_terminated: bool
    reason: str | None
    condition_matched: str | None


class TerminationPolicyEvaluator:
    """
    Evaluates termination policies for workflows.
    
    Checks if workflow should terminate based on declarative conditions.
    """

    def is_terminated(
        self,
        execution: WorkflowExecution,
        conditions: list[TerminationCondition],
    ) -> bool:
        """
        Check if workflow should terminate.
        
        Args:
            execution: The workflow execution
            conditions: List of termination conditions
            
        Returns:
            True if workflow should terminate
        """
        for condition in conditions:
            if self._evaluate_condition(execution, condition):
                return True
        return False

    def explain_termination(
        self,
        execution: WorkflowExecution,
        conditions: list[TerminationCondition],
    ) -> TerminationDecision:
        """
        Explain why workflow should or should not terminate.
        
        Args:
            execution: The workflow execution
            conditions: List of termination conditions
            
        Returns:
            TerminationDecision with explanation
        """
        for condition in conditions:
            if self._evaluate_condition(execution, condition):
                return TerminationDecision(
                    is_terminated=True,
                    reason=self._explain_condition(condition),
                    condition_matched=condition.condition_type,
                )
        
        return TerminationDecision(
            is_terminated=False,
            reason="No termination condition matched",
            condition_matched=None,
        )

    def _evaluate_condition(
        self,
        execution: WorkflowExecution,
        condition: TerminationCondition,
    ) -> bool:
        """
        Evaluate a single termination condition.
        
        Args:
            execution: The workflow execution
            condition: The termination condition
            
        Returns:
            True if condition is met
        """
        condition_type = condition.condition_type
        
        if condition_type == "always":
            return True
        
        if condition_type == "step_completed":
            step_id = condition.step_id
            if step_id:
                return step_id in execution.completed_steps
            return len(execution.completed_steps) > 0
        
        if condition_type == "step_failed":
            step_id = condition.step_id
            if step_id:
                return step_id in execution.failed_steps
            return len(execution.failed_steps) > 0
        
        if condition_type == "all_steps_completed":
            return (
                len(execution.current_steps) == 0
                and len(execution.completed_steps) > 0
            )
        
        if condition_type == "any_step_failed":
            return len(execution.failed_steps) > 0
        
        return False

    def _explain_condition(self, condition: TerminationCondition) -> str:
        """Generate explanation for a condition."""
        if condition.condition_type == "always":
            return "Always terminate"
        if condition.condition_type == "step_completed":
            if condition.step_id:
                return f"Step {condition.step_id} completed"
            return "Some step completed"
        if condition.condition_type == "step_failed":
            if condition.step_id:
                return f"Step {condition.step_id} failed"
            return "Some step failed"
        if condition.condition_type == "all_steps_completed":
            return "All steps completed"
        if condition.condition_type == "any_step_failed":
            return "Any step failed"
        return f"Condition {condition.condition_type}"
