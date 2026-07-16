"""
threat_intelligence/campaigns/models/enums.py

Campaign Enums.
"""
from __future__ import annotations

from enum import Enum


class CampaignStatus(Enum):
    """Campaign status."""
    PLANNED = "planned"
    PROPOSED = "proposed"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class CampaignSeverity(Enum):
    """Campaign severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class CampaignConfidenceLevel(Enum):
    """Campaign confidence level."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class AssertionStatus(Enum):
    """Assertion status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"
    REFUTED = "refuted"
    UNVERIFIED = "unverified"


class AssertionType(Enum):
    """Assertion type."""
    OBSERVATION = "observation"
    INFERENCE = "inference"
    ATTRIBUTION = "attribution"
    RELATIONSHIP = "relationship"
    TIMELINE = "timeline"
    CAPABILITY = "capability"
    INTENT = "intent"
    IMPACT = "impact"


class ObjectiveStatus(Enum):
    """Objective status."""
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    PARTIAL = "partial"
    FAILED = "failed"


class MotivationType(Enum):
    """Motivation type."""
    FINANCIAL = "financial"
    ESPIONAGE = "espionage"
    HACKTIVISM = "hacktivism"
    DESTRUCTION = "destruction"
    DISRUPTION = "disruption"
    IDEOLOGICAL = "ideological"
    POLITICAL = "political"
    PERSONAL = "personal"
    UNKNOWN = "unknown"


class VictimType(Enum):
    """Victim type."""
    ORGANIZATION = "organization"
    GOVERNMENT = "government"
    INDIVIDUAL = "individual"
    INFRASTRUCTURE = "infrastructure"
    SECTOR = "sector"


class TargetingType(Enum):
    """Targeting type."""
    SECTOR = "sector"
    GEOGRAPHY = "geography"
    TECHNOLOGY = "technology"
    PERSONNEL = "personnel"
    DATA = "data"
    FINANCIAL = "financial"


class LifecycleTransition(Enum):
    """Lifecycle transition."""
    PROPOSE = "propose"
    APPROVE = "approve"
    ACTIVATE = "activate"
    SUSPEND = "suspend"
    COMPLETE = "complete"
    CANCEL = "cancel"
    ARCHIVE = "archive"
    REACTIVATE = "reactivate"


class GovernanceAction(Enum):
    """Governance action."""
    CREATE = "create"
    UPDATE = "update"
    APPROVE = "approve"
    REJECT = "reject"
    REVIEW = "review"
    PUBLISH = "publish"
    ARCHIVE = "archive"
