"""
knowledge/inference/validation/inference_validator.py

Inference Validator for Inference Engine.

Validates inference results and their components.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.inference.engine.inference_result import InferenceResult, InferenceConclusion
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.explanation.explanation_model import Explanation


@dataclass
class ValidationIssue:
    """A validation issue."""
    issue_type: str
    severity: str
    message: str
    location: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceValidationResult:
    """Result of inference validation."""
    is_valid: bool
    result_id: str
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
        if severity == "error":
            self.is_valid = False
    
    def add_warning(
        self,
        issue_type: str,
        message: str,
        location: str = "",
    ) -> None:
        """Add a warning."""
        self.add_issue(issue_type, "warning", message, location)


class InferenceValidator:
    """
    Validates inference results.
    
    Checks:
    - Conclusion validity
    - Evidence integrity
    - Confidence integrity
    - Explanation completeness
    - Session integrity
    """
    
    def validate_result(self, result: InferenceResult) -> InferenceValidationResult:
        """
        Validate an inference result.
        
        Args:
            result: The result to validate
            
        Returns:
            Validation result
        """
        validation_result = InferenceValidationResult(
            is_valid=True,
            result_id=result.result_id,
        )
        
        self._validate_conclusions(result, validation_result)
        self._validate_evidence_references(result, validation_result)
        self._validate_confidence_updates(result, validation_result)
        self._validate_explanations(result, validation_result)
        self._validate_recommendations(result, validation_result)
        
        return validation_result
    
    def validate_session(self, session: InferenceSession) -> InferenceValidationResult:
        """
        Validate an inference session.
        
        Args:
            session: The session to validate
            
        Returns:
            Validation result
        """
        validation_result = InferenceValidationResult(
            is_valid=True,
            result_id=session.session_id,
        )
        
        if not session.session_id:
            validation_result.add_issue(
                "missing_session_id",
                "error",
                "Session must have a session_id",
            )
        
        if not session.graph_id:
            validation_result.add_warning(
                "missing_graph_id",
                "Session should reference a graph",
            )
        
        if not session.started_at:
            validation_result.add_issue(
                "missing_start_time",
                "error",
                "Session must have a started_at timestamp",
            )
        
        if session.status not in ("active", "completed", "failed"):
            validation_result.add_warning(
                "invalid_status",
                f"Session has unusual status: {session.status}",
            )
        
        return validation_result
    
    def validate_conclusion(
        self,
        conclusion: InferenceConclusion,
    ) -> InferenceValidationResult:
        """
        Validate a single conclusion.
        
        Args:
            conclusion: The conclusion to validate
            
        Returns:
            Validation result
        """
        validation_result = InferenceValidationResult(
            is_valid=True,
            result_id=conclusion.conclusion_id,
        )
        
        if not conclusion.conclusion_id:
            validation_result.add_issue(
                "missing_conclusion_id",
                "error",
                "Conclusion must have a conclusion_id",
            )
        
        if conclusion.conclusion_value is None:
            validation_result.add_issue(
                "missing_value",
                "error",
                "Conclusion must have a value",
            )
        
        if not (0.0 <= conclusion.confidence <= 1.0):
            validation_result.add_issue(
                "invalid_confidence",
                "error",
                f"Confidence must be between 0.0 and 1.0, got {conclusion.confidence}",
            )
        
        if not conclusion.evidence_ids:
            validation_result.add_issue(
                "no_evidence",
                "warning",
                "Conclusion should have supporting evidence",
            )
        
        return validation_result
    
    def validate_explanation(
        self,
        explanation: Explanation,
    ) -> InferenceValidationResult:
        """
        Validate an explanation.
        
        Args:
            explanation: The explanation to validate
            
        Returns:
            Validation result
        """
        validation_result = InferenceValidationResult(
            is_valid=True,
            result_id=explanation.explanation_id,
        )
        
        if not explanation.explanation_id:
            validation_result.add_issue(
                "missing_explanation_id",
                "error",
                "Explanation must have an explanation_id",
            )
        
        if not explanation.generated_text:
            validation_result.add_warning(
                "empty_text",
                "Explanation should have generated text",
            )
        
        if not explanation.rule_id:
            validation_result.add_warning(
                "no_rule_reference",
                "Explanation should reference a rule",
            )
        
        return validation_result
    
    def _validate_conclusions(
        self,
        result: InferenceResult,
        validation_result: InferenceValidationResult,
    ) -> None:
        """Validate conclusions in a result."""
        for conclusion in result.conclusions:
            conclusion_result = self.validate_conclusion(conclusion)
            for issue in conclusion_result.issues:
                validation_result.issues.append(issue)
        
        if not result.conclusions:
            validation_result.add_warning(
                "no_conclusions",
                "Result has no conclusions",
            )
    
    def _validate_evidence_references(
        self,
        result: InferenceResult,
        validation_result: InferenceValidationResult,
    ) -> None:
        """Validate evidence references."""
        all_evidence_ids: set[str] = set()
        
        for conclusion in result.conclusions:
            all_evidence_ids.update(conclusion.evidence_ids)
        
        for evidence_id in result.evidence_references:
            if evidence_id not in all_evidence_ids:
                validation_result.add_warning(
                    "unused_evidence",
                    f"Evidence {evidence_id} is referenced but not used",
                )
    
    def _validate_confidence_updates(
        self,
        result: InferenceResult,
        validation_result: InferenceValidationResult,
    ) -> None:
        """Validate confidence updates."""
        for update in result.confidence_updates:
            if "entity_id" not in update:
                validation_result.add_issue(
                    "missing_entity_id",
                    "error",
                    "Confidence update missing entity_id",
                )
            
            if "new_confidence" in update:
                new_conf = update["new_confidence"]
                if not (0.0 <= new_conf <= 1.0):
                    validation_result.add_issue(
                        "invalid_confidence",
                        "error",
                        f"Invalid confidence: {new_conf}",
                    )
    
    def _validate_explanations(
        self,
        result: InferenceResult,
        validation_result: InferenceValidationResult,
    ) -> None:
        """Validate explanations."""
        for i, explanation in enumerate(result.explanations):
            exp_result = self.validate_explanation(explanation)
            for issue in exp_result.issues:
                issue.location = f"explanations[{i}]"
                validation_result.issues.append(issue)
    
    def _validate_recommendations(
        self,
        result: InferenceResult,
        validation_result: InferenceValidationResult,
    ) -> None:
        """Validate recommendations."""
        for i, recommendation in enumerate(result.recommendations):
            if "type" not in recommendation:
                validation_result.add_warning(
                    "missing_type",
                    f"Recommendation at {i} missing type",
                    location=f"recommendations[{i}]",
                )
            
            if "rationale" not in recommendation:
                validation_result.add_warning(
                    "missing_rationale",
                    f"Recommendation at {i} missing rationale",
                    location=f"recommendations[{i}]",
                )
