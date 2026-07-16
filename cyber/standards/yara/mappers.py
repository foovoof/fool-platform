"""YARA Mappers."""
from typing import Any
from cyber.standards.models import StandardMappingResult, StandardType


class YaraMapper:
    """Maps YARA rules to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, rule: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "type": "detection_rule",
            "id": rule.get("rule_name", ""),
            "name": rule.get("meta", {}).get("description", ""),
            "meta": rule.get("meta", {}),
            "strings": rule.get("strings", []),
            "condition": rule.get("condition", ""),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.YARA,
            target_type="detection_rule",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_yara(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        mapped = {
            "rule_name": fool_obj.get("id", ""),
            "meta": fool_obj.get("meta", {}),
            "strings": fool_obj.get("strings", []),
            "condition": fool_obj.get("condition", ""),
        }
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.YARA,
            target_type="yara",
            mapped_object=mapped,
        )
