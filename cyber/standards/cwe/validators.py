"""CWE Validators."""
import re
from typing import Any
from cyber.standards.models import StandardValidationResult


class CweValidator:
    """Validates CWE objects."""
    
    CWE_PATTERN = re.compile(r"^CWE-\d+$")
    
    @classmethod
    def validate(cls, cwe: dict[str, Any]) -> StandardValidationResult:
        errors = []
        if "cwe_id" not in cwe:
            errors.append("Missing required field: cwe_id")
        elif not cls.CWE_PATTERN.match(cwe["cwe_id"]):
            errors.append(f"Invalid CWE ID format: {cwe['cwe_id']}")
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
        )
