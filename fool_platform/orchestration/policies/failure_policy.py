"""
fool_platform/orchestration/policies/failure_policy.py

Failure policy evaluation.
"""
from dataclasses import dataclass
from enum import Enum

from fool_platform.orchestration.models import WorkflowExecution, WorkflowStepExecution
from fool_platform.orchestration.registry.policy_registry import FailurePolicy


class FailureAction(str, Enum):
    """Possible actions on step failure."""
    FAIL = "fail"
    CONTINUE = "continue"
    BLOCK = "block"
    ESCALATE = "escalate"


@dataclass
class FailureDecision:
    """Result of failure policy evaluation."""
    action: FailureAction
    escalate_to: str | None
    reason: str


class FailurePolicyEvaluator:
    """
    Evaluates failure policies for workflows.
    
    Determines whether a failed step should cause workflow failure,
    allow continuation, or trigger escalation.
    """

    def evaluate_failure(
        self,
        execution: WorkflowExecution,
        failed_step: WorkflowStepExecution,
        policy: FailurePolicy,
    ) -> FailureDecision:
        """
        Evaluate failure policy for a failed step.
        
        Args:
            execution: The workflow execution
            failed_step: The failed step execution
            policy: The failure policy
            
        Returns:
            FailureDecision with the action to take
        """
        on_failure = policy.on_failure.lower()
        
        if on_failure == "escalate_to_human" or on_failure == "escalate":
            return FailureDecision(
                action=FailureAction.ESCALATE,
                escalate_to=policy.escalation_target,
                reason=f"Step {failed_step.step_id} failed: {failed_step.error}",
            )
        
        if on_failure == "continue":
            return FailureDecision(
                action=FailureAction.CONTINUE,
                escalate_to=None,
                reason=f"Step {failed_step.step_id} failed but policy allows continue: {failed_step.error}",
            )
        
        if on_failure == "block":
            return FailureDecision(
                action=FailureAction.BLOCK,
                escalate_to=None,
                reason=f"Step {failed_step.step_id} failed and blocked: {failed_step.error}",
            )
        
        return FailureDecision(
            action=FailureAction.FAIL,
            escalate_to=None,
            reason=f"Step {failed_step.step_id} failed with policy 'fail': {failed_step.error}",
        )

    def should_continue_workflow(
        self,
        decision: FailureDecision,
    ) -> bool:
        """
        Determine if workflow should continue after a failure.
        
        Args:
            decision: The failure decision
            
        Returns:
            True if workflow should continue
        """
        return decision.action in (FailureAction.CONTINUE, FailureAction.BLOCK)

    def should_fail_workflow(
        self,
        decision: FailureDecision,
    ) -> bool:
        """
        Determine if workflow should fail.
        
        Args:
            decision: The failure decision
            
        Returns:
            True if workflow should fail
        """
        return decision.action == FailureAction.FAIL
