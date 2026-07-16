"""
threat_intelligence/validation.py

Validation Module.

Provides validation for threat intelligence entities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models import (
    Indicator,
    ThreatActor,
    Campaign,
    Malware,
    Relationship,
    ConfidenceLevel,
)


@dataclass(frozen=True)
class ValidationIssue:
    """Validation issue."""
    field: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class ValidationResult:
    """Validation result."""
    is_valid: bool = True
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [
                {"field": i.field, "message": i.message, "severity": i.severity}
                for i in self.issues
            ],
        }


class IndicatorValidator:
    """Validates indicators."""
    
    @classmethod
    def validate(cls, indicator: Indicator) -> ValidationResult:
        """Validate an indicator."""
        issues = []
        
        if not indicator.id:
            issues.append(ValidationIssue("id", "ID is required"))
        
        if not indicator.value:
            issues.append(ValidationIssue("value", "Value is required"))
        
        if not indicator.indicator_type:
            issues.append(ValidationIssue("indicator_type", "Indicator type is required"))
        
        if indicator.confidence_score < 0 or indicator.confidence_score > 1:
            issues.append(ValidationIssue(
                "confidence_score",
                "Confidence score must be between 0 and 1"
            ))
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )


class ThreatActorValidator:
    """Validates threat actors."""
    
    @classmethod
    def validate(cls, actor: ThreatActor) -> ValidationResult:
        """Validate a threat actor."""
        issues = []
        
        if not actor.id:
            issues.append(ValidationIssue("id", "ID is required"))
        
        if not actor.name:
            issues.append(ValidationIssue("name", "Name is required"))
        
        if not actor.actor_type:
            issues.append(ValidationIssue("actor_type", "Actor type is required"))
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )


class CampaignValidator:
    """Validates campaigns."""
    
    @classmethod
    def validate(cls, campaign: Campaign) -> ValidationResult:
        """Validate a campaign."""
        issues = []
        
        if not campaign.id:
            issues.append(ValidationIssue("id", "ID is required"))
        
        if not campaign.name:
            issues.append(ValidationIssue("name", "Name is required"))
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )


class MalwareValidator:
    """Validates malware."""
    
    @classmethod
    def validate(cls, malware: Malware) -> ValidationResult:
        """Validate malware."""
        issues = []
        
        if not malware.id:
            issues.append(ValidationIssue("id", "ID is required"))
        
        if not malware.name:
            issues.append(ValidationIssue("name", "Name is required"))
        
        if not malware.malware_type:
            issues.append(ValidationIssue("malware_type", "Malware type is required"))
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )


class RelationshipValidator:
    """Validates relationships."""
    
    @classmethod
    def validate(cls, relationship: Relationship) -> ValidationResult:
        """Validate a relationship."""
        issues = []
        
        if not relationship.id:
            issues.append(ValidationIssue("id", "ID is required"))
        
        if not relationship.source_type:
            issues.append(ValidationIssue("source_type", "Source type is required"))
        
        if not relationship.source_id:
            issues.append(ValidationIssue("source_id", "Source ID is required"))
        
        if not relationship.target_type:
            issues.append(ValidationIssue("target_type", "Target type is required"))
        
        if not relationship.target_id:
            issues.append(ValidationIssue("target_id", "Target ID is required"))
        
        if not relationship.relationship_type:
            issues.append(ValidationIssue(
                "relationship_type",
                "Relationship type is required"
            ))
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )


class ValidationService:
    """
    Main validation service.
    
    Coordinates validation across all entity types.
    """
    
    def validate_indicator(self, indicator: Indicator) -> ValidationResult:
        """Validate an indicator."""
        return IndicatorValidator.validate(indicator)
    
    def validate_threat_actor(self, actor: ThreatActor) -> ValidationResult:
        """Validate a threat actor."""
        return ThreatActorValidator.validate(actor)
    
    def validate_campaign(self, campaign: Campaign) -> ValidationResult:
        """Validate a campaign."""
        return CampaignValidator.validate(campaign)
    
    def validate_malware(self, malware: Malware) -> ValidationResult:
        """Validate malware."""
        return MalwareValidator.validate(malware)
    
    def validate_relationship(self, relationship: Relationship) -> ValidationResult:
        """Validate a relationship."""
        return RelationshipValidator.validate(relationship)
