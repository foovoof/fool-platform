"""
fool_platform/orchestration/policies/timeout_policy.py

Timeout policy evaluation.
"""
from datetime import datetime, timezone

from fool_platform.orchestration.registry.policy_registry import TimeoutPolicy


class TimeoutPolicyEvaluator:
    """
    Evaluates timeout policies for workflow steps.
    
    Pure Python - no real timers, only evaluates timestamps.
    """

    def is_timed_out(
        self,
        started_at: str | None,
        policy: TimeoutPolicy,
        now: datetime | None = None,
    ) -> bool:
        """
        Check if a step has timed out.
        
        Args:
            started_at: ISO timestamp when step started
            policy: The timeout policy
            now: Current time (uses datetime.now if None)
            
        Returns:
            True if step has timed out
        """
        if started_at is None:
            return False

        current_time = now or datetime.now(timezone.utc)
        start_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        
        elapsed = (current_time - start_time).total_seconds()
        
        return elapsed > policy.duration_seconds

    def timeout_seconds(self, policy: TimeoutPolicy) -> int:
        """
        Get the timeout duration in seconds.
        
        Args:
            policy: The timeout policy
            
        Returns:
            Timeout duration in seconds
        """
        return policy.duration_seconds

    def remaining_time(
        self,
        started_at: str | None,
        policy: TimeoutPolicy,
        now: datetime | None = None,
    ) -> float:
        """
        Get remaining time before timeout.
        
        Args:
            started_at: ISO timestamp when step started
            policy: The timeout policy
            now: Current time (uses datetime.now if None)
            
        Returns:
            Remaining seconds (negative if already timed out)
        """
        if started_at is None:
            return float(policy.duration_seconds)

        current_time = now or datetime.now(timezone.utc)
        start_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        
        elapsed = (current_time - start_time).total_seconds()
        
        return policy.duration_seconds - elapsed
