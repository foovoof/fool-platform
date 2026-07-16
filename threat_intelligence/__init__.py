"""
threat_intelligence/__init__.py

FOOL Platform Threat Intelligence Core.

IMPORTANT: This is the CTI Core only.
No external integrations.
No applications.
No AI.

This module provides:
- Canonical threat intelligence models
- Intelligence services
- Repository abstraction
- Lifecycle management
- Confidence framework
- Evidence management
- Reporting
- Query capabilities
- Versioning

NOT included:
- STIX/TAXII
- MISP
- External feeds
- Threat Hunting
- Incident Response
- Digital Forensics
- AI/LLM
- Sigma execution
- YARA execution
- SOAR
- SIEM integrations

Architecture:
    Threat Models → Services → Repositories
                    ↓
              Lifecycle Manager
                    ↓
              Confidence Framework
                    ↓
              Evidence Management
                    ↓
              Query & Reporting
                    ↓
              Versioning & Audit
"""

from threat_intelligence.models import (
    ThreatEntityType,
    IndicatorType,
    ThreatActorType,
    MalwareType,
    ConfidenceLevel,
    ThreatLevel,
    ReportType,
    ReportStatus,
    Indicator,
    ThreatActor,
    Campaign,
    Malware,
    Tool,
    Infrastructure,
    Vulnerability,
    Relationship,
    RelationshipType,
    EvidenceReference,
    EvidenceBundle,
    EvidenceTimeline,
    EvidenceLineage,
    IntelligenceFinding,
    Sighting,
    Observation,
    ThreatReport,
    ExecutiveReport,
    TechnicalReport,
    ThreatPackage,
    ThreatCollection,
)

from threat_intelligence.repository import (
    RepositoryBase,
    InMemoryRepository,
    IndicatorRepository,
    ThreatActorRepository,
    CampaignRepository,
    MalwareRepository,
    InfrastructureRepository,
    VulnerabilityRepository,
    ToolRepository,
    RelationshipRepository,
    EvidenceRepository,
    FindingRepository,
    ReportRepository,
    PackageRepository,
)

from threat_intelligence.registry import ThreatIntelligenceRegistry

from threat_intelligence.services import (
    IndicatorService,
    ThreatActorService,
    MalwareService,
    RelationshipService,
)

from threat_intelligence.events import (
    ThreatIntelligenceEvent,
    ThreatIntelligenceEventType,
    ThreatIntelligenceEventEmitter,
)

from threat_intelligence.validation import (
    ValidationResult,
    ValidationIssue,
    ValidationService,
    IndicatorValidator,
    ThreatActorValidator,
    RelationshipValidator,
)

from threat_intelligence.query import QueryService

from threat_intelligence.versioning import (
    Version,
    VersionHistory,
    VersioningService,
)

from threat_intelligence.confidence import (
    ConfidenceAssessment,
    SourceAssessment,
    ReliabilityAssessment,
    ConfidenceService,
)

from threat_intelligence.lifecycle import (
    LifecycleState,
    LifecycleTransition,
    LifecycleService,
    IndicatorLifecycle,
    CampaignLifecycle,
    ReportLifecycle,
    FindingLifecycle,
)

from threat_intelligence.reporting import (
    ReportBuilder,
    ReportValidator,
    ReportExporter,
)

from threat_intelligence.evidence import (
    EvidenceValidator,
    EvidenceChainBuilder,
    EvidenceTimelineBuilder,
    EvidenceLineageBuilder,
    EvidenceExplanation,
)

from threat_intelligence.attribution import (
    AttributionEvidence,
    AttributionIndicator,
    AttributionRelationship,
    AttributionConfidence,
    AttributionSupport,
    AttributionBuilder,
)

__all__ = [
    # Enums
    "ThreatEntityType",
    "IndicatorType",
    "ThreatActorType",
    "MalwareType",
    "ConfidenceLevel",
    "ThreatLevel",
    "ReportType",
    "ReportStatus",
    # Models
    "Indicator",
    "ThreatActor",
    "Campaign",
    "Malware",
    "Tool",
    "Infrastructure",
    "Vulnerability",
    "Relationship",
    "RelationshipType",
    "EvidenceReference",
    "EvidenceBundle",
    "EvidenceTimeline",
    "EvidenceLineage",
    "IntelligenceFinding",
    "Sighting",
    "Observation",
    "ThreatReport",
    "ExecutiveReport",
    "TechnicalReport",
    "ThreatPackage",
    "ThreatCollection",
    # Repository
    "RepositoryBase",
    "InMemoryRepository",
    "IndicatorRepository",
    "ThreatActorRepository",
    "CampaignRepository",
    "MalwareRepository",
    "InfrastructureRepository",
    "VulnerabilityRepository",
    "ToolRepository",
    "RelationshipRepository",
    "EvidenceRepository",
    "FindingRepository",
    "ReportRepository",
    "PackageRepository",
    # Registry
    "ThreatIntelligenceRegistry",
    # Services
    "IndicatorService",
    "ThreatActorService",
    "MalwareService",
    "RelationshipService",
    # Events
    "ThreatIntelligenceEvent",
    "ThreatIntelligenceEventType",
    "ThreatIntelligenceEventEmitter",
    # Validation
    "ValidationResult",
    "ValidationIssue",
    "ValidationService",
    "IndicatorValidator",
    "ThreatActorValidator",
    "RelationshipValidator",
    # Query
    "QueryService",
    # Versioning
    "Version",
    "VersionHistory",
    "VersioningService",
    # Confidence
    "ConfidenceAssessment",
    "SourceAssessment",
    "ReliabilityAssessment",
    "ConfidenceService",
    # Lifecycle
    "LifecycleState",
    "LifecycleTransition",
    "LifecycleService",
    "IndicatorLifecycle",
    "CampaignLifecycle",
    "ReportLifecycle",
    "FindingLifecycle",
    # Reporting
    "ReportBuilder",
    "ReportValidator",
    "ReportExporter",
    # Evidence
    "EvidenceValidator",
    "EvidenceChainBuilder",
    "EvidenceTimelineBuilder",
    "EvidenceLineageBuilder",
    "EvidenceExplanation",
    # Attribution
    "AttributionEvidence",
    "AttributionIndicator",
    "AttributionRelationship",
    "AttributionConfidence",
    "AttributionSupport",
    "AttributionBuilder",
]
