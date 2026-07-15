"""
knowledge/inference/engine/inference_engine.py

Inference Engine for FOOL Platform.

Implements deterministic rule-based inference.

IMPORTANT: This engine does NOT:
- Modify the knowledge graph
- Make autonomous decisions
- Perform planning
- Use AI/LLM

This engine ONLY:
- Evaluates rules against knowledge
- Derives facts deterministically
- Generates explainable conclusions
- Produces recommendations (NOT decisions)
"""
from __future__ import annotations

from typing import Any

from knowledge.graph.models import Graph
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.engine.inference_result import InferenceResult, InferenceConclusion
from knowledge.inference.rules.rule_registry import RuleRegistry
from knowledge.inference.rules.rule_validator import RuleValidator
from knowledge.inference.rules.rule_evaluator import RuleEvaluator, EvaluationContext
from knowledge.inference.rules.rule_execution import RuleExecutor, ExecutionContext
from knowledge.inference.evidence.evidence_tracker import EvidenceTracker
from knowledge.inference.evidence.evidence_chain import EvidenceChainBuilder
from knowledge.inference.confidence.confidence_calculator import ConfidenceCalculator
from knowledge.inference.confidence.confidence_propagation import ConfidencePropagation
from knowledge.inference.explanation.explanation_generator import ExplanationGenerator
from knowledge.inference.validation.inference_validator import InferenceValidator


class InferenceEngine:
    """
    Deterministic Inference Engine.
    
    Evaluates rules against knowledge and generates conclusions.
    Does NOT modify the knowledge graph.
    Does NOT make autonomous decisions.
    """
    
    def __init__(
        self,
        rule_registry: RuleRegistry | None = None,
        event_emitter: Any = None,
    ) -> None:
        """
        Initialize the inference engine.
        
        Args:
            rule_registry: Optional rule registry
            event_emitter: Optional event emitter
        """
        self._rule_registry = rule_registry or RuleRegistry()
        self._rule_validator = RuleValidator()
        self._rule_evaluator = RuleEvaluator()
        self._rule_executor = RuleExecutor()
        self._evidence_tracker = EvidenceTracker()
        self._chain_builder = EvidenceChainBuilder()
        self._confidence_calculator = ConfidenceCalculator()
        self._confidence_propagation = ConfidencePropagation()
        self._explanation_generator = ExplanationGenerator()
        self._validator = InferenceValidator()
        self._event_emitter = event_emitter
    
    def create_session(
        self,
        graph: Graph,
        metadata: dict[str, Any] | None = None,
    ) -> InferenceSession:
        """
        Create a new inference session.
        
        Args:
            graph: The knowledge graph
            metadata: Optional session metadata
            
        Returns:
            New inference session
        """
        session = InferenceSession(
            graph_id=graph.graph_id,
            graph_version=graph.graph_version,
            metadata=metadata or {},
        )
        
        self._emit_event("knowledge.inference.session.started", {
            "session_id": session.session_id,
            "graph_id": graph.graph_id,
        })
        
        return session
    
    def execute(
        self,
        session: InferenceSession,
        graph: Graph,
    ) -> InferenceResult:
        """
        Execute inference for a session.
        
        Args:
            session: The inference session
            graph: The knowledge graph
            
        Returns:
            Inference result with conclusions and recommendations
        """
        result = InferenceResult(session_id=session.session_id)
        
        rules = self._rule_registry.list_rules(enabled_only=True)
        
        for rule in rules:
            session.add_rule_evaluated(rule.rule_id)
            
            self._emit_event("knowledge.rule.evaluated", {
                "session_id": session.session_id,
                "rule_id": rule.rule_id,
                "rule_name": rule.name,
            })
            
            eval_context = EvaluationContext(
                graph=graph,
                session_id=session.session_id,
            )
            
            eval_result = self._rule_evaluator.evaluate_rule(rule, eval_context)
            
            if eval_result.triggered:
                session.add_rule_triggered(rule.rule_id)
                
                self._emit_event("knowledge.rule.triggered", {
                    "session_id": session.session_id,
                    "rule_id": rule.rule_id,
                })
                
                for evidence_id in eval_result.evidence_ids:
                    session.add_evidence(evidence_id)
                    result.add_evidence_reference(evidence_id)
                
                exec_context = ExecutionContext(
                    graph=graph,
                    evaluation_result=eval_result,
                    session_id=session.session_id,
                )
                
                exec_result = self._rule_executor.execute_rule(rule, exec_context)
                
                for conclusion in exec_result.conclusions:
                    result.add_conclusion(conclusion)
                    session.add_conclusion(conclusion.conclusion_id)
                    
                    self._evidence_tracker.track_conclusion(
                        conclusion.conclusion_id,
                        eval_result.evidence_ids,
                        rule.rule_id,
                    )
                    
                    self._emit_event("knowledge.conclusion.generated", {
                        "session_id": session.session_id,
                        "conclusion_id": conclusion.conclusion_id,
                        "rule_id": rule.rule_id,
                        "confidence": conclusion.confidence,
                    })
                    
                    chain = self._chain_builder.build_chain(
                        conclusion.conclusion_id,
                        eval_result.evidence_ids,
                        rule.rule_id,
                    )
                    result.explanations.append(chain.to_dict())
                    
                    if conclusion.confidence < 1.0:
                        update = self._confidence_propagation.update_confidence_chain(
                            conclusion.conclusion_id,
                            conclusion.confidence,
                            rule.rule_id,
                            eval_result.evidence_ids,
                            f"Derived from rule '{rule.name}'",
                        )
                        session.add_confidence_update(update.update_id)
                
                for update in exec_result.confidence_updates:
                    result.add_confidence_update(
                        update["entity_id"],
                        0.0,
                        update["confidence"],
                        rule.rule_id,
                    )
                
                for recommendation in exec_result.recommendations:
                    result.add_recommendation(
                        recommendation.get("type", "unknown"),
                        recommendation.get("entity_id", ""),
                        recommendation.get("action", ""),
                        recommendation.get("rationale", ""),
                    )
        
        validation_result = self._validator.validate_result(result)
        if not validation_result.is_valid:
            result.metadata["validation_issues"] = [
                {
                    "type": i.issue_type,
                    "severity": i.severity,
                    "message": i.message,
                }
                for i in validation_result.issues
            ]
        
        session.mark_completed()
        
        self._emit_event("knowledge.inference.session.completed", {
            "session_id": session.session_id,
            "conclusions": len(result.conclusions),
            "recommendations": len(result.recommendations),
        })
        
        return result
    
    def execute_with_rules(
        self,
        session: InferenceSession,
        graph: Graph,
        rule_ids: list[str],
    ) -> InferenceResult:
        """
        Execute inference with specific rules.
        
        Args:
            session: The inference session
            graph: The knowledge graph
            rule_ids: Rule IDs to execute
            
        Returns:
            Inference result
        """
        result = InferenceResult(session_id=session.session_id)
        
        for rule_id in rule_ids:
            rule = self._rule_registry.get_rule(rule_id)
            if not rule or not rule.enabled:
                continue
            
            session.add_rule_evaluated(rule.rule_id)
            
            eval_context = EvaluationContext(
                graph=graph,
                session_id=session.session_id,
            )
            
            eval_result = self._rule_evaluator.evaluate_rule(rule, eval_context)
            
            if eval_result.triggered:
                session.add_rule_triggered(rule.rule_id)
                
                for evidence_id in eval_result.evidence_ids:
                    session.add_evidence(evidence_id)
                    result.add_evidence_reference(evidence_id)
                
                exec_context = ExecutionContext(
                    graph=graph,
                    evaluation_result=eval_result,
                    session_id=session.session_id,
                )
                
                exec_result = self._rule_executor.execute_rule(rule, exec_context)
                
                for conclusion in exec_result.conclusions:
                    result.add_conclusion(conclusion)
                    session.add_conclusion(conclusion.conclusion_id)
                
                for update in exec_result.confidence_updates:
                    result.add_confidence_update(
                        update["entity_id"],
                        0.0,
                        update["confidence"],
                        rule.rule_id,
                    )
                
                for recommendation in exec_result.recommendations:
                    result.add_recommendation(
                        recommendation.get("type", "unknown"),
                        recommendation.get("entity_id", ""),
                        recommendation.get("action", ""),
                        recommendation.get("rationale", ""),
                    )
        
        session.mark_completed()
        return result
    
    def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Emit an event if event emitter is configured."""
        if self._event_emitter is None:
            return
        
        try:
            if hasattr(self._event_emitter, "emit"):
                self._event_emitter.emit(event_type, data)
        except Exception:
            pass
