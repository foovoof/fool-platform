"""
cyber/standards/cve/mappers.py

CVE Mappers.

Maps CVE objects to/from FOOL canonical domain.
"""
from __future__ import annotations

from typing import Any

from cyber.standards.models import (
    StandardMappingResult,
    StandardType,
)


class CveMapper:
    """Maps CVE objects to FOOL domain."""
    
    @classmethod
    def to_fool_domain(cls, cve: dict[str, Any]) -> StandardMappingResult:
        """Map CVE to FOOL domain."""
        errors = []
        
        cve_id = cve.get("cve_id", "")
        if not cve_id:
            errors.append("Missing CVE ID")
            return StandardMappingResult(
                success=False,
                source_standard=StandardType.CVE,
                errors=tuple(errors),
            )
        
        mapped = {
            "type": "vulnerability",
            "id": cve_id,
            "name": cve.get("description", ""),
            "description": cve.get("description", ""),
            "severity": cve.get("severity", ""),
            "cvss_score": cve.get("cvss_score", 0.0),
            "references": cve.get("references", []),
        }
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CVE,
            target_type="vulnerability",
            mapped_object=mapped,
        )
    
    @classmethod
    def to_cve(cls, fool_obj: dict[str, Any]) -> StandardMappingResult:
        """Map FOOL domain to CVE."""
        mapped = {
            "cve_id": fool_obj.get("id", ""),
            "description": fool_obj.get("description", ""),
            "severity": fool_obj.get("severity", ""),
            "cvss_score": fool_obj.get("cvss_score", 0.0),
        }
        
        return StandardMappingResult(
            success=True,
            source_standard=StandardType.CVE,
            target_type="cve",
            mapped_object=mapped,
        )
