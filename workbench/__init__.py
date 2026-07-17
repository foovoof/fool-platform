"""
workbench/__init__.py

Threat Intelligence Workbench Module.

Phase 8C - Threat Intelligence Workbench Foundation.

IMPORTANT: The Workbench governs intelligence products.
It NEVER owns them.

FUNDAMENTAL PRINCIPLES:
- Platform owns Intelligence Assets
- Workbench governs Intelligence Assets
- Workspaces consume Intelligence Assets

The Workbench SHALL never become another CTI Core.
It orchestrates. It governs. It certifies.
It NEVER owns platform knowledge.

REFERENCE NOT REplica:
Every intelligence asset used inside the Workbench
SHALL be represented by references.
NEVER copies. NEVER duplicated models.
"""
from workbench.models import (
    IntelligenceProduct,
    IntelligenceCollection,
    AssertionReference,
    EvidencePackageReference,
    KnowledgeReference,
    ProductVersion,
    ProductHistory,
    Reviewer,
    ReviewCycle,
    ApprovalRecord,
    ApprovalWorkflow,
    Publication,
    PublicationHistory,
    SourceAssessment,
    ConfidenceReview,
    GovernanceDecision,
    PublicationPolicy,
    WorkbenchSession,
    WorkbenchContext,
    WorkbenchHistory,
)

from workbench.models.enums import (
    ProductLifecycleStatus,
    ReviewStatus,
    ApprovalStatus,
    PublicationStatus,
    CollectionStatus,
    SourceReliability,
    ConfidenceLevel,
)

from workbench.runtime import (
    ProductManager,
    CollectionManager,
    ReviewManager,
    ApprovalManager,
    PublicationManager,
    GovernanceManager,
    SourceAssessmentManager,
    ConfidenceReviewManager,
)

from workbench.events import (
    WorkbenchEventEmitter,
    WorkbenchEventType,
)

__all__ = [
    # Models
    "IntelligenceProduct",
    "IntelligenceCollection",
    "AssertionReference",
    "EvidencePackageReference",
    "KnowledgeReference",
    "ProductVersion",
    "ProductHistory",
    "Reviewer",
    "ReviewCycle",
    "ApprovalRecord",
    "ApprovalWorkflow",
    "Publication",
    "PublicationHistory",
    "SourceAssessment",
    "ConfidenceReview",
    "GovernanceDecision",
    "PublicationPolicy",
    "WorkbenchSession",
    "WorkbenchContext",
    "WorkbenchHistory",
    # Enums
    "ProductLifecycleStatus",
    "ReviewStatus",
    "ApprovalStatus",
    "PublicationStatus",
    "CollectionStatus",
    "SourceReliability",
    "ConfidenceLevel",
    # Runtime
    "ProductManager",
    "CollectionManager",
    "ReviewManager",
    "ApprovalManager",
    "PublicationManager",
    "GovernanceManager",
    "SourceAssessmentManager",
    "ConfidenceReviewManager",
    # Events
    "WorkbenchEventEmitter",
    "WorkbenchEventType",
]
