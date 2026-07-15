"""
knowledge/inference/rules/rule_registry.py

Rule Registry for Inference Engine.

Provides rule storage, retrieval, and management.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


class ConditionType(Enum):
    """Types of rule conditions."""
    ENTITY_EXISTS = "entity_exists"
    ATTRIBUTE_EQUALS = "attribute_equals"
    ATTRIBUTE_NOT_EQUALS = "attribute_not_equals"
    ATTRIBUTE_GREATER_THAN = "attribute_greater_than"
    ATTRIBUTE_LESS_THAN = "attribute_less_than"
    ATTRIBUTE_IN = "attribute_in"
    ATTRIBUTE_CONTAINS = "attribute_contains"
    RELATIONSHIP_EXISTS = "relationship_exists"
    RELATIONSHIP_TYPE = "relationship_type"
    IDENTITY_EXISTS = "identity_exists"
    NODE_TYPE = "node_type"
    ALL_CONDITIONS = "all_conditions"
    ANY_CONDITIONS = "any_conditions"
    NOT_CONDITION = "not_condition"


class OutputType(Enum):
    """Types of rule outputs."""
    ADD_ATTRIBUTE = "add_attribute"
    UPDATE_ATTRIBUTE = "update_attribute"
    ADD_IDENTITY = "add_identity"
    ADD_RELATIONSHIP = "add_relationship"
    SET_CONFIDENCE = "set_confidence"
    CREATE_ENTITY = "create_entity"
    CLASSIFY_ENTITY = "classify_entity"
    GENERATE_CONCLUSION = "generate_conclusion"
    PROPAGATE_CONFIDENCE = "propagate_confidence"


@dataclass
class RuleCondition:
    """Represents a single condition in a rule."""
    condition_id: str = field(default_factory=lambda: str(uuid4()))
    condition_type: ConditionType = ConditionType.ENTITY_EXISTS
    target: str = ""
    attribute: str | None = None
    value: Any = None
    operator: str = "="
    nested_conditions: list[RuleCondition] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert condition to dictionary."""
        return {
            "condition_id": self.condition_id,
            "condition_type": self.condition_type.value,
            "target": self.target,
            "attribute": self.attribute,
            "value": self.value,
            "operator": self.operator,
            "nested_conditions": [c.to_dict() for c in self.nested_conditions],
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RuleCondition:
        """Create condition from dictionary."""
        if isinstance(data.get("condition_type"), str):
            data["condition_type"] = ConditionType(data["condition_type"])
        if "nested_conditions" in data:
            data["nested_conditions"] = [
                cls.from_dict(c) for c in data["nested_conditions"]
            ]
        return cls(**data)


@dataclass
class RuleOutput:
    """Represents a single output action of a rule."""
    output_id: str = field(default_factory=lambda: str(uuid4()))
    output_type: OutputType = OutputType.GENERATE_CONCLUSION
    target: str = ""
    attribute: str | None = None
    value: Any = None
    confidence: float = 1.0
    action: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert output to dictionary."""
        return {
            "output_id": self.output_id,
            "output_type": self.output_type.value,
            "target": self.target,
            "attribute": self.attribute,
            "value": self.value,
            "confidence": self.confidence,
            "action": self.action,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RuleOutput:
        """Create output from dictionary."""
        if isinstance(data.get("output_type"), str):
            data["output_type"] = OutputType(data["output_type"])
        return cls(**data)


@dataclass
class Rule:
    """
    Represents an inference rule.
    
    Rules define conditions and outputs for knowledge derivation.
    All rules are deterministic and explainable.
    """
    rule_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    priority: int = 0
    enabled: bool = True
    conditions: list[RuleCondition] = field(default_factory=list)
    outputs: list[RuleOutput] = field(default_factory=list)
    source_ontology: str | None = None
    source_contract: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def is_valid(self) -> bool:
        """Check if rule is valid."""
        return (
            bool(self.rule_id)
            and bool(self.name)
            and len(self.conditions) > 0
            and len(self.outputs) > 0
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "priority": self.priority,
            "enabled": self.enabled,
            "conditions": [c.to_dict() for c in self.conditions],
            "outputs": [o.to_dict() for o in self.outputs],
            "source_ontology": self.source_ontology,
            "source_contract": self.source_contract,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Rule:
        """Create rule from dictionary."""
        if "conditions" in data:
            data["conditions"] = [
                RuleCondition.from_dict(c) for c in data["conditions"]
            ]
        if "outputs" in data:
            data["outputs"] = [
                RuleOutput.from_dict(o) for o in data["outputs"]
            ]
        return cls(**data)


class RuleRegistry:
    """
    Registry for managing inference rules.
    
    Provides rule registration, retrieval, and validation.
    """
    
    def __init__(self) -> None:
        """Initialize the rule registry."""
        self._rules: dict[str, Rule] = {}
        self._rules_by_name: dict[str, str] = {}
    
    def register_rule(self, rule: Rule) -> bool:
        """
        Register a new rule.
        
        Args:
            rule: The rule to register
            
        Returns:
            True if registered successfully
        """
        if not rule.is_valid():
            return False
        
        if rule.rule_id in self._rules:
            return False
        
        self._rules[rule.rule_id] = rule
        self._rules_by_name[rule.name] = rule.rule_id
        return True
    
    def unregister_rule(self, rule_id: str) -> bool:
        """
        Unregister a rule.
        
        Args:
            rule_id: The rule ID to unregister
            
        Returns:
            True if unregistered successfully
        """
        if rule_id not in self._rules:
            return False
        
        rule = self._rules[rule_id]
        del self._rules_by_name[rule.name]
        del self._rules[rule_id]
        return True
    
    def get_rule(self, rule_id: str) -> Rule | None:
        """
        Get a rule by ID.
        
        Args:
            rule_id: The rule ID
            
        Returns:
            The rule or None
        """
        return self._rules.get(rule_id)
    
    def get_rule_by_name(self, name: str) -> Rule | None:
        """
        Get a rule by name.
        
        Args:
            name: The rule name
            
        Returns:
            The rule or None
        """
        rule_id = self._rules_by_name.get(name)
        if rule_id:
            return self._rules.get(rule_id)
        return None
    
    def list_rules(self, enabled_only: bool = True) -> list[Rule]:
        """
        List all registered rules.
        
        Args:
            enabled_only: Only return enabled rules
            
        Returns:
            List of rules
        """
        rules = list(self._rules.values())
        if enabled_only:
            rules = [r for r in rules if r.enabled]
        return sorted(rules, key=lambda r: r.priority, reverse=True)
    
    def update_rule(self, rule: Rule) -> bool:
        """
        Update an existing rule.
        
        Args:
            rule: The rule to update
            
        Returns:
            True if updated successfully
        """
        if rule.rule_id not in self._rules:
            return False
        
        old_rule = self._rules[rule.rule_id]
        if old_rule.name != rule.name:
            del self._rules_by_name[old_rule.name]
            self._rules_by_name[rule.name] = rule.rule_id
        
        rule.updated_at = datetime.now(timezone.utc).isoformat()
        self._rules[rule.rule_id] = rule
        return True
    
    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule."""
        rule = self._rules.get(rule_id)
        if rule:
            rule.enabled = True
            return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule."""
        rule = self._rules.get(rule_id)
        if rule:
            rule.enabled = False
            return True
        return False
    
    def count(self) -> int:
        """Get the number of registered rules."""
        return len(self._rules)
