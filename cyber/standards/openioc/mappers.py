"""OpenIOC Mappers."""
from typing import Any
from cyber.standards.models import StandardMappingResult, StandardType


class OpenIOCMapper:
    """Maps OpenIOC objects to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "type": "indicator",
            "id": obj.get("ioc_id", ""),
            "name": obj.get("name", ""),
            "description": obj.get("description", ""),
            "items": obj.get("items", []),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.OPENIOC,
            target_type="indicator",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_openioc(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "ioc_id": fool_obj.get("id", ""),
            "name": fool_obj.get("name", ""),
            "description": fool_obj.get("description", ""),
            "items": fool_obj.get("items", []),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.OPENIOC,
            target_type="openioc",
            mapped_object=mapped,
        )
