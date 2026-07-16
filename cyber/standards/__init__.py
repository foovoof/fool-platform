"""
cyber/standards/__init__.py

FOOL Platform Cyber Standards Integration.

This module provides interoperability with industry cybersecurity standards.

IMPORTANT: This is an interoperability layer only.
- FOOL remains the canonical internal model.
- External standards never become the source of truth.
- No execution of rules or detection logic.
- No external feeds or network access.
- No AI/LLM integration.

Supported Standards:
- STIX 2.x (Structured Threat Information Expression)
- MITRE ATT&CK
- CVE (Common Vulnerabilities and Exposures)
- CWE (Common Weakness Enumeration)
- CAPEC (Common Attack Pattern Enumeration and Classification)
- Sigma (Detection Rules)
- YARA (Malware Detection Rules)
- OpenIOC (Open Indicators of Compromise)

Architecture:
    External Standards
            ↓
    Standard Adapters
            ↓
    FOOL Canonical Domain
            ↓
    Knowledge Graph
            ↓
    Inference
            ↓
    Correlation
            ↓
    Threat Intelligence
"""

from cyber.standards.models import (
    StandardType,
    StandardVersion,
    StandardMetadata,
    StandardValidationResult,
    StandardMappingResult,
    StixObject,
    AttackObject,
    CveObject,
    CweObject,
    CapecObject,
    SigmaRule,
    YaraRule,
    OpenIOCObject,
)

from cyber.standards.registry import CyberStandardRegistry, StandardInfo, MappingInfo
from cyber.standards.services import (
    StandardIntegrationService,
    ValidationService,
    MappingService,
    SerializationService,
)
from cyber.standards.events import (
    CyberStandardEvent,
    CyberStandardEventType,
    CyberStandardEventEmitter,
)

__all__ = [
    # Models
    "StandardType",
    "StandardVersion",
    "StandardMetadata",
    "StandardValidationResult",
    "StandardMappingResult",
    "StixObject",
    "AttackObject",
    "CveObject",
    "CweObject",
    "CapecObject",
    "SigmaRule",
    "YaraRule",
    "OpenIOCObject",
    # Registry
    "CyberStandardRegistry",
    "StandardInfo",
    "MappingInfo",
    # Services
    "StandardIntegrationService",
    "ValidationService",
    "MappingService",
    "SerializationService",
    # Events
    "CyberStandardEvent",
    "CyberStandardEventType",
    "CyberStandardEventEmitter",
]
