from __future__ import annotations

"""
knowledge/inference/services/rule_service.py

Rule Service for the Knowledge Layer.

Orchestrates rule management operations.
"""
from typing import Any

from knowledge.inference.rules.rule_registry import Rule, RuleRegistry
from knowledge.inference.rules.rule_validator import RuleValidator
from knowledge.inference.validation.rule_consistency_validator import RuleConsistencyValidator


class RuleService:
    """
    Service for rule management.
    
    Orchestrates:
    - Rule registration
    - Rule validation
    - Rule consistency checks
    """
    
    def __init__(
        self,
        rule_registry: RuleRegistry | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            rule_registry: Optional rule registry
        """
        self._registry = rule_registry or RuleRegistry()
        self._validator = RuleValidator()
        self._consistency_validator = RuleConsistencyValidator()
    
    def register_rule(self, rule: Rule) -> dict[str, Any]:
        """
        Register a new rule.
        
        Args:
            rule: The rule to register
            
        Returns:
            Registration result
        """
        validation = self._validator.validate_rule(rule)
        
        if not validation.is_valid:
            return {
                "success": False,
                "errors": [
                    {"type": i.issue_type, "message": i.message}
                    for i in validation.issues
                    if i.severity == "error"
                ],
            }
        
        success = self._registry.register_rule(rule)
        
        return {
            "success": success,
            "rule_id": rule.rule_id,
            "warnings": [
                {"type": i.issue_type, "message": i.message}
                for i in validation.issues
                if i.severity == "warning"
            ],
        }
    
    def update_rule(self, rule: Rule) -> dict[str, Any]:
        """
        Update an existing rule.
        
        Args:
            rule: The rule to update
            
        Returns:
            Update result
        """
        validation = self._validator.validate_rule(rule)
        
        if not validation.is_valid:
            return {
                "success": False,
                "errors": [
                    {"type": i.issue_type, "message": i.message}
                    for i in validation.issues
                    if i.severity == "error"
                ],
            }
        
        success = self._registry.update_rule(rule)
        
        return {
            "success": success,
            "rule_id": rule.rule_id,
        }
    
    def unregister_rule(self, rule_id: str) -> dict[str, Any]:
        """
        Unregister a rule.
        
        Args:
            rule_id: The rule ID
            
        Returns:
            Unregistration result
        """
        success = self._registry.unregister_rule(rule_id)
        
        return {
            "success": success,
            "rule_id": rule_id,
        }
    
    def get_rule(self, rule_id: str) -> dict[str, Any] | None:
        """
        Get a rule by ID.
        
        Args:
            rule_id: The rule ID
            
        Returns:
            Rule data or None
        """
        rule = self._registry.get_rule(rule_id)
        if rule:
            return rule.to_dict()
        return None
    
    def list_rules(self, enabled_only: bool = True) -> list[dict[str, Any]]:
        """
        List all rules.
        
        Args:
            enabled_only: Only return enabled rules
            
        Returns:
            List of rule data
        """
        rules = self._registry.list_rules(enabled_only)
        return [r.to_dict() for r in rules]
    
    def validate_rule(self, rule: Rule) -> dict[str, Any]:
        """
        Validate a rule.
        
        Args:
            rule: The rule to validate
            
        Returns:
            Validation result
        """
        validation = self._validator.validate_rule(rule)
        
        return {
            "is_valid": validation.is_valid,
            "issues": [
                {
                    "type": i.issue_type,
                    "severity": i.severity,
                    "message": i.message,
                    "location": i.location,
                }
                for i in validation.issues
            ],
        }
    
    def validate_consistency(self) -> dict[str, Any]:
        """
        Validate rule consistency.
        
        Returns:
            Consistency validation result
        """
        result = self._consistency_validator.validate_rules(self._registry)
        
        return {
            "is_consistent": result.is_consistent,
            "issues": [
                {
                    "type": i.issue_type,
                    "severity": i.severity,
                    "message": i.message,
                    "rule_ids": i.rule_ids,
                }
                for i in result.issues
            ],
            "circular_references": result.circular_references,
            "conflicting_rules": [
                {"rule1": r[0], "rule2": r[1]}
                for r in result.conflicting_rules
            ],
        }
