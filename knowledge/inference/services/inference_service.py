from __future__ import annotations

"""
knowledge/inference/services/inference_service.py

Inference Service for the Knowledge Layer.

Orchestrates inference operations.
"""
from typing import Any

from knowledge.graph.models import Graph
from knowledge.inference.engine.inference_engine import InferenceEngine
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.engine.inference_result import InferenceResult
from knowledge.inference.events.inference_events import InferenceEventEmitter
from knowledge.inference.validation.inference_validator import InferenceValidator


class InferenceService:
    """
    Service for inference operations.
    
    Orchestrates:
    - Inference sessions
    - Rule evaluation
    - Result validation
    - Event emission
    """
    
    def __init__(
        self,
        inference_engine: InferenceEngine | None = None,
        event_emitter: InferenceEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            inference_engine: Optional inference engine
            event_emitter: Optional event emitter
        """
        self._engine = inference_engine or InferenceEngine()
        self._event_emitter = event_emitter or InferenceEventEmitter()
        self._validator = InferenceValidator()
    
    def run_inference(
        self,
        graph: Graph,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Run inference on a graph.
        
        Args:
            graph: The knowledge graph
            metadata: Optional metadata
            
        Returns:
            Inference results with session info
        """
        session = self._engine.create_session(graph, metadata)
        result = self._engine.execute(session, graph)
        
        validation = self._validator.validate_result(result)
        
        return {
            "session_id": session.session_id,
            "session_status": session.status,
            "rules_evaluated": len(session.rules_evaluated),
            "rules_triggered": len(session.rules_triggered),
            "conclusions": len(result.conclusions),
            "recommendations": len(result.recommendations),
            "result": result.to_dict(),
            "validation": {
                "is_valid": validation.is_valid,
                "issues": [
                    {"type": i.issue_type, "severity": i.severity, "message": i.message}
                    for i in validation.issues
                ],
            },
        }
    
    def run_inference_with_rules(
        self,
        graph: Graph,
        rule_ids: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Run inference with specific rules.
        
        Args:
            graph: The knowledge graph
            rule_ids: Rule IDs to execute
            metadata: Optional metadata
            
        Returns:
            Inference results
        """
        session = self._engine.create_session(graph, metadata)
        result = self._engine.execute_with_rules(session, graph, rule_ids)
        
        validation = self._validator.validate_result(result)
        
        return {
            "session_id": session.session_id,
            "rules_executed": rule_ids,
            "conclusions": len(result.conclusions),
            "recommendations": len(result.recommendations),
            "result": result.to_dict(),
            "validation": {
                "is_valid": validation.is_valid,
                "issues": [
                    {"type": i.issue_type, "severity": i.severity, "message": i.message}
                    for i in validation.issues
                ],
            },
        }
    
    def get_session(self, session: InferenceSession) -> dict[str, Any]:
        """
        Get session information.
        
        Args:
            session: The session
            
        Returns:
            Session info
        """
        return session.to_dict()
    
    def get_recommendations(
        self,
        result: InferenceResult,
    ) -> list[dict[str, Any]]:
        """
        Get recommendations from inference result.
        
        Args:
            result: The inference result
            
        Returns:
            List of recommendations
        """
        return result.recommendations
