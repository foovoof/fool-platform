"""
cyber/standards/models.py

Cyber Standards Models.

Immutable dataclass models for industry standards.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class StandardType(Enum):
    """Type of cyber standard."""
    STIX = "stix"
    ATTACK = "attack"
    CVE = "cve"
    CWE = "cwe"
    CAPEC = "capec"
    SIGMA = "sigma"
    YARA = "yara"
    OPENIOC = "openioc"


class StandardVersion(Enum):
    """Standard version."""
    STIX_20 = "2.0"
    STIX_21 = "2.1"
    ATTACK_8 = "8.0"
    ATTACK_9 = "9.0"
    ATTACK_10 = "10.0"
    ATTACK_11 = "11.0"
    ATTACK_12 = "12.0"
    ATTACK_13 = "13.0"
    CVE_4 = "4.0"
    CVE_5 = "5.0"


@dataclass(frozen=True)
class StandardMetadata:
    """Metadata for a standard."""
    standard_type: StandardType = StandardType.STIX
    version: str = ""
    source: str = ""
    author: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "standard_type": self.standard_type.value,
            "version": self.version,
            "source": self.source,
            "author": self.author,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class StixObject:
    """STIX 2.x object."""
    id: str = ""
    type: str = ""
    spec_version: str = "2.1"
    created: str = ""
    modified: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "spec_version": self.spec_version,
            "created": self.created,
            "modified": self.modified,
            **self.metadata,
        }


@dataclass(frozen=True)
class AttackObject:
    """MITRE ATT&CK object."""
    id: str = ""
    name: str = ""
    description: str = ""
    external_references: tuple[dict, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "external_references": list(self.external_references),
            **self.metadata,
        }


@dataclass(frozen=True)
class CveObject:
    """CVE object."""
    cve_id: str = ""
    description: str = ""
    severity: str = ""
    cvss_score: float = 0.0
    published: str = ""
    references: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "cve_id": self.cve_id,
            "description": self.description,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "published": self.published,
            "references": list(self.references),
            **self.metadata,
        }


@dataclass(frozen=True)
class CweObject:
    """CWE object."""
    cwe_id: str = ""
    name: str = ""
    description: str = ""
    extended_description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "cwe_id": self.cwe_id,
            "name": self.name,
            "description": self.description,
            "extended_description": self.extended_description,
            **self.metadata,
        }


@dataclass(frozen=True)
class CapecObject:
    """CAPEC object."""
    capec_id: str = ""
    name: str = ""
    description: str = ""
    prerequisites: tuple[str, ...] = field(default_factory=tuple)
    related_weaknesses: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "capec_id": self.capec_id,
            "name": self.name,
            "description": self.description,
            "prerequisites": list(self.prerequisites),
            "related_weaknesses": list(self.related_weaknesses),
            **self.metadata,
        }


@dataclass(frozen=True)
class SigmaRule:
    """Sigma rule metadata."""
    rule_id: str = ""
    title: str = ""
    description: str = ""
    level: str = ""
    status: str = ""
    logsource: dict[str, str] = field(default_factory=dict)
    detection: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "status": self.status,
            "logsource": self.logsource,
            "detection": self.detection,
            **self.metadata,
        }


@dataclass(frozen=True)
class YaraRule:
    """YARA rule metadata."""
    rule_name: str = ""
    meta: dict[str, str] = field(default_factory=dict)
    strings: tuple[dict, ...] = field(default_factory=tuple)
    condition: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "meta": self.meta,
            "strings": list(self.strings),
            "condition": self.condition,
            **self.metadata,
        }


@dataclass(frozen=True)
class OpenIOCObject:
    """OpenIOC object."""
    ioc_id: str = ""
    name: str = ""
    description: str = ""
    items: tuple[dict, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ioc_id": self.ioc_id,
            "name": self.name,
            "description": self.description,
            "items": list(self.items),
            **self.metadata,
        }


@dataclass(frozen=True)
class StandardValidationResult:
    """Result of standard validation."""
    is_valid: bool = True
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class StandardMappingResult:
    """Result of standard mapping."""
    success: bool = False
    source_standard: StandardType = StandardType.STIX
    target_type: str = ""
    mapped_object: dict[str, Any] | None = None
    errors: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "source_standard": self.source_standard.value,
            "target_type": self.target_type,
            "mapped_object": self.mapped_object,
            "errors": list(self.errors),
        }
