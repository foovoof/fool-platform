"""CAPEC Validators."""
import re
from typing import Any
from cyber.standards.models import StandardValidationResult


class CapecValidator:
    """Validates CAPEC objects."""
    
    CAPEC_PATTERN = re.compile(r"^CAPEC-\d+$")
    
    @classmethod
    def validate(cls, capec: dict[str, Any]) -> StandardValidationResult:
        errors = []
        if "capec_id" not in capec:
            errors.append("Missing required field: capec_id")
        elif not cls.CAPEC_PATTERN.match(capec["capec_id"]):
            errors.append(f"Invalid CAPEC ID format: {capec['capec_id']}")
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
        )
