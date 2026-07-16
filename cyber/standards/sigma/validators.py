"""Sigma Validators."""
from typing import Any
from cyber.standards.models import StandardValidationResult


class SigmaValidator:
    """Validates Sigma rule metadata."""
    
    VALID_LEVELS = {"informational", "low", "medium", "high", "critical"}
    VALID_STATUSES = {"experimental", "test", "stable", "deprecated"}
    
    @classmethod
    def validate(cls, rule: dict[str, Any]) -> StandardValidationResult:
        errors = []
        warnings = []
        
        if "title" not in rule:
            errors.append("Missing required field: title")
        
        if "detection" not in rule:
            errors.append("Missing required field: detection")
        
        level = rule.get("level", "")
        if level and level.lower() not in cls.VALID_LEVELS:
            warnings.append(f"Unknown level: {level}")
        
        status = rule.get("status", "")
        if status and status.lower() not in cls.VALID_STATUSES:
            warnings.append(f"Unknown status: {status}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
