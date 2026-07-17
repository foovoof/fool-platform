"""
threat_hunting/models/enums.py

Threat Hunting Enums.
"""
from __future__ import annotations

from enum import Enum


class HuntStatus(Enum):
    """Hunt status."""
    DRAFT = "draft"
    PLANNED = "planned"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class SessionStatus(Enum):
    """Hunt session status."""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class HypothesisStatus(Enum):
    """Hypothesis status."""
    DRAFT = "draft"
    APPROVED = "approved"
    RUNNING = "running"
    VALIDATED = "validated"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class FindingSeverity(Enum):
    """Finding severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"
    NONE = "none"


class RecommendationType(Enum):
    """Recommendation type."""
    REVIEW_INDICATOR = "review_indicator"
    REVIEW_CAMPAIGN = "review_campaign"
    REVIEW_THREAT_ACTOR = "review_threat_actor"
    REVIEW_MALWARE = "review_malware"
    REVIEW_INFRASTRUCTURE = "review_infrastructure"
    REVIEW_VULNERABILITY = "review_vulnerability"
    REVIEW_EVIDENCE = "review_evidence"
    REVIEW_RELATIONSHIP = "review_relationship"
    COLLECT_ADDITIONAL_DATA = "collect_additional_data"
    UPDATE_INTELLIGENCE = "update_intelligence"


class EvidenceType(Enum):
    """Evidence type."""
    OBSERVATION = "observation"
    INDICATOR = "indicator"
    RELATIONSHIP = "relationship"
    CAMPAIGN = "campaign"
    THREAT_ACTOR = "threat_actor"
    MALWARE = "malware"
    INFRASTRUCTURE = "infrastructure"
    VULNERABILITY = "vulnerability"
    EXTERNAL_REFERENCE = "external_reference"


class ConfidenceLevel(Enum):
    """Confidence level."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"
