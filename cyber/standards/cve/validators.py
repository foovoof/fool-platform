"""
cyber/standards/cve/validators.py

CVE Validators.
"""
from __future__ import annotations

import re
from typing import Any

from cyber.standards.models import StandardValidationResult


class CveValidator:
    """Validates CVE objects."""
    
    CVE_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")
    
    @classmethod
    def validate(cls, cve: dict[str, Any]) -> StandardValidationResult:
        """Validate a CVE."""
        errors = []
        warnings = []
        
        if "cve_id" not in cve:
            errors.append("Missing required field: cve_id")
        else:
            cve_id = cve["cve_id"]
            if not cls.CVE_PATTERN.match(cve_id):
                errors.append(f"Invalid CVE ID format: {cve_id}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
