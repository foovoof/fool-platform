"""
fool_platform/orchestration/policies/retry_policy.py

Retry policy evaluation.
"""
from fool_platform.orchestration.models import WorkflowStepExecution
from fool_platform.orchestration.registry.policy_registry import RetryPolicy


class RetryPolicyEvaluator:
    """
    Evaluates retry policies for workflow steps.
    
    Pure Python - no sleeping, no real timers.
    """

    def should_retry(
        self,
        step_execution: WorkflowStepExecution,
        policy: RetryPolicy,
    ) -> bool:
        """
        Determine if a step should be retried.
        
        Args:
            step_execution: The step execution state
            policy: The retry policy
            
        Returns:
            True if step should be retried
        """
        if step_execution.status != "failed":
            return False
        
        if step_execution.attempts >= policy.max_attempts:
            return False
        
        return True

    def next_attempt(
        self,
        step_execution: WorkflowStepExecution,
        policy: RetryPolicy,
    ) -> int:
        """
        Calculate the next attempt number.
        
        Args:
            step_execution: The step execution state
            policy: The retry policy
            
        Returns:
            The next attempt number
        """
        return step_execution.attempts + 1

    def max_attempts(self, policy: RetryPolicy) -> int:
        """
        Get the maximum number of attempts.
        
        Args:
            policy: The retry policy
            
        Returns:
            Maximum attempts
        """
        return policy.max_attempts

    def calculate_backoff(
        self,
        step_execution: WorkflowStepExecution,
        policy: RetryPolicy,
    ) -> float:
        """
        Calculate backoff delay in seconds.
        
        Args:
            step_execution: The step execution state
            policy: The retry policy
            
        Returns:
            Backoff delay in seconds
        """
        if policy.backoff_seconds <= 0:
            return 0.0
        
        backoff = policy.backoff_seconds * (policy.backoff_multiplier ** step_execution.attempts)
        
        if policy.max_backoff_seconds:
            backoff = min(backoff, policy.max_backoff_seconds)
        
        return backoff
