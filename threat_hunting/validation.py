"""
threat_hunting/validation.py

Threat Hunting Validation.
"""
from __future__ import annotations

from dataclasses import dataclass

from threat_hunting.models import Hunt, HuntHypothesis, HuntObservation, HuntFinding


@dataclass
class ValidationResult:
    """Validation result."""
    is_valid: bool = True
    issues: list[str] = None
    
    def __post_init__(self) -> None:
        if self.issues is None:
            self.issues = []
    
    def add_issue(self, issue: str) -> None:
        """Add a validation issue."""
        self.is_valid = False
        self.issues.append(issue)


class HuntValidator:
    """Validator for hunts."""
    
    @staticmethod
    def validate(hunt: Hunt) -> ValidationResult:
        """Validate hunt."""
        result = ValidationResult()
        
        if not hunt.name:
            result.add_issue("Hunt name is required")
        
        if not hunt.title:
            result.add_issue("Hunt title is required")
        
        return result


class HypothesisValidator:
    """Validator for hypotheses."""
    
    @staticmethod
    def validate(hypothesis: HuntHypothesis) -> ValidationResult:
        """Validate hypothesis."""
        result = ValidationResult()
        
        if not hypothesis.title:
            result.add_issue("Hypothesis title is required")
        
        if not hypothesis.hypothesis_text:
            result.add_issue("Hypothesis text is required")
        
        return result
    
    @staticmethod
    def validate_transition(from_status: str, to_status: str) -> ValidationResult:
        """Validate hypothesis status transition."""
        result = ValidationResult()
        
        valid_transitions = {
            "draft": ["approved", "archived"],
            "approved": ["running", "rejected", "archived"],
            "running": ["validated", "rejected", "archived"],
            "validated": ["archived"],
            "rejected": ["draft", "archived"],
            "archived": [],
        }
        
        valid_targets = valid_transitions.get(from_status, [])
        if to_status not in valid_targets:
            result.add_issue(f"Invalid transition from {from_status} to {to_status}")
        
        return result


class ObservationValidator:
    """Validator for observations."""
    
    @staticmethod
    def validate(observation: HuntObservation) -> ValidationResult:
        """Validate observation."""
        result = ValidationResult()
        
        if not observation.description:
            result.add_issue("Observation description is required")
        
        if observation.confidence_score < 0 or observation.confidence_score > 1:
            result.add_issue("Confidence score must be between 0 and 1")
        
        return result


class FindingValidator:
    """Validator for findings."""
    
    @staticmethod
    def validate(finding: HuntFinding) -> ValidationResult:
        """Validate finding."""
        result = ValidationResult()
        
        if not finding.title:
            result.add_issue("Finding title is required")
        
        if not finding.description:
            result.add_issue("Finding description is required")
        
        valid_severities = ["critical", "high", "medium", "low", "informational", "none"]
        if finding.severity and finding.severity not in valid_severities:
            result.add_issue(f"Invalid severity: {finding.severity}")
        
        return result


class EvidenceValidator:
    """Validator for evidence."""
    
    @staticmethod
    def validate_evidence_refs(evidence_refs: list) -> ValidationResult:
        """Validate evidence references."""
        result = ValidationResult()
        
        for ref in evidence_refs:
            if not ref.get("entity_id"):
                result.add_issue("Evidence reference must have entity_id")
            if not ref.get("entity_type"):
                result.add_issue("Evidence reference must have entity_type")
        
        return result


class SessionValidator:
    """Validator for hunt sessions."""
    
    @staticmethod
    def validate_session_integrity(session: dict) -> ValidationResult:
        """Validate session integrity."""
        result = ValidationResult()
        
        required_fields = ["hunt_id", "status"]
        for field in required_fields:
            if field not in session or not session[field]:
                result.add_issue(f"Session must have {field}")
        
        return result


class ExplanationValidator:
    """Validator for hunt explanations."""
    
    @staticmethod
    def validate_explanation(explanation: dict) -> ValidationResult:
        """Validate explanation."""
        result = ValidationResult()
        
        if not explanation.get("description"):
            result.add_issue("Explanation must have description")
        
        return result
