"""
threat_intelligence/campaigns/validation.py

Campaign Validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from threat_intelligence.campaigns.models import Campaign


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


class CampaignValidator:
    """Validator for campaigns."""
    
    @staticmethod
    def validate(campaign: Campaign) -> ValidationResult:
        """
        Validate a campaign.
        
        Args:
            campaign: Campaign to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not campaign.name:
            result.add_issue("Campaign name is required")
        
        if not campaign.id:
            result.add_issue("Campaign ID is required")
        
        if campaign.start_date and campaign.end_date:
            if campaign.start_date > campaign.end_date:
                result.add_issue("Start date must be before end date")
        
        if campaign.confidence_score < 0 or campaign.confidence_score > 1:
            result.add_issue("Confidence score must be between 0 and 1")
        
        return result


class TimelineValidator:
    """Validator for campaign timelines."""
    
    @staticmethod
    def validate_timeline_consistency(
        first_observed: str,
        last_observed: str,
        events: list[dict[str, Any]],
    ) -> ValidationResult:
        """
        Validate timeline consistency.
        
        Args:
            first_observed: First observed timestamp
            last_observed: Last observed timestamp
            events: List of events
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if first_observed and last_observed:
            if first_observed > last_observed:
                result.add_issue("First observed must be before last observed")
        
        return result


class AssertionValidator:
    """Validator for campaign assertions."""
    
    @staticmethod
    def validate_assertion(assertion: dict[str, Any]) -> ValidationResult:
        """
        Validate an assertion.
        
        Args:
            assertion: Assertion data
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not assertion.get("assertion"):
            result.add_issue("Assertion content is required")
        
        if not assertion.get("assertion_type"):
            result.add_issue("Assertion type is required")
        
        return result


class RelationshipValidator:
    """Validator for campaign relationships."""
    
    @staticmethod
    def validate_relationship(relationship: dict[str, Any]) -> ValidationResult:
        """
        Validate a relationship.
        
        Args:
            relationship: Relationship data
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        required_fields = [
            "campaign_id",
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
