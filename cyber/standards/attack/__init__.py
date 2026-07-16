"""
cyber/standards/attack/__init__.py

MITRE ATT&CK Standard Module.

ATT&CK framework support for FOOL Platform.
"""
from enum import Enum

from cyber.standards.models import (
    StandardType,
    StandardVersion,
    StandardMetadata,
    AttackObject,
    StandardValidationResult,
    StandardMappingResult,
)

__all__ = [
    "StandardType",
    "StandardVersion",
    "StandardMetadata",
    "AttackObject",
    "StandardValidationResult",
    "StandardMappingResult",
    "AttackTactic",
    "AttackPlatform",
]


class AttackTactic(Enum):
    """ATT&CK tactics."""
    RECONNAISSANCE = "reconnaissance"
    RESOURCE_DEVELOPMENT = "resource-development"
    INITIAL_ACCESS = "initial-access"
    EXECUTION = "execution"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege-escalation"
    DEFENSE_EVASION = "defense-evasion"
    CREDENTIAL_ACCESS = "credential-access"
    DISCOVERY = "discovery"
    LATERAL_MOVEMENT = "lateral-movement"
    COLLECTION = "collection"
    COMMAND_AND_CONTROL = "command-and-control"
    EXFILTRATION = "exfiltration"
    IMPACT = "impact"


class AttackPlatform(Enum):
    """ATT&CK platforms."""
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    NETWORK = "Network"
    OFFICE365 = "Office 365"
    GOOGLE_WORKSPACE = "Google Workspace"
    SAAS = "SaaS"
    IaaS = "IaaS"
    AZURE_AD = "Azure AD"
    CONTAINERS = "Containers"
    PRE = "PRE"
    Android = "Android"
    IOS = "iOS"
