"""YARA Validators."""
from typing import Any
from cyber.standards.models import StandardValidationResult


class YaraValidator:
    """Validates YARA rule metadata."""
    
    @classmethod
    def validate(cls, rule: dict[str, Any]) -> StandardValidationResult:
        errors = []
        warnings = []
        
        if "rule_name" not in rule:
            errors.append("Missing required field: rule_name")
        
        if "condition" not in rule:
            warnings.append("No condition defined")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
