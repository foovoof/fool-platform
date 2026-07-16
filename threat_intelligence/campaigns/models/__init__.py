"""
threat_intelligence/campaigns/models/__init__.py

Campaign Models.
"""
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

from threat_intelligence.campaigns.models.base import (
    CampaignBase,
    Auditable,
    Explainable,
    Versionable,
    ConfidenceMixin,
)

from threat_intelligence.campaigns.models.campaign import (
    Campaign,
    CampaignAlias,
    CampaignMetadata,
)

from threat_intelligence.campaigns.models.timeline import (
    TimelineEvent,
    Milestone,
    ObservedActivity,
    ActivityWindow,
    CampaignTimeline,
)

from threat_intelligence.campaigns.models.assertion import (
    CampaignAssertion,
    AssertionRevision,
)

from threat_intelligence.campaigns.models.evidence import (
    CampaignEvidence,
    EvidenceLink,
)

from threat_intelligence.campaigns.models.relationships import (
    CampaignRelationship,
    CampaignRelationshipType,
)

from threat_intelligence.campaigns.models.lifecycle import (
    LifecycleTransition,
    LifecycleState,
    CampaignLifecycle,
)

from threat_intelligence.campaigns.models.governance import (
    Approval,
    Review,
    AuditEntry,
    AuditTrail,
)

from threat_intelligence.campaigns.models.versioning import (
    CampaignVersion,
    CampaignHistory,
    RollbackMetadata,
)

__all__ = [
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
    # Base
    "CampaignBase",
    "Auditable",
    "Explainable",
    "Versionable",
    "ConfidenceMixin",
    # Campaign
    "Campaign",
    "CampaignAlias",
    "CampaignMetadata",
    # Timeline
    "TimelineEvent",
    "Milestone",
    "ObservedActivity",
    "ActivityWindow",
    "CampaignTimeline",
    # Assertion
    "CampaignAssertion",
    "AssertionRevision",
    # Evidence
    "CampaignEvidence",
    "EvidenceLink",
    # Relationships
    "CampaignRelationship",
    "CampaignRelationshipType",
    # Lifecycle
    "LifecycleTransition",
    "LifecycleState",
    "CampaignLifecycle",
    # Governance
    "Approval",
    "Review",
    "AuditEntry",
    "AuditTrail",
    # Versioning
    "CampaignVersion",
    "CampaignHistory",
    "RollbackMetadata",
]
