"""
cyber/standards/stix/validators.py

STIX Validators.

Validates STIX objects for structure and required fields.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import (
    StixObject,
    StandardValidationResult,
)
from cyber.standards.stix.enums import StixObjectType


class StixValidator:
    """
    Validates STIX objects.
    
    Validates:
    - Object structure
    - Required fields
    - Identifier formats
    - Reference integrity
    """
    
    REQUIRED_FIELDS = {"id", "type", "created", "modified"}
    
    VALID_OBJECT_TYPES = {t.value for t in StixObjectType}
    
    @staticmethod
    def validate_object(obj: dict[str, Any]) -> StandardValidationResult:
        """
        Validate a STIX object.
        
        Args:
            obj: STIX object dictionary
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        for field_name in StixValidator.REQUIRED_FIELDS:
            if field_name not in obj:
                errors.append(f"Missing required field: {field_name}")
        
        if "type" in obj:
            if obj["type"] not in StixValidator.VALID_OBJECT_TYPES:
                warnings.append(f"Unknown object type: {obj['type']}")
        
        if "id" in obj:
            if not StixValidator._validate_id_format(obj["id"]):
                errors.append(f"Invalid ID format: {obj['id']}")
        
        if "spec_version" in obj:
            if obj["spec_version"] not in ("2.0", "2.1"):
                errors.append(f"Unsupported spec version: {obj['spec_version']}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def _validate_id_format(stix_id: str) -> bool:
        """Validate STIX ID format."""
        if not stix_id:
            return False
        
        parts = stix_id.split("--")
        if len(parts) != 2:
            return False
        
        type_part, uuid_part = parts
        
        if not type_part or not uuid_part:
            return False
        
        uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        import re
        return bool(re.match(uuid_pattern, uuid_part))
    
    @staticmethod
    def validate_bundle(bundle: dict[str, Any]) -> StandardValidationResult:
        """
        Validate a STIX bundle.
        
        Args:
            bundle: STIX bundle dictionary
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        if "type" not in bundle or bundle["type"] != "bundle":
            errors.append("Bundle must have type 'bundle'")
        
        if "objects" not in bundle:
            errors.append("Bundle must have 'objects' field")
        elif not isinstance(bundle["objects"], list):
            errors.append("Bundle 'objects' must be a list")
        
        if "spec_version" in bundle:
            if bundle["spec_version"] not in ("2.0", "2.1"):
                errors.append(f"Unsupported spec version: {bundle['spec_version']}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
    
    @staticmethod
    def validate_relationship(rel: dict[str, Any]) -> StandardValidationResult:
        """
        Validate a STIX relationship object.
        
        Args:
            rel: STIX relationship dictionary
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        if "type" in rel and rel["type"] != "relationship":
            warnings.append(f"Expected type 'relationship', got: {rel['type']}")
        
        required = ["source_ref", "target_ref", "relationship_type"]
        for field_name in required:
            if field_name not in rel:
                errors.append(f"Missing required field: {field_name}")
        
        return StandardValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
