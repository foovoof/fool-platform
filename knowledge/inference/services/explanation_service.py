from __future__ import annotations

"""
knowledge/inference/services/explanation_service.py

Explanation Service for the Knowledge Layer.

Orchestrates explanation operations.
"""
from typing import Any

from knowledge.inference.explanation.explanation_model import Explanation
from knowledge.inference.explanation.explanation_generator import ExplanationGenerator
from knowledge.inference.rules.rule_registry import Rule
from knowledge.inference.engine.inference_result import InferenceConclusion, InferenceResult
from knowledge.inference.engine.inference_session import InferenceSession


class ExplanationService:
    """
    Service for explanation management.
    
    Orchestrates:
    - Explanation generation
    - Explanation retrieval
    """
    
    def __init__(
        self,
        generator: ExplanationGenerator | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            generator: Optional explanation generator
        """
        self._generator = generator or ExplanationGenerator()
    
    def explain_rule(
        self,
        rule: Rule,
    ) -> dict[str, Any]:
        """
        Explain a rule.
        
        Args:
            rule: The rule to explain
            
        Returns:
            Explanation data
        """
        explanation = self._generator.explain_rule(rule)
        
        return {
            "success": True,
            "explanation": explanation.to_dict(),
        }
    
    def explain_conclusion(
        self,
        conclusion: InferenceConclusion,
        rule: Rule | None = None,
        evidence: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Explain a conclusion.
        
        Args:
            conclusion: The conclusion to explain
            rule: Optional rule that generated it
            evidence: Optional evidence used
            
        Returns:
            Explanation data
        """
        explanation = self._generator.explain_conclusion(
            conclusion,
            rule,
            evidence,
        )
        
        return {
            "success": True,
            "explanation": explanation.to_dict(),
        }
    
    def explain_session(
        self,
        session: InferenceSession,
    ) -> dict[str, Any]:
        """
        Explain an inference session.
        
        Args:
            session: The session to explain
            
        Returns:
            Explanation data
        """
        explanation = self._generator.explain_session(session)
        
        return {
            "success": True,
            "explanation": explanation.to_dict(),
        }
    
    def explain_result(
        self,
        result: InferenceResult,
        rules: list[Rule],
    ) -> dict[str, Any]:
        """
        Explain an inference result.
        
        Args:
            result: The result to explain
            rules: Rules used
            
        Returns:
            Explanations data
        """
        rule_map = {r.rule_id: r for r in rules}
        explanations = []
        
        for conclusion in result.conclusions:
            rule = rule_map.get(conclusion.source_rule_id)
            explanation = self._generator.explain_conclusion(
                conclusion,
                rule,
            )
            explanations.append(explanation.to_dict())
        
        return {
            "success": True,
            "conclusion_count": len(result.conclusions),
            "explanations": explanations,
        }
    
    def generate_summary(
        self,
        result: InferenceResult,
    ) -> str:
        """
        Generate a summary of inference results.
        
        Args:
            result: The result
            
        Returns:
            Summary text
        """
        parts = [
            f"Inference completed with {len(result.conclusions)} conclusion(s).",
        ]
        
        if result.recommendations:
            parts.append(
                f"{len(result.recommendations)} recommendation(s) generated."
            )
        
        if result.explanations:
            parts.append(
                f"{len(result.explanations)} explanation(s) provided."
            )
        
        return " ".join(parts)
