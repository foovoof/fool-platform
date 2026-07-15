"""
connectors/base/policies.py

Connector Policies.

Policy evaluation for connector operations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from connectors.base.models import PolicyAction, ConnectorRequest


class PolicyType(Enum):
    """Policy type."""
    SOURCE = "source"
    SIZE = "size"
    TYPE = "type"
    RATE = "rate"
    CUSTOM = "custom"


@dataclass
class PolicyRule:
    """Policy rule."""
    rule_id: str = ""
    name: str = ""
    description: str = ""
    policy_type: PolicyType = PolicyType.CUSTOM
    action: PolicyAction = PolicyAction.ALLOW
    conditions: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True
    
    def evaluate(self, request: ConnectorRequest) -> PolicyAction:
        """
        Evaluate policy against request.
        
        Args:
            request: Connector request
            
        Returns:
            Policy action
        """
        if not self.enabled:
            return PolicyAction.ALLOW
        
        if self._check_conditions(request):
            return self.action
        
        return PolicyAction.ALLOW
    
    def _check_conditions(self, request: ConnectorRequest) -> bool:
        """Check if conditions match."""
        for key, expected in self.conditions.items():
            actual = self._get_condition_value(request, key)
            if actual != expected:
                return False
        return True
    
    def _get_condition_value(
        self,
        request: ConnectorRequest,
        key: str,
    ) -> Any:
        """Get condition value from request."""
        if key == "source":
            return request.source
        elif key == "operation":
            return request.operation
        elif key == "connector_type":
            return request.connector_type.value
        elif key.startswith("inputs."):
            return request.inputs.get(key[7:])
        elif key.startswith("parameters."):
            return request.parameters.get(key[10:])
        elif key in request.metadata:
            return request.metadata[key]
        return None


@dataclass
class PolicyResult:
    """Policy evaluation result."""
    action: PolicyAction = PolicyAction.ALLOW
    matched_rules: list[str] = field(default_factory=list)
    denied_reason: str = ""
    
    def is_allowed(self) -> bool:
        return self.action == PolicyAction.ALLOW
    
    def is_denied(self) -> bool:
        return self.action == PolicyAction.DENY
    
    def is_warn(self) -> bool:
        return self.action == PolicyAction.WARN


class ConnectorPolicyEngine:
    """
    Evaluates policies for connector operations.
    
    Responsibilities:
    - Load policies
    - Evaluate requests
    - Return policy results
    """
    
    def __init__(self) -> None:
        """Initialize policy engine."""
        self._policies: list[PolicyRule] = []
        self._enabled = True
    
    def add_policy(self, policy: PolicyRule) -> None:
        """Add a policy."""
        self._policies.append(policy)
        self._policies.sort(key=lambda p: p.priority, reverse=True)
    
    def remove_policy(self, rule_id: str) -> bool:
        """Remove a policy by ID."""
        for i, policy in enumerate(self._policies):
            if policy.rule_id == rule_id:
                self._policies.pop(i)
                return True
        return False
    
    def clear_policies(self) -> None:
        """Clear all policies."""
        self._policies.clear()
    
    def enable(self) -> None:
        """Enable policy evaluation."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable policy evaluation."""
        self._enabled = False
    
    def evaluate(self, request: ConnectorRequest) -> PolicyResult:
        """
        Evaluate request against policies.
        
        Args:
            request: Connector request
            
        Returns:
            Policy result
        """
        if not self._enabled:
            return PolicyResult()
        
        result = PolicyResult()
        
        for policy in self._policies:
            if not policy.enabled:
                continue
            
            action = policy.evaluate(request)
            
            if action == PolicyAction.DENY:
                result.action = PolicyAction.DENY
                result.matched_rules.append(policy.rule_id)
                result.denied_reason = f"Policy '{policy.name}' denied: {policy.description}"
                return result
            
            elif action == PolicyAction.WARN:
                result.action = PolicyAction.WARN
                result.matched_rules.append(policy.rule_id)
            
            elif action == PolicyAction.ALLOW and policy in self._policies:
                result.matched_rules.append(policy.rule_id)
        
        return result
    
    def get_policies(self) -> list[PolicyRule]:
        """Get all policies."""
        return self._policies.copy()
    
    @classmethod
    def create_default_engine(cls) -> ConnectorPolicyEngine:
        """Create default policy engine."""
        engine = cls()
        
        engine.add_policy(PolicyRule(
            rule_id="default-allow",
            name="Default Allow",
            description="Allow all operations by default",
            action=PolicyAction.ALLOW,
            priority=-100,
        ))
        
        return engine
