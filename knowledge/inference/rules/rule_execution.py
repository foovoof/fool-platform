"""
knowledge/inference/rules/rule_execution.py

Rule Execution for Inference Engine.

Executes rule outputs and generates conclusions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from knowledge.graph.models import Graph, Node
from knowledge.inference.rules.rule_registry import (
    Rule,
    RuleOutput,
    OutputType,
)
from knowledge.inference.rules.rule_evaluator import RuleEvaluationResult
from knowledge.inference.engine.inference_result import InferenceConclusion, ConclusionType


@dataclass
class ExecutionContext:
    """Context for rule execution."""
    graph: Graph
    evaluation_result: RuleEvaluationResult
    session_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """Result of executing a rule output."""
    output_id: str
    executed: bool
    conclusion: InferenceConclusion | None = None
    generated_entity: dict[str, Any] | None = None
    confidence_update: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class RuleExecutionResult:
    """Result of executing a rule."""
    rule_id: str
    executed_outputs: list[ExecutionResult] = field(default_factory=list)
    conclusions: list[InferenceConclusion] = field(default_factory=list)
    generated_entities: list[dict[str, Any]] = field(default_factory=list)
    confidence_updates: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)


class RuleExecutor:
    """
    Executes rule outputs and generates conclusions.
    
    Executions are deterministic and generate recommendations,
    NOT direct graph modifications.
    """
    
    def __init__(self) -> None:
        """Initialize the rule executor."""
        self._handlers: dict[OutputType, callable] = {
            OutputType.ADD_ATTRIBUTE: self._execute_add_attribute,
            OutputType.UPDATE_ATTRIBUTE: self._execute_update_attribute,
            OutputType.ADD_IDENTITY: self._execute_add_identity,
            OutputType.ADD_RELATIONSHIP: self._execute_add_relationship,
            OutputType.SET_CONFIDENCE: self._execute_set_confidence,
            OutputType.CREATE_ENTITY: self._execute_create_entity,
            OutputType.CLASSIFY_ENTITY: self._execute_classify_entity,
            OutputType.GENERATE_CONCLUSION: self._execute_generate_conclusion,
            OutputType.PROPAGATE_CONFIDENCE: self._execute_propagate_confidence,
        }
    
    def execute_rule(
        self,
        rule: Rule,
        context: ExecutionContext,
    ) -> RuleExecutionResult:
        """
        Execute a rule's outputs.
        
        Args:
            rule: The rule to execute
            context: Execution context
            
        Returns:
            Rule execution result
        """
        result = RuleExecutionResult(rule_id=rule.rule_id)
        
        if not context.evaluation_result.triggered:
            return result
        
        for output in rule.outputs:
            execution_result = self._execute_output(output, rule, context)
            result.executed_outputs.append(execution_result)
            
            if execution_result.conclusion:
                result.conclusions.append(execution_result.conclusion)
            
            if execution_result.generated_entity:
                result.generated_entities.append(
                    execution_result.generated_entity
                )
            
            if execution_result.confidence_update:
                result.confidence_updates.append(
                    execution_result.confidence_update
                )
        
        self._generate_recommendations(rule, result, context)
        
        return result
    
    def _execute_output(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute a single output."""
        handler = self._handlers.get(output.output_type)
        
        if handler is None:
            return ExecutionResult(
                output_id=output.output_id,
                executed=False,
                error=f"Unknown output type: {output.output_type}",
            )
        
        return handler(output, rule, context)
    
    def _execute_add_attribute(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute add attribute output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.ATTRIBUTE,
            conclusion_value={
                "entity_id": output.target,
                "attribute": output.attribute,
                "value": output.value,
            },
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        recommendation = {
            "type": "add_attribute",
            "entity_id": output.target,
            "attribute": output.attribute,
            "value": output.value,
            "confidence": output.confidence,
            "rationale": f"Rule '{rule.name}' recommends adding attribute",
        }
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_update_attribute(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute update attribute output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.ATTRIBUTE,
            conclusion_value={
                "entity_id": output.target,
                "attribute": output.attribute,
                "old_value": None,
                "new_value": output.value,
            },
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_add_identity(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute add identity output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.IDENTITY,
            conclusion_value={
                "entity_id": output.target,
                "identity_ref": output.value,
            },
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_add_relationship(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute add relationship output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.RELATIONSHIP,
            conclusion_value={
                "source_id": output.target,
                "target_id": output.value,
                "relationship_type": output.attribute,
            },
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_set_confidence(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute set confidence output."""
        confidence_update = {
            "entity_id": output.target,
            "confidence": output.confidence,
            "rule_id": rule.rule_id,
            "evidence_ids": context.evaluation_result.evidence_ids,
        }
        
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.FACT,
            conclusion_value=confidence_update,
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
            confidence_update=confidence_update,
        )
    
    def _execute_create_entity(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute create entity output."""
        entity = {
            "entity_type": output.attribute,
            "attributes": output.value or {},
            "confidence": output.confidence,
            "evidence_ids": context.evaluation_result.evidence_ids,
            "source_rule_id": rule.rule_id,
        }
        
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.FACT,
            conclusion_value=entity,
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
            generated_entity=entity,
        )
    
    def _execute_classify_entity(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute classify entity output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.CLASSIFICATION,
            conclusion_value={
                "entity_id": output.target,
                "classification": output.value,
            },
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_generate_conclusion(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute generate conclusion output."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.DERIVATION,
            conclusion_value=output.value,
            evidence_ids=context.evaluation_result.evidence_ids,
            confidence=output.confidence,
            source_rule_id=rule.rule_id,
            metadata=output.metadata,
        )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=True,
            conclusion=conclusion,
        )
    
    def _execute_propagate_confidence(
        self,
        output: RuleOutput,
        rule: Rule,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute propagate confidence output."""
        node = context.graph.get_node(output.target)
        
        if node:
            confidence_update = {
                "entity_id": output.target,
                "confidence": output.confidence,
                "rule_id": rule.rule_id,
                "evidence_ids": context.evaluation_result.evidence_ids,
                "propagated": True,
            }
            
            return ExecutionResult(
                output_id=output.output_id,
                executed=True,
                confidence_update=confidence_update,
            )
        
        return ExecutionResult(
            output_id=output.output_id,
            executed=False,
            error=f"Entity {output.target} not found",
        )
    
    def _generate_recommendations(
        self,
        rule: Rule,
        result: RuleExecutionResult,
        context: ExecutionContext,
    ) -> None:
        """Generate recommendations from execution result."""
        for conclusion in result.conclusions:
            if conclusion.conclusion_type == ConclusionType.ATTRIBUTE:
                value = conclusion.conclusion_value
                result.recommendations.append({
                    "type": "update_attribute",
                    "entity_id": value.get("entity_id"),
                    "attribute": value.get("attribute"),
                    "action": "add_or_update",
                    "rationale": f"Derived from rule '{rule.name}'",
                })
            
            elif conclusion.conclusion_type == ConclusionType.RELATIONSHIP:
                value = conclusion.conclusion_value
                result.recommendations.append({
                    "type": "add_relationship",
                    "source_id": value.get("source_id"),
                    "target_id": value.get("target_id"),
                    "relationship_type": value.get("relationship_type"),
                    "rationale": f"Derived from rule '{rule.name}'",
                })
