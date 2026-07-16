"""CWE Mappers."""
from typing import Any
from cyber.standards.models import StandardMappingResult, StandardType


class CweMapper:
    """Maps CWE objects to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, cwe: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "type": "weakness",
            "id": cwe.get("cwe_id", ""),
            "name": cwe.get("name", ""),
            "description": cwe.get("description", ""),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CWE,
            target_type="weakness",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_cwe(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "cwe_id": fool_obj.get("id", ""),
            "name": fool_obj.get("name", ""),
            "description": fool_obj.get("description", ""),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CWE,
            target_type="cwe",
            mapped_object=mapped,
        )
