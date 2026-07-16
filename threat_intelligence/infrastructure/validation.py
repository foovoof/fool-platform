"""
threat_intelligence/infrastructure/validation.py

Infrastructure Validation.
"""
from __future__ import annotations

from dataclasses import dataclass

from threat_intelligence.infrastructure.models import Infrastructure


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


class InfrastructureValidator:
    """Validator for infrastructure."""
    
    @staticmethod
    def validate(infra: Infrastructure) -> ValidationResult:
        """Validate infrastructure."""
        result = ValidationResult()
        
        if not infra.name:
            result.add_issue("Infrastructure name is required")
        
        if not infra.infrastructure_type:
            result.add_issue("Infrastructure type is required")
        
        if not infra.value:
            result.add_issue("Infrastructure value is required")
        
        if infra.confidence_score < 0 or infra.confidence_score > 1:
            result.add_issue("Confidence score must be between 0 and 1")
        
        return result


class InfrastructureAssertionValidator:
    """Validator for infrastructure assertions."""
    
    @staticmethod
    def validate(assertion: dict) -> ValidationResult:
        """Validate assertion."""
        result = ValidationResult()
        
        if not assertion.get("assertion"):
            result.add_issue("Assertion content is required")
        
        if not assertion.get("assertion_type"):
            result.add_issue("Assertion type is required")
        
        return result


class RelationshipValidator:
    """Validator for relationships."""
    
    @staticmethod
    def validate(relationship: dict) -> ValidationResult:
        """Validate relationship."""
        result = ValidationResult()
        
        required_fields = [
            "infrastructure_id",
            "source_type",
            "source_id",
            "target_type",
            "target_id",
            "relationship_type",
        ]
        
        for field in required_fields:
            if not relationship.get(field):
                result.add_issue(f"{field} is required")
        
        return result


class LifecycleValidator:
    """Validator for lifecycle transitions."""
    
    VALID_TRANSITIONS = {
        "draft": ["observed", "archived"],
        "observed": ["validated", "archived"],
        "validated": ["published", "archived"],
        "published": ["active", "deprecated", "archived"],
        "active": ["deprecated", "archived"],
        "deprecated": ["active", "archived"],
        "revoked": ["archived"],
        "archived": [],
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        valid_targets = cls.VALID_TRANSITIONS.get(from_status, [])
        return to_status in valid_targets
