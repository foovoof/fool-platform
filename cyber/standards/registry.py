"""
cyber/standards/registry.py

Cyber Standards Registry.

Maintains registry of supported standards and mappings.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cyber.standards.models import StandardType, StandardVersion


@dataclass
class StandardInfo:
    """Information about a registered standard."""
    standard_type: StandardType
    name: str
    version: str
    supported_versions: tuple[str, ...]
    supported_object_types: tuple[str, ...]
    description: str = ""


@dataclass
class MappingInfo:
    """Information about a registered mapping."""
    source_type: StandardType
    target_type: str
    source_object_types: tuple[str, ...]
    target_object_types: tuple[str, ...]
    is_bidirectional: bool


class CyberStandardRegistry:
    """
    Registry of supported cyber standards.
    
    Provides:
    - Standard registration
    - Standard lookup
    - Mapping lookup
    - Version information
    """
    
    def __init__(self) -> None:
        self._standards: dict[StandardType, StandardInfo] = {}
        self._mappings: dict[tuple[StandardType, str], MappingInfo] = {}
        self._register_default_standards()
    
    def _register_default_standards(self) -> None:
        """Register default supported standards."""
        self.register_standard(StandardInfo(
            standard_type=StandardType.STIX,
            name="STIX 2.x",
            version="2.1",
            supported_versions=("2.0", "2.1"),
            supported_object_types=(
                "indicator", "malware", "threat-actor", "intrusion-set",
                "attack-pattern", "vulnerability", "infrastructure", "tool",
                "campaign", "relationship", "report",
            ),
            description="Structured Threat Information Expression",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.ATTACK,
            name="MITRE ATT&CK",
            version="13.0",
            supported_versions=("8.0", "9.0", "10.0", "11.0", "12.0", "13.0"),
            supported_object_types=(
                "technique", "tactic", "group", "malware", "mitigation",
            ),
            description="MITRE ATT&CK Framework",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.CVE,
            name="CVE",
            version="5.0",
            supported_versions=("4.0", "5.0"),
            supported_object_types=("cve",),
            description="Common Vulnerabilities and Exposures",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.CWE,
            name="CWE",
            version="4.14",
            supported_versions=("4.0", "4.14"),
            supported_object_types=("cwe",),
            description="Common Weakness Enumeration",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.CAPEC,
            name="CAPEC",
            version="3.9",
            supported_versions=("3.0", "3.9"),
            supported_object_types=("capec",),
            description="Common Attack Pattern Enumeration and Classification",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.SIGMA,
            name="Sigma",
            version="0.1",
            supported_versions=("0.1",),
            supported_object_types=("sigma",),
            description="Sigma rule format",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.YARA,
            name="YARA",
            version="4.0",
            supported_versions=("3.0", "4.0"),
            supported_object_types=("yara",),
            description="YARA rule format",
        ))
        
        self.register_standard(StandardInfo(
            standard_type=StandardType.OPENIOC,
            name="OpenIOC",
            version="1.0",
            supported_versions=("1.0",),
            supported_object_types=("openioc",),
            description="OpenIOC format",
        ))
    
    def register_standard(self, info: StandardInfo) -> None:
        """Register a standard."""
        self._standards[info.standard_type] = info
    
    def get_standard(self, standard_type: StandardType) -> StandardInfo | None:
        """Get standard info by type."""
        return self._standards.get(standard_type)
    
    def list_standards(self) -> list[StandardInfo]:
        """List all registered standards."""
        return list(self._standards.values())
    
    def register_mapping(self, info: MappingInfo) -> None:
        """Register a mapping."""
        key = (info.source_type, info.target_type)
        self._mappings[key] = info
    
    def get_mapping(
        self, source_type: StandardType, target_type: str
    ) -> MappingInfo | None:
        """Get mapping info."""
        return self._mappings.get((source_type, target_type))
    
    def list_mappings(self, source_type: StandardType) -> list[MappingInfo]:
        """List all mappings for a source type."""
        return [
            m for k, m in self._mappings.items()
            if k[0] == source_type
        ]
    
    def supports_standard(self, standard_type: StandardType) -> bool:
        """Check if a standard is supported."""
        return standard_type in self._standards
    
    def supports_version(
        self, standard_type: StandardType, version: str
    ) -> bool:
        """Check if a version is supported."""
        info = self._standards.get(standard_type)
        if not info:
            return False
        return version in info.supported_versions
