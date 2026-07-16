"""
cyber/standards/cve/__init__.py

CVE Standard Module.

CVE (Common Vulnerabilities and Exposures) support.
"""
from enum import Enum

from cyber.standards.models import (
    StandardType,
    StandardVersion,
    StandardMetadata,
    CveObject,
    StandardValidationResult,
    StandardMappingResult,
)

__all__ = [
    "StandardType",
    "StandardVersion",
    "StandardMetadata",
    "CveObject",
    "StandardValidationResult",
    "StandardMappingResult",
    "CveSeverity",
]


class CveSeverity(Enum):
    """CVE severity levels."""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
