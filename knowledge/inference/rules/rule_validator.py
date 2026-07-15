"""
knowledge/inference/rules/rule_validator.py

Rule Validator for Inference Engine.

Validates rule structure, references, and compliance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.inference.rules.rule_registry import (
    Rule,
    RuleCondition,
    ConditionType,
    OutputType,
)


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    issue_type: str
    severity: str
    message: str
    location: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleValidationResult:
    """Result of rule validation."""
    is_valid: bool
    rule_id: str
    issues: list[ValidationIssue] = field(default_factory=list)
    
    def add_issue(
        self,
        issue_type: str,
        severity: str,
        message: str,
        location: str = "",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add a validation issue."""
        self.issues.append(ValidationIssue(
            issue_type=issue_type,
            severity=severity,
            message=message,
            location=location,
            details=details or {},
        ))
        self.is_valid = False
    
    def add_warning(
        self,
        issue_type: str,
        message: str,
        location: str = "",
    ) -> None:
        """Add a warning."""
        self.add_issue(issue_type, "warning", message, location)


class RuleValidator:
    """
    Validates inference rules.
    
    Checks:
    - Structure validity
    - Reference validity
    - Ontology compliance
    - Contract compliance
    """
    
    def __init__(
        self,
        ontology_loader: Any = None,
        contract_validator: Any = None,
    ) -> None:
        """
        Initialize the rule validator.
        
        Args:
            ontology_loader: Optional ontology loader
            contract_validator: Optional contract validator
        """
        self._ontology_loader = ontology_loader
        self._contract_validator = contract_validator
    
    def validate_rule(self, rule: Rule) -> RuleValidationResult:
        """
        Validate a rule.
        
        Args:
            rule: The rule to validate
            
        Returns:
            Validation result
        """
        result = RuleValidationResult(is_valid=True, rule_id=rule.rule_id)
        
        self._validate_basic_structure(rule, result)
        self._validate_conditions(rule.conditions, result)
        self._validate_outputs(rule.outputs, result)
        self._validate_ontology_references(rule, result)
        self._validate_contract_references(rule, result)
        
        return result
    
    def _validate_basic_structure(
        self,
        rule: Rule,
        result: RuleValidationResult,
    ) -> None:
        """Validate basic rule structure."""
        if not rule.rule_id:
            result.add_issue(
                "missing_rule_id",
                "error",
                "Rule must have a rule_id",
            )
        
        if not rule.name:
            result.add_issue(
                "missing_name",
                "error",
                "Rule must have a name",
            )
        
        if not rule.version:
            result.add_warning(
                "missing_version",
                "Rule should have a version",
            )
        
        if len(rule.conditions) == 0:
            result.add_issue(
                "no_conditions",
                "error",
                "Rule must have at least one condition",
            )
        
        if len(rule.outputs) == 0:
            result.add_issue(
                "no_outputs",
                "error",
                "Rule must have at least one output",
            )
    
    def _validate_conditions(
        self,
        conditions: list[RuleCondition],
        result: RuleValidationResult,
        path: str = "conditions",
    ) -> None:
        """Validate rule conditions."""
        for i, condition in enumerate(conditions):
            condition_path = f"{path}[{i}]"
            
            if not condition.condition_type:
                result.add_issue(
                    "invalid_condition_type",
                    "error",
                    f"Condition at {condition_path} has no type",
                    location=condition_path,
                )
            
            if condition.condition_type in (
                ConditionType.ATTRIBUTE_EQUALS,
                ConditionType.ATTRIBUTE_NOT_EQUALS,
                ConditionType.ATTRIBUTE_GREATER_THAN,
                ConditionType.ATTRIBUTE_LESS_THAN,
            ):
                if not condition.attribute:
                    result.add_issue(
                        "missing_attribute",
                        "error",
                        f"Condition at {condition_path} requires attribute",
                        location=condition_path,
                    )
            
            if condition.condition_type in (
                ConditionType.ALL_CONDITIONS,
                ConditionType.ANY_CONDITIONS,
            ):
                if len(condition.nested_conditions) == 0:
                    result.add_warning(
                        "no_nested_conditions",
                        f"Condition at {condition_path} has no nested conditions",
                        location=condition_path,
                    )
                else:
                    self._validate_conditions(
                        condition.nested_conditions,
                        result,
                        f"{condition_path}.nested",
                    )
    
    def _validate_outputs(
        self,
        outputs: list[Any],
        result: RuleValidationResult,
        path: str = "outputs",
    ) -> None:
        """Validate rule outputs."""
        for i, output in enumerate(outputs):
            output_path = f"{path}[{i}]"
            
            if not output.output_type:
                result.add_issue(
                    "invalid_output_type",
                    "error",
                    f"Output at {output_path} has no type",
                    location=output_path,
                )
            
            if not output.action and output.output_type != OutputType.GENERATE_CONCLUSION:
                result.add_warning(
                    "missing_action",
                    f"Output at {output_path} has no action",
                    location=output_path,
                )
            
            if output.confidence < 0.0 or output.confidence > 1.0:
                result.add_issue(
                    "invalid_confidence",
                    "error",
                    f"Output at {output_path} has invalid confidence value",
                    location=output_path,
                    details={"confidence": output.confidence},
                )
    
    def _validate_ontology_references(
        self,
        rule: Rule,
        result: RuleValidationResult,
    ) -> None:
        """Validate ontology references."""
        if rule.source_ontology:
            if self._ontology_loader:
                concept = self._ontology_loader.get_concept(rule.source_ontology)
                if not concept:
                    result.add_warning(
                        "unknown_ontology_reference",
                        f"Rule references unknown ontology concept: {rule.source_ontology}",
                    )
    
    def _validate_contract_references(
        self,
        rule: Rule,
        result: RuleValidationResult,
    ) -> None:
        """Validate contract references."""
        if rule.source_contract:
            if self._contract_validator:
                contract = self._contract_validator.get_contract(rule.source_contract)
                if not contract:
                    result.add_warning(
                        "unknown_contract_reference",
                        f"Rule references unknown contract: {rule.source_contract}",
                    )
    
    def validate_rules(
        self,
        rules: list[Rule],
    ) -> dict[str, RuleValidationResult]:
        """
        Validate multiple rules.
        
        Args:
            rules: List of rules to validate
            
        Returns:
            Dictionary of rule_id -> validation result
        """
        return {rule.rule_id: self.validate_rule(rule) for rule in rules}
    
    def check_circular_references(
        self,
        rules: list[Rule],
    ) -> list[list[str]]:
        """
        Check for circular rule references.
        
        Args:
            rules: List of rules to check
            
        Returns:
            List of circular reference chains
        """
        adjacency: dict[str, set[str]] = {}
        for rule in rules:
            adjacency[rule.rule_id] = set()
            for condition in rule.conditions:
                if condition.target:
                    adjacency[rule.rule_id].add(condition.target)
        
        cycles: list[list[str]] = []
        visited: set[str] = set()
        path: list[str] = []
        
        def dfs(node_id: str) -> None:
            if node_id in path:
                cycle_start = path.index(node_id)
                cycles.append(path[cycle_start:] + [node_id])
                return
            
            if node_id in visited:
                return
            
            visited.add(node_id)
            path.append(node_id)
            
            for neighbor in adjacency.get(node_id, set()):
                dfs(neighbor)
            
            path.pop()
        
        for node_id in adjacency:
            if node_id not in visited:
                dfs(node_id)
        
        return cycles
