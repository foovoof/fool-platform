"""
knowledge/inference/validation/rule_consistency_validator.py

Rule Consistency Validator for Inference Engine.

Validates rule consistency and detects circular references.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.inference.rules.rule_registry import Rule, RuleRegistry


@dataclass
class ConsistencyIssue:
    """A consistency issue."""
    issue_type: str
    severity: str
    message: str
    rule_ids: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsistencyResult:
    """Result of consistency validation."""
    is_consistent: bool
    issues: list[ConsistencyIssue] = field(default_factory=list)
    circular_references: list[list[str]] = field(default_factory=list)
    conflicting_rules: list[tuple[str, str]] = field(default_factory=list)
    
    def add_issue(
        self,
        issue_type: str,
        severity: str,
        message: str,
        rule_ids: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add a consistency issue."""
        self.issues.append(ConsistencyIssue(
            issue_type=issue_type,
            severity=severity,
            message=message,
            rule_ids=rule_ids or [],
            details=details or {},
        ))
        if severity == "error":
            self.is_consistent = False


class RuleConsistencyValidator:
    """
    Validates rule consistency.
    
    Checks:
    - Circular references
    - Conflicting rules
    - Unreachable rules
    - Orphan rules
    """
    
    def validate_rules(
        self,
        registry: RuleRegistry,
    ) -> ConsistencyResult:
        """
        Validate all rules in a registry.
        
        Args:
            registry: The rule registry
            
        Returns:
            Consistency result
        """
        rules = registry.list_rules(enabled_only=False)
        result = ConsistencyResult(is_consistent=True)
        
        self._check_circular_references(rules, result)
        self._check_conflicting_rules(rules, result)
        self._check_rule_dependencies(rules, result)
        self._check_orphan_rules(rules, result)
        
        return result
    
    def _check_circular_references(
        self,
        rules: list[Rule],
        result: ConsistencyResult,
    ) -> None:
        """Check for circular rule references."""
        adjacency: dict[str, set[str]] = {}
        rule_map: dict[str, Rule] = {}
        
        for rule in rules:
            adjacency[rule.rule_id] = set()
            rule_map[rule.rule_id] = rule
            
            for condition in rule.conditions:
                if condition.target:
                    adjacency[rule.rule_id].add(condition.target)
        
        visited: set[str] = set()
        path: list[str] = []
        
        def dfs(node_id: str) -> list[str] | None:
            if node_id in path:
                cycle_start = path.index(node_id)
                return path[cycle_start:] + [node_id]
            
            if node_id in visited:
                return None
            
            visited.add(node_id)
            path.append(node_id)
            
            for neighbor in adjacency.get(node_id, set()):
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            
            path.pop()
            return None
        
        for rule_id in adjacency:
            if rule_id not in visited:
                cycle = dfs(rule_id)
                if cycle:
                    result.circular_references.append(cycle)
                    result.add_issue(
                        "circular_reference",
                        "error",
                        f"Circular reference detected: {' -> '.join(cycle[:5])}",
                        rule_ids=cycle,
                    )
    
    def _check_conflicting_rules(
        self,
        rules: list[Rule],
        result: ConsistencyResult,
    ) -> None:
        """Check for conflicting rules."""
        rule_by_name: dict[str, Rule] = {}
        
        for rule in rules:
            if rule.name in rule_by_name:
                existing = rule_by_name[rule.name]
                result.conflicting_rules.append((existing.rule_id, rule.rule_id))
                result.add_issue(
                    "duplicate_name",
                    "error",
                    f"Multiple rules with name '{rule.name}'",
                    rule_ids=[existing.rule_id, rule.rule_id],
                )
            rule_by_name[rule.name] = rule
        
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i + 1:]:
                if self._rules_conflict(rule1, rule2):
                    result.conflicting_rules.append((rule1.rule_id, rule2.rule_id))
                    result.add_issue(
                        "conflicting_rules",
                        "warning",
                        f"Rules '{rule1.name}' and '{rule2.name}' may conflict",
                        rule_ids=[rule1.rule_id, rule2.rule_id],
                    )
    
    def _rules_conflict(self, rule1: Rule, rule2: Rule) -> bool:
        """Check if two rules conflict."""
        if rule1.conditions == rule2.conditions:
            if rule1.outputs != rule2.outputs:
                return True
        
        return False
    
    def _check_rule_dependencies(
        self,
        rules: list[Rule],
        result: ConsistencyResult,
    ) -> None:
        """Check for unreachable rules."""
        reachable: set[str] = set()
        rule_ids = {r.rule_id for r in rules}
        
        for rule in rules:
            for condition in rule.conditions:
                if condition.target in rule_ids:
                    reachable.add(condition.target)
        
        for rule in rules:
            if rule.rule_id not in reachable:
                result.add_issue(
                    "unreachable_rule",
                    "warning",
                    f"Rule '{rule.name}' has no dependencies",
                    rule_ids=[rule.rule_id],
                )
    
    def _check_orphan_rules(
        self,
        rules: list[Rule],
        result: ConsistencyResult,
    ) -> None:
        """Check for orphan rules (no inputs, no outputs)."""
        for rule in rules:
            has_input = any(c.target for c in rule.conditions)
            has_output = any(o.target or o.value for o in rule.outputs)
            
            if not has_input and not has_output:
                result.add_issue(
                    "orphan_rule",
                    "warning",
                    f"Rule '{rule.name}' has no inputs or outputs",
                    rule_ids=[rule.rule_id],
                )
