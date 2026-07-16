"""Sigma Mappers."""
from typing import Any
from cyber.standards.models import StandardMappingResult, StandardType


class SigmaMapper:
    """Maps Sigma rules to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, rule: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "type": "detection_rule",
            "id": rule.get("id", ""),
            "name": rule.get("title", ""),
            "description": rule.get("description", ""),
            "level": rule.get("level", ""),
            "status": rule.get("status", ""),
            "logsource": rule.get("logsource", {}),
            "detection": rule.get("detection", {}),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.SIGMA,
            target_type="detection_rule",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_sigma(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "title": fool_obj.get("name", ""),
            "description": fool_obj.get("description", ""),
            "level": fool_obj.get("level", ""),
            "detection": fool_obj.get("detection", {}),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.SIGMA,
            target_type="sigma",
            mapped_object=mapped,
        )
