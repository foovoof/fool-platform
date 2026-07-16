"""
threat_intelligence/infrastructure/__init__.py

Infrastructure Intelligence Module.

Phase 6E.6 - Infrastructure Intelligence Foundation.

Infrastructure is a governed Cyber Threat Intelligence entity.
It is NOT a scanner.
It is NOT an external data source.
It is NOT an enrichment engine.

IMPORTANT: This module does NOT perform:
- DNS Resolution
- WHOIS
- Passive DNS
- Internet Access
- External Enrichment
- Threat Hunting
- Detection Logic
"""
from threat_intelligence.infrastructure.models import (
    Infrastructure,
    InfrastructureIdentity,
    InfrastructureAlias,
    InfrastructureAssertion,
    InfrastructureEvidence,
    InfrastructureRelationship,
    InfrastructureVersion,
    InfrastructureHistory,
    InfrastructureCapability,
    InfrastructureMetadata,
    LifecycleTransition,
    LifecycleState,
)

from threat_intelligence.infrastructure.models.enums import (
    InfrastructureType,
    InfrastructureRole,
    HostingType,
    ServiceType,
    Protocol,
    InfrastructureStatus,
    AssertionStatus,
    AssertionType,
)

from threat_intelligence.infrastructure.taxonomy import (
    InfrastructureTypeRegistry,
    InfrastructureRoleRegistry,
    HostingTypeRegistry,
    ServiceTypeRegistry,
    ProtocolRegistry,
    RelationshipRegistry,
)

from threat_intelligence.infrastructure.service import InfrastructureService

from threat_intelligence.infrastructure.lifecycle import InfrastructureLifecycleService

from threat_intelligence.infrastructure.validation import (
    InfrastructureValidator,
    InfrastructureAssertionValidator,
    RelationshipValidator,
    LifecycleValidator,
    ValidationResult,
)

from threat_intelligence.infrastructure.events import (
    InfrastructureEventEmitter,
    InfrastructureEventType,
)

from threat_intelligence.infrastructure.queries import InfrastructureQueryService

__all__ = [
    # Models
    "Infrastructure",
    "InfrastructureIdentity",
    "InfrastructureAlias",
    "InfrastructureAssertion",
    "InfrastructureEvidence",
    "InfrastructureRelationship",
    "InfrastructureVersion",
    "InfrastructureHistory",
    "InfrastructureCapability",
    "InfrastructureMetadata",
    "LifecycleTransition",
    "LifecycleState",
    # Enums
    "InfrastructureType",
    "InfrastructureRole",
    "HostingType",
    "ServiceType",
    "Protocol",
    "InfrastructureStatus",
    "AssertionStatus",
    "AssertionType",
    # Taxonomy
    "InfrastructureTypeRegistry",
    "InfrastructureRoleRegistry",
    "HostingTypeRegistry",
    "ServiceTypeRegistry",
    "ProtocolRegistry",
    "RelationshipRegistry",
    # Services
    "InfrastructureService",
    "InfrastructureLifecycleService",
    # Validation
    "InfrastructureValidator",
    "InfrastructureAssertionValidator",
    "RelationshipValidator",
    "LifecycleValidator",
    "ValidationResult",
    # Events
    "InfrastructureEventEmitter",
    "InfrastructureEventType",
    # Queries
    "InfrastructureQueryService",
]
