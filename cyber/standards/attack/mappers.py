"""
cyber/standards/attack/mappers.py

ATT&CK Mappers.

Maps ATT&CK objects to/from FOOL canonical domain.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import (
    StandardMappingResult,
    StandardType,
)


class AttackMapper:
    """
    Maps ATT&CK objects to FOOL domain.
    """
    
    @classmethod
    def to_fool_domain(cls, attack_obj: dict[str, Any]) -> StandardMappingResult:
        """
        Map an ATT&CK object to FOOL domain.
        
        Args:
            attack_obj: ATT&CK object dictionary
            
        Returns:
            Mapping result
        """
        errors = []
        
        attack_id = attack_obj.get("id", "")
        
        if attack_id.startswith("T"):
            fool_type = "technique"
        elif attack_id.startswith("G"):
            fool_type = "threat_actor"
        elif attack_id.startswith("S"):
            fool_type = "malware"
        elif attack_id.startswith("M"):
            fool_type = "course_of_action"
        else:
            errors.append(f"Unknown ATT&CK ID format: {attack_id}")
            return StandardMappingResult(
                success=False,
                source_standard=StandardType.ATTACK,
                errors=tuple(errors),
            )
        
        mapped = {
            "type": fool_type,
            "id": attack_id,
            "name": attack_obj.get("name", ""),
            "description": attack_obj.get("description", ""),
            "external_references": attack_obj.get("external_references", []),
        }
        
        if " Techniques" in attack_obj:
            mapped["techniques"] = attack_obj.get(" Techniques", [])
        
        if "tactics" in attack_obj:
            mapped["tactics"] = attack_obj.get("tactics", [])
        
        if "groups" in attack_obj:
            mapped["groups"] = attack_obj.get("groups", [])
        
        if "software" in attack_obj:
            mapped["software"] = attack_obj.get("software", [])
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.ATTACK,
            target_type=fool_type,
            mapped_object=mapped,
        )
    
    @classmethod
    def to_attack(cls, fool_obj: dict[str, Any], attack_type: str) -> StandardMappingResult:
        """
        Map a FOOL object to ATT&CK.
        
        Args:
            fool_obj: FOOL domain object
            attack_type: Target ATT&CK type
            
        Returns:
            Mapping result
        """
        errors = []
        
        attack_prefix_map = {
            "technique": "T",
            "threat_actor": "G",
            "malware": "S",
            "course_of_action": "M",
        }
        
        prefix = attack_prefix_map.get(attack_type)
        if not prefix:
            errors.append(f"Unknown FOOL type: {attack_type}")
            return StandardMappingResult(
                success=False,
                source_standard=StandardType.ATTACK,
                errors=tuple(errors),
            )
        
        mapped = {
            "id": fool_obj.get("id", f"{prefix}0000"),
            "name": fool_obj.get("name", ""),
            "description": fool_obj.get("description", ""),
        }
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.ATTACK,
            target_type=attack_type,
            mapped_object=mapped,
        )
