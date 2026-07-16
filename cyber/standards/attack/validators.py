"""
cyber/standards/attack/validators.py

ATT&CK Validators.

Validates ATT&CK objects.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import StandardValidationResult


class AttackValidator:
    """
    Validates ATT&CK objects.
    """
    
    @staticmethod
    def validate_technique(technique: dict[str, Any]) -> StandardValidationResult:
        """Validate an ATT&CK technique."""
        errors = []
        warnings = []
        
        if "id" not in technique:
            errors.append("Missing required field: id")
        
        if "name" not in technique:
            errors.append("Missing required field: name")
        
        technique_id = technique.get("id", "")
        if technique_id and not technique_id.startswith("T"):
            if "." in technique_id:
                if not technique_id.startswith("T"):
                    errors.append(f"Invalid technique ID format: {technique_id}")
            else:
                errors.append(f"Invalid technique ID format: {technique_id}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def validate_tactic(tactic: dict[str, Any]) -> StandardValidationResult:
        """Validate an ATT&CK tactic."""
        errors = []
        warnings = []
        
        if "id" not in tactic:
            errors.append("Missing required field: id")
        
        if "name" not in tactic:
            errors.append("Missing required field: name")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def validate_group(group: dict[str, Any]) -> StandardValidationResult:
        """Validate an ATT&CK group."""
        errors = []
        warnings = []
        
        if "id" not in group:
            errors.append("Missing required field: id")
        
        if "name" not in group:
            errors.append("Missing required field: name")
        
        group_id = group.get("id", "")
        if group_id and not group_id.startswith("G"):
            errors.append(f"Invalid group ID format: {group_id}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def validate_malware(malware: dict[str, Any]) -> StandardValidationResult:
        """Validate an ATT&CK malware."""
        errors = []
        warnings = []
        
        if "id" not in malware:
            errors.append("Missing required field: id")
        
        if "name" not in malware:
            errors.append("Missing required field: name")
        
        malware_id = malware.get("id", "")
        if malware_id and not malware_id.startswith("S"):
            errors.append(f"Invalid malware ID format: {malware_id}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def validate_mitigation(mitigation: dict[str, Any]) -> StandardValidationResult:
        """Validate an ATT&CK mitigation."""
        errors = []
        warnings = []
        
        if "id" not in mitigation:
            errors.append("Missing required field: id")
        
        if "name" not in mitigation:
            errors.append("Missing required field: name")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
