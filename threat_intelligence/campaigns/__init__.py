"""
threat_intelligence/campaigns/__init__.py

Campaign Intelligence Module.

Phase 6E.4 - Campaign Intelligence Foundation.

Campaign is a governed intelligence entity.
Campaign is NOT an analytical conclusion.
"""
from threat_intelligence.campaigns.models import (
    Campaign,
    CampaignAlias,
    CampaignMetadata,
    TimelineEvent,
    Milestone,
    ObservedActivity,
    ActivityWindow,
    CampaignTimeline,
    CampaignAssertion,
    AssertionRevision,
    CampaignEvidence,
    EvidenceLink,
    CampaignRelationship,
    CampaignRelationshipType,
    CampaignLifecycle,
    Approval,
    Review,
    AuditEntry,
    AuditTrail,
    CampaignVersion,
    CampaignHistory,
    RollbackMetadata,
)

from threat_intelligence.campaigns.models.enums import (
    CampaignStatus,
    CampaignSeverity,
    CampaignConfidenceLevel,
    AssertionStatus,
    AssertionType,
    ObjectiveStatus,
    MotivationType,
    VictimType,
    TargetingType,
    LifecycleTransition,
    GovernanceAction,
)

from threat_intelligence.campaigns.services import (
    CampaignService,
    AssertionService,
    TimelineService,
    EvidenceService,
    RelationshipService,
    LifecycleService,
    GovernanceService,
    VersionService,
)

from threat_intelligence.campaigns.repositories import (
    CampaignRepository,
    TimelineEventRepository,
    CampaignAssertionRepository,
    CampaignEvidenceRepository,
    CampaignRelationshipRepository,
)

from threat_intelligence.campaigns.events import (
    CampaignEventEmitter,
    CampaignEventType,
)

from threat_intelligence.campaigns.validation import (
    CampaignValidator,
    ValidationResult,
)

from threat_intelligence.campaigns.queries import CampaignQueryService

from threat_intelligence.campaigns.registry import CampaignRegistry

__all__ = [
    # Models
    "Campaign",
    "CampaignAlias",
    "CampaignMetadata",
    "TimelineEvent",
    "Milestone",
    "ObservedActivity",
    "ActivityWindow",
    "CampaignTimeline",
    "CampaignAssertion",
    "AssertionRevision",
    "CampaignEvidence",
    "EvidenceLink",
    "CampaignRelationship",
    "CampaignRelationshipType",
    "CampaignLifecycle",
    "Approval",
    "Review",
    "AuditEntry",
    "AuditTrail",
    "CampaignVersion",
    "CampaignHistory",
    "RollbackMetadata",
    # Enums
    "CampaignStatus",
    "CampaignSeverity",
    "CampaignConfidenceLevel",
    "AssertionStatus",
    "AssertionType",
    "ObjectiveStatus",
    "MotivationType",
    "VictimType",
    "TargetingType",
    "LifecycleTransition",
    "GovernanceAction",
    # Services
    "CampaignService",
    "AssertionService",
    "TimelineService",
    "EvidenceService",
    "RelationshipService",
    "LifecycleService",
    "GovernanceService",
    "VersionService",
    # Repositories
    "CampaignRepository",
    "TimelineEventRepository",
    "CampaignAssertionRepository",
    "CampaignEvidenceRepository",
    "CampaignRelationshipRepository",
    # Events
    "CampaignEventEmitter",
    "CampaignEventType",
    # Validation
    "CampaignValidator",
    "ValidationResult",
    # Queries
    "CampaignQueryService",
    # Registry
    "CampaignRegistry",
]
