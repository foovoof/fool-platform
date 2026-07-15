"""
knowledge/inference/explanation/explanation_generator.py

Explanation Generator for Inference Engine.

Generates human-readable explanations for inference results.
"""
from __future__ import annotations

from typing import Any

from knowledge.inference.explanation.explanation_model import Explanation
from knowledge.inference.engine.inference_result import (
    InferenceResult,
    InferenceConclusion,
)
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.rules.rule_registry import Rule
from knowledge.inference.confidence.confidence_model import ConfidenceRecord


class ExplanationGenerator:
    """
    Generates explanations for inference results.
    
    Every inference result is explainable.
    Explanations are deterministic and human-readable.
    """
    
    def __init__(self) -> None:
        """Initialize the explanation generator."""
        pass
    
    def generate_explanation(
        self,
        rule: Rule,
        evidence_ids: list[str],
        conclusions: list[InferenceConclusion],
    ) -> Explanation:
        """
        Generate an explanation for a rule evaluation.
        
        Args:
            rule: The rule evaluated
            evidence_ids: Evidence IDs used
            conclusions: Conclusions generated
            
        Returns:
            Explanation
        """
        explanation = Explanation(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            evidence_ids=evidence_ids,
            conclusion_ids=[c.conclusion_id for c in conclusions],
        )
        
        explanation.add_step(
            "rule_evaluation",
            f"Evaluating rule: {rule.name}",
            {
                "rule_id": rule.rule_id,
                "description": rule.description,
                "priority": rule.priority,
            },
        )
        
        explanation.add_step(
            "evidence_collection",
            f"Collecting evidence: {len(evidence_ids)} piece(s)",
            {"evidence_count": len(evidence_ids)},
        )
        
        for condition in rule.conditions:
            explanation.add_step(
                "condition_check",
                f"Checking condition: {condition.condition_type.value}",
                {
                    "target": condition.target,
                    "attribute": condition.attribute,
                    "value": condition.value,
                },
            )
        
        if conclusions:
            for conclusion in conclusions:
                explanation.add_step(
                    "conclusion_generated",
                    f"Generated conclusion: {conclusion.conclusion_type.value}",
                    {
                        "conclusion_id": conclusion.conclusion_id,
                        "confidence": conclusion.confidence,
                        "value": conclusion.conclusion_value,
                    },
                )
        
        explanation.generated_text = self._generate_text(explanation)
        
        return explanation
    
    def explain_rule(self, rule: Rule) -> Explanation:
        """
        Explain a rule.
        
        Args:
            rule: The rule to explain
            
        Returns:
            Explanation
        """
        explanation = Explanation(
            rule_id=rule.rule_id,
            rule_name=rule.name,
        )
        
        explanation.add_step(
            "rule_introduction",
            f"Rule: {rule.name}",
            {"rule_id": rule.rule_id, "version": rule.version},
        )
        
        explanation.add_step(
            "rule_description",
            f"Description: {rule.description}",
        )
        
        explanation.add_step(
            "conditions",
            f"Conditions ({len(rule.conditions)}):",
            [
                {
                    "type": c.condition_type.value,
                    "target": c.target,
                    "attribute": c.attribute,
                    "value": c.value,
                }
                for c in rule.conditions
            ],
        )
        
        explanation.add_step(
            "outputs",
            f"Outputs ({len(rule.outputs)}):",
            [
                {
                    "type": o.output_type.value,
                    "action": o.action,
                    "confidence": o.confidence,
                }
                for o in rule.outputs
            ],
        )
        
        explanation.generated_text = self._generate_rule_text(explanation)
        
        return explanation
    
    def explain_conclusion(
        self,
        conclusion: InferenceConclusion,
        rule: Rule | None = None,
        evidence: list[dict[str, Any]] | None = None,
    ) -> Explanation:
        """
        Explain a conclusion.
        
        Args:
            conclusion: The conclusion to explain
            rule: The rule that generated it
            evidence: Evidence used
            
        Returns:
            Explanation
        """
        explanation = Explanation(
            rule_id=rule.rule_id if rule else "",
            rule_name=rule.name if rule else "",
            evidence_ids=conclusion.evidence_ids,
            conclusion_ids=[conclusion.conclusion_id],
        )
        
        explanation.add_step(
            "conclusion",
            f"Conclusion: {conclusion.conclusion_type.value}",
            {
                "conclusion_id": conclusion.conclusion_id,
                "value": conclusion.conclusion_value,
            },
        )
        
        explanation.add_step(
            "confidence",
            f"Confidence: {conclusion.confidence:.2f}",
        )
        
        if rule:
            explanation.add_step(
                "source_rule",
                f"Derived from rule: {rule.name}",
                {"rule_id": rule.rule_id},
            )
        
        if evidence:
            explanation.add_step(
                "evidence",
                f"Supported by {len(evidence)} evidence piece(s)",
                {"evidence": evidence},
            )
        
        explanation.generated_text = self._generate_conclusion_text(
            explanation,
            conclusion,
        )
        
        return explanation
    
    def explain_session(self, session: InferenceSession) -> Explanation:
        """
        Explain an inference session.
        
        Args:
            session: The session to explain
            
        Returns:
            Explanation
        """
        explanation = Explanation(
            rule_id="session",
            rule_name=f"Session {session.session_id[:8]}",
        )
        
        explanation.add_step(
            "session_start",
            f"Session started at {session.started_at}",
            {"session_id": session.session_id},
        )
        
        explanation.add_step(
            "rules_processed",
            f"Rules evaluated: {len(session.rules_evaluated)}",
            {"evaluated": session.rules_evaluated},
        )
        
        explanation.add_step(
            "rules_triggered",
            f"Rules triggered: {len(session.rules_triggered)}",
            {"triggered": session.rules_triggered},
        )
        
        explanation.add_step(
            "evidence_used",
            f"Evidence used: {len(session.evidence_used)}",
        )
        
        explanation.add_step(
            "conclusions",
            f"Conclusions generated: {len(session.conclusions_generated)}",
        )
        
        if session.completed_at:
            explanation.add_step(
                "session_complete",
                f"Session completed at {session.completed_at}",
                {"status": session.status},
            )
        
        explanation.generated_text = self._generate_session_text(explanation)
        
        return explanation
    
    def _generate_text(self, explanation: Explanation) -> str:
        """Generate text from explanation structure."""
        parts = [
            f"Rule '{explanation.rule_name}' was evaluated.",
        ]
        
        if explanation.evidence_ids:
            parts.append(
                f"Based on {len(explanation.evidence_ids)} evidence piece(s), "
                f"{len(explanation.conclusion_ids)} conclusion(s) were generated."
            )
        
        return " ".join(parts)
    
    def _generate_rule_text(self, explanation: Explanation) -> str:
        """Generate text explaining a rule."""
        return f"Rule '{explanation.rule_name}' evaluates conditions and produces outputs deterministically."
    
    def _generate_conclusion_text(
        self,
        explanation: Explanation,
        conclusion: InferenceConclusion,
    ) -> str:
        """Generate text explaining a conclusion."""
        parts = [
            f"A {conclusion.conclusion_type.value} conclusion was generated",
            f"with confidence {conclusion.confidence:.2f}.",
        ]
        
        if conclusion.evidence_ids:
            parts.append(
                f"This conclusion is supported by {len(conclusion.evidence_ids)} "
                f"evidence piece(s)."
            )
        
        return " ".join(parts)
    
    def _generate_session_text(self, explanation: Explanation) -> str:
        """Generate text explaining a session."""
        return f"Inference session processed rules and generated conclusions."
