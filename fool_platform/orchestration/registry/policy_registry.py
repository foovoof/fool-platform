"""
fool_platform/orchestration/registry/policy_registry.py

Policy registry for extracting and exposing workflow policies.
"""
from dataclasses import dataclass, field
from typing import Any

from fool_platform.orchestration.orchestration_exceptions import PolicyEvaluationError
from fool_platform.orchestration.registry.workflow_registry import WorkflowDefinition


@dataclass
class RetryPolicy:
    """Retry policy configuration."""
    max_attempts: int = 1
    backoff_seconds: int = 0
    backoff_multiplier: float = 1.0
    max_backoff_seconds: int | None = None


@dataclass
class TimeoutPolicy:
    """Timeout policy configuration."""
    duration_seconds: int = 300
    action: str = "fail"  # fail, continue, block


@dataclass
class FailurePolicy:
    """Failure policy configuration."""
    on_failure: str = "fail"  # fail, continue, block, escalate_to_human
    escalation_target: str | None = None


@dataclass
class TerminationCondition:
    """Termination condition configuration."""
    condition_type: str
    step_id: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


class PolicyRegistry:
    """
    Registry for workflow policies.
    
    Extracts and exposes retry, timeout, failure, and termination policies
    from workflow definitions.
    """

    def __init__(
        self,
        workflow_registry: "WorkflowRegistry | None" = None,
    ) -> None:
        """
        Initialize the policy registry.
        
        Args:
            workflow_registry: Optional workflow registry to extract policies from
        """
        self._workflow_registry = workflow_registry

    def get_retry_policy(
        self,
        workflow_id: str,
        step_id: str | None = None,
    ) -> RetryPolicy:
        """
        Get retry policy for a workflow or step.
        
        Args:
            workflow_id: The workflow ID
            step_id: Optional step ID for step-specific policy
            
        Returns:
            RetryPolicy instance
            
        Raises:
            PolicyEvaluationError: If workflow not found
        """
        if not self._workflow_registry:
            return RetryPolicy()

        workflow = self._workflow_registry.get_workflow(workflow_id)
        if not workflow:
            raise PolicyEvaluationError(
                policy_type="retry",
                reason=f"Workflow not found: {workflow_id}",
            )

        if step_id:
            for step in workflow.steps:
                if step.step_id == step_id and step.retry_policy:
                    return RetryPolicy(
                        max_attempts=step.retry_policy.get("max_attempts", 1),
                        backoff_seconds=step.retry_policy.get("backoff_seconds", 0),
                        backoff_multiplier=step.retry_policy.get("backoff_multiplier", 1.0),
                        max_backoff_seconds=step.retry_policy.get("max_backoff_seconds"),
                    )

        return RetryPolicy()

    def get_timeout_policy(
        self,
        workflow_id: str,
        step_id: str | None = None,
    ) -> TimeoutPolicy:
        """
        Get timeout policy for a workflow or step.
        
        Args:
            workflow_id: The workflow ID
            step_id: Optional step ID for step-specific policy
            
        Returns:
            TimeoutPolicy instance
            
        Raises:
            PolicyEvaluationError: If workflow not found
        """
        if not self._workflow_registry:
            return TimeoutPolicy()

        workflow = self._workflow_registry.get_workflow(workflow_id)
        if not workflow:
            raise PolicyEvaluationError(
                policy_type="timeout",
                reason=f"Workflow not found: {workflow_id}",
            )

        if step_id:
            for step in workflow.steps:
                if step.step_id == step_id and step.timeout_policy:
                    return TimeoutPolicy(
                        duration_seconds=step.timeout_policy.get("duration_seconds", 300),
                        action=step.timeout_policy.get("action", "fail"),
                    )

        return TimeoutPolicy()

    def get_failure_policy(self, workflow_id: str) -> FailurePolicy:
        """
        Get failure policy for a workflow.
        
        Args:
            workflow_id: The workflow ID
            
        Returns:
            FailurePolicy instance
            
        Raises:
            PolicyEvaluationError: If workflow not found
        """
        if not self._workflow_registry:
            return FailurePolicy()

        workflow = self._workflow_registry.get_workflow(workflow_id)
        if not workflow:
            raise PolicyEvaluationError(
                policy_type="failure",
                reason=f"Workflow not found: {workflow_id}",
            )

        if workflow.failure_policy:
            return FailurePolicy(
                on_failure=workflow.failure_policy.get("on_failure", "fail"),
                escalation_target=workflow.failure_policy.get("escalation_target"),
            )

        return FailurePolicy()

    def get_termination_conditions(self, workflow_id: str) -> list[TerminationCondition]:
        """
        Get termination conditions for a workflow.
        
        Args:
            workflow_id: The workflow ID
            
        Returns:
            List of TerminationCondition instances
            
        Raises:
            PolicyEvaluationError: If workflow not found
        """
        if not self._workflow_registry:
            return []

        workflow = self._workflow_registry.get_workflow(workflow_id)
        if not workflow:
            raise PolicyEvaluationError(
                policy_type="termination",
                reason=f"Workflow not found: {workflow_id}",
            )

        conditions = []
        for cond in workflow.termination_conditions:
            conditions.append(TerminationCondition(
                condition_type=cond.get("condition_type", "always"),
                step_id=cond.get("step_id"),
                params=cond.get("params", {}),
            ))

        return conditions
