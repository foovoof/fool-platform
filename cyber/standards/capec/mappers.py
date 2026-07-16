"""CAPEC Mappers."""
from typing import Any
from cyber.standards.models import StandardMappingResult, StandardType


class CapecMapper:
    """Maps CAPEC objects to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, capec: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "type": "attack_pattern",
            "id": capec.get("capec_id", ""),
            "name": capec.get("name", ""),
            "description": capec.get("description", ""),
            "prerequisites": capec.get("prerequisites", []),
            "related_weaknesses": capec.get("related_weaknesses", []),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CAPEC,
            target_type="attack_pattern",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_capec(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "capec_id": fool_obj.get("id", ""),
            "name": fool_obj.get("name", ""),
            "description": fool_obj.get("description", ""),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CAPEC,
            target_type="capec",
            mapped_object=mapped,
        )
