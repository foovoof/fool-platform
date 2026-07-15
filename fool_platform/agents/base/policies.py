"""
fool_platform/agents/base/policies.py

Agent Policy Framework for FOOL Platform.

Provides policy evaluation for agent operations.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from fool_platform.agents.base.agent_exceptions import AgentPolicyError
from fool_platform.agents.base.context import AgentContext
from fool_platform.agents.base.models import AgentTask


class AgentPolicyDecision(Enum):
    """Possible policy decisions."""
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"


@dataclass
class AgentPolicy:
    """
    Represents an agent policy.
    
    Defines rules for agent behavior.
    """
    policy_name: str
    enabled: bool = True
    capability_restrictions: list[str] = field(default_factory=list)
    task_restrictions: list[str] = field(default_factory=list)
    metadata_flags: dict[str, bool] = field(default_factory=dict)

    def is_enabled(self) -> bool:
        """Check if the policy is enabled."""
        return self.enabled

    def has_capability_restriction(self) -> bool:
        """Check if there are capability restrictions."""
        return len(self.capability_restrictions) > 0

    def allows_capability(self, capability_id: str) -> bool:
        """
        Check if a capability is allowed.
        
        Args:
            capability_id: The capability to check
            
        Returns:
            True if allowed
        """
        if not self.has_capability_restriction():
            return True
        # If restrictions exist, the capability must NOT be in the restricted list
        return capability_id not in self.capability_restrictions

    def has_task_restriction(self) -> bool:
        """Check if there are task restrictions."""
        return len(self.task_restrictions) > 0

    def allows_task_type(self, task_type: str) -> bool:
        """
        Check if a task type is allowed.
        
        Args:
            task_type: The task type to check
            
        Returns:
            True if allowed
        """
        if not self.has_task_restriction():
            return True
        # If restrictions exist, the task type must NOT be in the restricted list
        return task_type not in self.task_restrictions

    def get_metadata_flag(self, key: str) -> bool:
        """
        Get a metadata flag value.
        
        Args:
            key: The flag key
            
        Returns:
            Flag value or False if not set
        """
        return self.metadata_flags.get(key, False)


@dataclass
class AgentPolicyDecisionResult:
    """Result of a policy evaluation."""
    decision: AgentPolicyDecision
    policy_name: str
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_allowed(self) -> bool:
        """Check if the decision is allow."""
        return self.decision == AgentPolicyDecision.ALLOW

    @property
    def is_denied(self) -> bool:
        """Check if the decision is deny."""
        return self.decision == AgentPolicyDecision.DENY

    @property
    def is_warning(self) -> bool:
        """Check if the decision is warn."""
        return self.decision == AgentPolicyDecision.WARN


class AgentPolicyEvaluator:
    """
    Evaluates policies for agent operations.
    
    Makes decisions about whether operations should proceed.
    """

    def __init__(self, policies: list[AgentPolicy] | None = None) -> None:
        """
        Initialize the policy evaluator.
        
        Args:
            policies: List of policies to evaluate
        """
        self._policies: dict[str, AgentPolicy] = {}
        if policies:
            for policy in policies:
                self._policies[policy.policy_name] = policy

    def add_policy(self, policy: AgentPolicy) -> None:
        """
        Add a policy.
        
        Args:
            policy: The policy to add
        """
        self._policies[policy.policy_name] = policy

    def remove_policy(self, policy_name: str) -> bool:
        """
        Remove a policy.
        
        Args:
            policy_name: Name of the policy to remove
            
        Returns:
            True if removed, False if not found
        """
        if policy_name in self._policies:
            del self._policies[policy_name]
            return True
        return False

    def get_policy(self, policy_name: str) -> AgentPolicy | None:
        """
        Get a policy by name.
        
        Args:
            policy_name: Name of the policy
            
        Returns:
            The policy or None if not found
        """
        return self._policies.get(policy_name)

    def evaluate_task(
        self,
        task: AgentTask,
        context: AgentContext,
        policy_name: str | None = None,
    ) -> AgentPolicyDecisionResult:
        """
        Evaluate a task against policies.
        
        Args:
            task: The task to evaluate
            context: The execution context
            policy_name: Optional specific policy to evaluate
            
        Returns:
            Policy decision result
            
        Raises:
            AgentPolicyError: If evaluation fails
        """
        if policy_name:
            return self._evaluate_single_policy(
                policy_name, task, context
            )

        for name, policy in self._policies.items():
            result = self._evaluate_single_policy(name, task, context)
            if result.is_denied:
                return result

        return AgentPolicyDecisionResult(
            decision=AgentPolicyDecision.ALLOW,
            policy_name="default",
            reason="All policies passed",
        )

    def _evaluate_single_policy(
        self,
        policy_name: str,
        task: AgentTask,
        context: AgentContext,
    ) -> AgentPolicyDecisionResult:
        """
        Evaluate a single policy.
        
        Args:
            policy_name: Name of the policy
            task: The task to evaluate
            context: The execution context
            
        Returns:
            Policy decision result
        """
        policy = self._policies.get(policy_name)
        if not policy:
            return AgentPolicyDecisionResult(
                decision=AgentPolicyDecision.ALLOW,
                policy_name=policy_name,
                reason=f"Policy {policy_name} not found",
            )

        if not policy.is_enabled():
            return AgentPolicyDecisionResult(
                decision=AgentPolicyDecision.ALLOW,
                policy_name=policy_name,
                reason="Policy is disabled",
            )

        if policy.has_capability_restriction():
            if not policy.allows_capability(task.task_type):
                return AgentPolicyDecisionResult(
                    decision=AgentPolicyDecision.DENY,
                    policy_name=policy_name,
                    reason=f"Capability {task.task_type} is not allowed",
                )

        if policy.has_task_restriction():
            if not policy.allows_task_type(task.task_type):
                return AgentPolicyDecisionResult(
                    decision=AgentPolicyDecision.DENY,
                    policy_name=policy_name,
                    reason=f"Task type {task.task_type} is not allowed",
                )

        for flag_key, expected_value in policy.metadata_flags.items():
            actual_value = context.get_metadata(flag_key)
            if actual_value != expected_value:
                return AgentPolicyDecisionResult(
                    decision=AgentPolicyDecision.DENY,
                    policy_name=policy_name,
                    reason=f"Metadata flag {flag_key} mismatch",
                )

        return AgentPolicyDecisionResult(
            decision=AgentPolicyDecision.ALLOW,
            policy_name=policy_name,
            reason="Policy check passed",
        )

    def list_policies(self) -> list[str]:
        """
        List all policy names.
        
        Returns:
            List of policy names
        """
        return list(self._policies.keys())
