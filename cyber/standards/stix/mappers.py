"""
cyber/standards/stix/mappers.py

STIX Mappers.

Maps STIX objects to/from FOOL canonical domain.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import (
    StixObject,
    StandardMappingResult,
    StandardType,
)


class StixMapper:
    """
    Maps STIX objects to FOOL canonical domain.
    
    Responsibilities:
    - STIX → FOOL Domain
    - FOOL Domain → STIX
    
    Mappings are deterministic.
    """
    
    OBJECT_TYPE_MAPPING: dict[str, str] = {
        "attack-pattern": "technique",
        "malware": "malware",
        "threat-actor": "threat_actor",
        "intrusion-set": "threat_actor",
        "campaign": "campaign",
        "infrastructure": "infrastructure",
        "vulnerability": "vulnerability",
        "tool": "tool",
        "indicator": "indicator",
        "report": "report",
        "identity": "identity",
        "course-of-action": "course_of_action",
    }
    
    RELATIONSHIP_MAPPING: dict[str, str] = {
        "uses": "uses",
        "used-by": "used_by",
        "targets": "targets",
        "targeted-by": "targeted_by",
        "delivers": "delivers",
        "delivered-by": "delivered_by",
        "drops": "drops",
        "dropped-by": "dropped_by",
        "exploits": "exploits",
        "exploited-by": "exploited_by",
        "communicates-with": "communicates_with",
        "related-to": "related_to",
        "indicates": "indicates",
        "mitigates": "mitigates",
        "mitigated-by": "mitigated_by",
    }
    
    @classmethod
    def to_fool_domain(cls, stix_obj: dict[str, Any]) -> StandardMappingResult:
        """
        Map a STIX object to FOOL domain.
        
        Args:
            stix_obj: STIX object dictionary
            
        Returns:
            Mapping result
        """
        errors = []
        
        obj_type = stix_obj.get("type", "")
        fool_type = cls.OBJECT_TYPE_MAPPING.get(obj_type)
        
        if not fool_type:
            errors.append(f"Unsupported STIX type: {obj_type}")
            return StandardMappingResult(
                success=False,
                source_standard=StandardType.STIX,
                errors=tuple(errors),
            )
        
        mapped = {
            "type": fool_type,
            "id": stix_obj.get("id", ""),
            "name": stix_obj.get("name", ""),
            "description": stix_obj.get("description", ""),
            "labels": stix_obj.get("labels", []),
            "external_references": stix_obj.get("external_references", []),
            "created": stix_obj.get("created", ""),
            "modified": stix_obj.get("modified", ""),
        }
        
        if obj_type == "attack-pattern":
            mapped["kill_chain_phases"] = stix_obj.get("kill_chain_phases", [])
        
        if obj_type == "malware":
            mapped["is_family"] = stix_obj.get("is_family", True)
            mapped["aliases"] = stix_obj.get("malware_aliases", [])
        
        if obj_type == "threat-actor" or obj_type == "intrusion-set":
            mapped["threat_actor_type"] = stix_obj.get("threat_actor_types", [])
            mapped["sophistication"] = stix_obj.get("sophistication", "")
            mapped["resource_level"] = stix_obj.get("resource_level", "")
        
        if obj_type == "vulnerability":
            mapped["cvss_score"] = stix_obj.get("cvss_score", 0.0)
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.STIX,
            target_type=fool_type,
            mapped_object=mapped,
        )
    
    @classmethod
    def to_stix(cls, fool_obj: dict[str, Any], stix_type: str) -> StandardMappingResult:
        """
        Map a FOOL object to STIX.
        
        Args:
            fool_obj: FOOL domain object
            stix_type: Target STIX type
            
        Returns:
            Mapping result
        """
        errors = []
        
        stix_type_map = {v: k for k, v in cls.OBJECT_TYPE_MAPPING.items()}
        target_stix_type = stix_type_map.get(fool_obj.get("type", ""))
        
        if not target_stix_type:
            errors.append(f"Unknown FOOL type: {fool_obj.get('type')}")
            return StandardMappingResult(
                success=False,
                source_standard=StandardType.STIX,
                errors=tuple(errors),
            )
        
        mapped = {
            "type": target_stix_type,
            "id": fool_obj.get("id", ""),
            "created": fool_obj.get("created", ""),
            "modified": fool_obj.get("modified", ""),
        }
        
        if "name" in fool_obj:
            mapped["name"] = fool_obj["name"]
        
        if "description" in fool_obj:
            mapped["description"] = fool_obj["description"]
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.STIX,
            target_type=stix_type,
            mapped_object=mapped,
        )
    
    @classmethod
    def map_relationship(cls, stix_rel: dict[str, Any]) -> dict[str, Any]:
        """
        Map a STIX relationship to FOOL domain.
        
        Args:
            stix_rel: STIX relationship
            
        Returns:
            Mapped relationship
        """
        rel_type = stix_rel.get("relationship_type", "")
        fool_rel_type = cls.RELATIONSHIP_MAPPING.get(rel_type, rel_type)
        
        return {
            "type": fool_rel_type,
            "source_ref": stix_rel.get("source_ref", ""),
            "target_ref": stix_rel.get("target_ref", ""),
            "created": stix_rel.get("created", ""),
            "modified": stix_rel.get("modified", ""),
        }
