"""OpenIOC Validators."""
from typing import Any
from cyber.standards.models import StandardValidationResult


class OpenIOCValidator:
    """Validates OpenIOC objects."""
    
    @classmethod
    def validate(cls, obj: dict[str, Any]) -> StandardValidationResult:
        errors = []
        warnings = []
        
        if "ioc_id" not in obj:
            errors.append("Missing required field: ioc_id")
        
        if "name" not in obj:
            warnings.append("No name provided")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
