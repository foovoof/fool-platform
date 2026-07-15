"""
knowledge/inference/rules/rule_evaluator.py

Rule Evaluator for Inference Engine.

Evaluates rule conditions against knowledge graph facts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge
from knowledge.inference.rules.rule_registry import (
    Rule,
    RuleCondition,
    ConditionType,
)


@dataclass
class EvaluationContext:
    """Context for rule evaluation."""
    graph: Graph
    session_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result of evaluating a single condition."""
    condition_id: str
    is_met: bool
    matched_value: Any = None
    evidence_ids: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleEvaluationResult:
    """Result of evaluating a rule."""
    rule_id: str
    triggered: bool
    conditions_met: list[EvaluationResult] = field(default_factory=list)
    conditions_not_met: list[EvaluationResult] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    context_values: dict[str, Any] = field(default_factory=dict)


class RuleEvaluator:
    """
    Evaluates rule conditions against knowledge graph facts.
    
    All evaluations are deterministic.
    No eval() or exec() used.
    """
    
    def __init__(self) -> None:
        """Initialize the rule evaluator."""
        self._handlers: dict[ConditionType, callable] = {
            ConditionType.ENTITY_EXISTS: self._evaluate_entity_exists,
            ConditionType.ATTRIBUTE_EQUALS: self._evaluate_attribute_equals,
            ConditionType.ATTRIBUTE_NOT_EQUALS: self._evaluate_attribute_not_equals,
            ConditionType.ATTRIBUTE_GREATER_THAN: self._evaluate_attribute_greater_than,
            ConditionType.ATTRIBUTE_LESS_THAN: self._evaluate_attribute_less_than,
            ConditionType.ATTRIBUTE_IN: self._evaluate_attribute_in,
            ConditionType.ATTRIBUTE_CONTAINS: self._evaluate_attribute_contains,
            ConditionType.RELATIONSHIP_EXISTS: self._evaluate_relationship_exists,
            ConditionType.RELATIONSHIP_TYPE: self._evaluate_relationship_type,
            ConditionType.IDENTITY_EXISTS: self._evaluate_identity_exists,
            ConditionType.NODE_TYPE: self._evaluate_node_type,
            ConditionType.ALL_CONDITIONS: self._evaluate_all_conditions,
            ConditionType.ANY_CONDITIONS: self._evaluate_any_conditions,
            ConditionType.NOT_CONDITION: self._evaluate_not_condition,
        }
    
    def evaluate_rule(
        self,
        rule: Rule,
        context: EvaluationContext,
    ) -> RuleEvaluationResult:
        """
        Evaluate a rule against the knowledge graph.
        
        Args:
            rule: The rule to evaluate
            context: Evaluation context
            
        Returns:
            Rule evaluation result
        """
        result = RuleEvaluationResult(
            rule_id=rule.rule_id,
            triggered=False,
        )
        
        all_conditions_met = True
        
        for condition in rule.conditions:
            condition_result = self._evaluate_condition(condition, context)
            
            if condition_result.is_met:
                result.conditions_met.append(condition_result)
            else:
                result.conditions_not_met.append(condition_result)
                all_conditions_met = False
            
            result.evidence_ids.extend(condition_result.evidence_ids)
        
        result.triggered = all_conditions_met
        
        return result
    
    def _evaluate_condition(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate a single condition."""
        handler = self._handlers.get(condition.condition_type)
        
        if handler is None:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
                details={"error": f"Unknown condition type: {condition.condition_type}"},
            )
        
        return handler(condition, context)
    
    def _evaluate_entity_exists(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate entity exists condition."""
        node = context.graph.get_node(condition.target)
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=node is not None,
            matched_value=node,
            evidence_ids=[node.node_id] if node else [],
            details={"target": condition.target},
        )
    
    def _evaluate_attribute_equals(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute equals condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
                details={"error": f"Entity {condition.target} not found"},
            )
        
        actual_value = node.attributes.get(condition.attribute)
        is_met = actual_value == condition.value
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
            details={
                "attribute": condition.attribute,
                "expected": condition.value,
                "actual": actual_value,
            },
        )
    
    def _evaluate_attribute_not_equals(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute not equals condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        actual_value = node.attributes.get(condition.attribute)
        is_met = actual_value != condition.value
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_attribute_greater_than(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute greater than condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        actual_value = node.attributes.get(condition.attribute)
        
        try:
            is_met = float(actual_value) > float(condition.value)
        except (TypeError, ValueError):
            is_met = False
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_attribute_less_than(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute less than condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        actual_value = node.attributes.get(condition.attribute)
        
        try:
            is_met = float(actual_value) < float(condition.value)
        except (TypeError, ValueError):
            is_met = False
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_attribute_in(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute in condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        actual_value = node.attributes.get(condition.attribute)
        is_met = actual_value in condition.value
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_attribute_contains(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate attribute contains condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        actual_value = str(node.attributes.get(condition.attribute, ""))
        is_met = condition.value in actual_value
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=is_met,
            matched_value=actual_value,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_relationship_exists(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate relationship exists condition."""
        edges = context.graph.get_edges_between(
            condition.target,
            condition.value,
        )
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=len(edges) > 0,
            matched_value=edges,
            evidence_ids=[e.edge_id for e in edges],
        )
    
    def _evaluate_relationship_type(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate relationship type condition."""
        edges = context.graph.get_edges_between(
            condition.target,
            condition.value,
        )
        
        from knowledge.graph.models import RelationshipType
        expected_type = RelationshipType(condition.attribute)
        
        matching_edges = [e for e in edges if e.relationship_type == expected_type]
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=len(matching_edges) > 0,
            matched_value=matching_edges,
            evidence_ids=[e.edge_id for e in matching_edges],
        )
    
    def _evaluate_identity_exists(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate identity exists condition."""
        nodes = context.graph.get_nodes_by_identity(condition.value)
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=len(nodes) > 0,
            matched_value=nodes,
            evidence_ids=[n.node_id for n in nodes],
        )
    
    def _evaluate_node_type(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate node type condition."""
        node = context.graph.get_node(condition.target)
        
        if not node:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
            )
        
        from knowledge.graph.models import NodeType
        expected_type = NodeType(condition.value)
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=node.node_type == expected_type,
            matched_value=node.node_type,
            evidence_ids=[node.node_id],
        )
    
    def _evaluate_all_conditions(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate all conditions (AND)."""
        results = [
            self._evaluate_condition(c, context)
            for c in condition.nested_conditions
        ]
        
        all_met = all(r.is_met for r in results)
        all_evidence = [e for r in results for e in r.evidence_ids]
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=all_met,
            evidence_ids=all_evidence,
        )
    
    def _evaluate_any_conditions(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate any conditions (OR)."""
        results = [
            self._evaluate_condition(c, context)
            for c in condition.nested_conditions
        ]
        
        any_met = any(r.is_met for r in results)
        all_evidence = [e for r in results for e in r.evidence_ids]
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=any_met,
            evidence_ids=all_evidence,
        )
    
    def _evaluate_not_condition(
        self,
        condition: RuleCondition,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """Evaluate NOT condition."""
        if not condition.nested_conditions:
            return EvaluationResult(
                condition_id=condition.condition_id,
                is_met=False,
                details={"error": "NOT condition requires nested conditions"},
            )
        
        nested_result = self._evaluate_all_conditions(
            condition.nested_conditions[0],
            context,
        )
        
        return EvaluationResult(
            condition_id=condition.condition_id,
            is_met=not nested_result.is_met,
            evidence_ids=nested_result.evidence_ids,
        )
