"""
threat_intelligence/products/__init__.py

Intelligence Products Module.

Phase 6E.9 - Intelligence Reports & Products Foundation.

IMPORTANT: This module does NOT perform:
- PDF Generation
- HTML Reports
- Markdown Rendering
- Dashboards
- Visualizations
- AI Summary
- Natural Language Generation
- Templates Engine
- Email Distribution
- TAXII
- STIX Export
- MISP Export
- IOC Feeds
- External APIs

Products reference canonical intelligence entities.
Products never duplicate knowledge.
"""
from threat_intelligence.products.models import (
    IntelligenceProduct,
    ThreatReport,
    TechnicalReport,
    StrategicReport,
    OperationalReport,
    TacticalReport,
    ExecutiveSummary,
    ProductMetadata,
    ProductAssertion,
    ProductEvidence,
    ProductConfidence,
    ProductProvenance,
    ProductVersion,
    ProductHistory,
    LifecycleTransition,
    LifecycleState,
    ApprovalRecord,
)

from threat_intelligence.products.models.enums import (
    ProductType,
    ProductStatus,
    ClassificationLevel,
    SensitivityLevel,
    AudienceType,
    AssertionStatus,
    AssertionType,
    CreationMethod,
)

from threat_intelligence.products.registries import (
    ProductTypeRegistry,
    ClassificationRegistry,
    SensitivityRegistry,
    AudienceRegistry,
    LifecycleRegistry,
    VersionRegistry,
    RelationshipRegistry,
    AssertionTypeRegistry,
    EvidenceTypeRegistry,
)

from threat_intelligence.products.service import ProductService, LifecycleService

from threat_intelligence.products.validation import (
    ProductValidator,
    StructureValidator,
    LifecycleValidator,
    ReferenceValidator,
    VersionValidator,
    RegistryValidator,
    ValidationResult,
)

from threat_intelligence.products.events import ProductEventEmitter, ProductEventType

from threat_intelligence.products.queries import ProductQueryService

__all__ = [
    # Models
    "IntelligenceProduct",
    "ThreatReport",
    "TechnicalReport",
    "StrategicReport",
    "OperationalReport",
    "TacticalReport",
    "ExecutiveSummary",
    "ProductMetadata",
    "ProductAssertion",
    "ProductEvidence",
    "ProductConfidence",
    "ProductProvenance",
    "ProductVersion",
    "ProductHistory",
    "LifecycleTransition",
    "LifecycleState",
    "ApprovalRecord",
    # Enums
    "ProductType",
    "ProductStatus",
    "ClassificationLevel",
    "SensitivityLevel",
    "AudienceType",
    "AssertionStatus",
    "AssertionType",
    "CreationMethod",
    # Registries
    "ProductTypeRegistry",
    "ClassificationRegistry",
    "SensitivityRegistry",
    "AudienceRegistry",
    "LifecycleRegistry",
    "VersionRegistry",
    "RelationshipRegistry",
    "AssertionTypeRegistry",
    "EvidenceTypeRegistry",
    # Services
    "ProductService",
    "LifecycleService",
    # Validation
    "ProductValidator",
    "StructureValidator",
    "LifecycleValidator",
    "ReferenceValidator",
    "VersionValidator",
    "RegistryValidator",
    "ValidationResult",
    # Events
    "ProductEventEmitter",
    "ProductEventType",
    # Queries
    "ProductQueryService",
]
