"""
cyber/standards/services.py

Cyber Standards Services.

Orchestrates standard operations.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import (
    StandardType,
    StandardValidationResult,
    StandardMappingResult,
)
from cyber.standards.registry import CyberStandardRegistry


class StandardIntegrationService:
    """
    Coordinates standard integration operations.
    
    Orchestrates:
    - Loading standards
    - Validation
    - Mapping
    """
    
    def __init__(self, registry: CyberStandardRegistry | None = None) -> None:
        self._registry = registry or CyberStandardRegistry()
    
    @property
    def registry(self) -> CyberStandardRegistry:
        """Get the standard registry."""
        return self._registry


class ValidationService:
    """
    Coordinates validation operations.
    """
    
    def __init__(self) -> None:
        self._registry = CyberStandardRegistry()
    
    def validate(
        self, standard_type: StandardType, obj: dict[str, Any]
    ) -> StandardValidationResult:
        """
        Validate an object against its standard.
        
        Args:
            standard_type: The standard type
            obj: Object to validate
            
        Returns:
            Validation result
        """
        if standard_type == StandardType.STIX:
            from cyber.standards.stix.validators import StixValidator
            return StixValidator.validate_object(obj)
        
        elif standard_type == StandardType.ATTACK:
            from cyber.standards.attack.validators import AttackValidator
            technique = AttackValidator.validate_technique(obj)
            if technique.is_valid:
                return StandardValidationResult(is_valid=True)
            return technique
        
        elif standard_type == StandardType.CVE:
            from cyber.standards.cve.validators import CveValidator
            return CveValidator.validate(obj)
        
        elif standard_type == StandardType.CWE:
            from cyber.standards.cwe.validators import CweValidator
            return CweValidator.validate(obj)
        
        elif standard_type == StandardType.CAPEC:
            from cyber.standards.capec.validators import CapecValidator
            return CapecValidator.validate(obj)
        
        elif standard_type == StandardType.SIGMA:
            from cyber.standards.sigma.validators import SigmaValidator
            return SigmaValidator.validate(obj)
        
        elif standard_type == StandardType.YARA:
            from cyber.standards.yara.validators import YaraValidator
            return YaraValidator.validate(obj)
        
        elif standard_type == StandardType.OPENIOC:
            from cyber.standards.openioc.validators import OpenIOCValidator
            return OpenIOCValidator.validate(obj)
        
        return StandardValidationResult(
            is_valid=False,
            errors=("Unknown standard type",),
        )


class MappingService:
    """
    Coordinates mapping operations.
    """
    
    def __init__(self) -> None:
        self._registry = CyberStandardRegistry()
    
    def to_fool_domain(
        self, standard_type: StandardType, obj: dict[str, Any]
    ) -> StandardMappingResult:
        """
        Map a standard object to FOOL domain.
        
        Args:
            standard_type: The standard type
            obj: Object to map
            
        Returns:
            Mapping result
        """
        if standard_type == StandardType.STIX:
            from cyber.standards.stix.mappers import StixMapper
            return StixMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.ATTACK:
            from cyber.standards.attack.mappers import AttackMapper
            return AttackMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.CVE:
            from cyber.standards.cve.mappers import CveMapper
            return CveMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.CWE:
            from cyber.standards.cwe.mappers import CweMapper
            return CweMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.CAPEC:
            from cyber.standards.capec.mappers import CapecMapper
            return CapecMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.SIGMA:
            from cyber.standards.sigma.mappers import SigmaMapper
            return SigmaMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.YARA:
            from cyber.standards.yara.mappers import YaraMapper
            return YaraMapper.to_fool_domain(obj)
        
        elif standard_type == StandardType.OPENIOC:
            from cyber.standards.openioc.mappers import OpenIOCMapper
            return OpenIOCMapper.to_fool_domain(obj)
        
        return StandardMappingResult(
            success=False,
            source_standard=standard_type,
            errors=("Unknown standard type",),
        )


class SerializationService:
    """
    Coordinates serialization operations.
    """
    
    def serialize(
        self, standard_type: StandardType, obj: dict[str, Any]
    ) -> str:
        """Serialize an object to JSON."""
        if standard_type == StandardType.STIX:
            from cyber.standards.stix.serializers import StixSerializer
            return StixSerializer.serialize(obj)
        
        elif standard_type == StandardType.ATTACK:
            from cyber.standards.attack.serializers import AttackSerializer
            return AttackSerializer.serialize(obj)
        
        elif standard_type == StandardType.CVE:
            from cyber.standards.cve.serializers import CveSerializer
            return CveSerializer.serialize(obj)
        
        elif standard_type == StandardType.CWE:
            from cyber.standards.cwe.serializers import CweSerializer
            return CweSerializer.serialize(obj)
        
        elif standard_type == StandardType.CAPEC:
            from cyber.standards.capec.serializers import CapecSerializer
            return CapecSerializer.serialize(obj)
        
        elif standard_type == StandardType.SIGMA:
            from cyber.standards.sigma.serializers import SigmaSerializer
            return SigmaSerializer.serialize(obj)
        
        elif standard_type == StandardType.YARA:
            from cyber.standards.yara.serializers import YaraSerializer
            return YaraSerializer.serialize(obj)
        
        elif standard_type == StandardType.OPENIOC:
            from cyber.standards.openioc.serializers import OpenIOCSerializer
            return OpenIOCSerializer.serialize(obj)
        
        raise ValueError(f"Unknown standard type: {standard_type}")
    
    def deserialize(
        self, standard_type: StandardType, json_str: str
    ) -> dict[str, Any]:
        """Deserialize JSON to object."""
        if standard_type == StandardType.STIX:
            from cyber.standards.stix.serializers import StixSerializer
            return StixSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.ATTACK:
            from cyber.standards.attack.serializers import AttackSerializer
            return AttackSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.CVE:
            from cyber.standards.cve.serializers import CveSerializer
            return CveSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.CWE:
            from cyber.standards.cwe.serializers import CweSerializer
            return CweSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.CAPEC:
            from cyber.standards.capec.serializers import CapecSerializer
            return CapecSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.SIGMA:
            from cyber.standards.sigma.serializers import SigmaSerializer
            return SigmaSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.YARA:
            from cyber.standards.yara.serializers import YaraSerializer
            return YaraSerializer.deserialize(json_str)
        
        elif standard_type == StandardType.OPENIOC:
            from cyber.standards.openioc.serializers import OpenIOCSerializer
            return OpenIOCSerializer.deserialize(json_str)
        
        raise ValueError(f"Unknown standard type: {standard_type}")
