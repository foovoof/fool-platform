"""
threat_intelligence/products/models/enums.py

Intelligence Products Enums.
"""
from __future__ import annotations

from enum import Enum


class ProductType(Enum):
    """Intelligence product type."""
    THREAT_REPORT = "threat_report"
    TECHNICAL_REPORT = "technical_report"
    STRATEGIC_REPORT = "strategic_report"
    OPERATIONAL_REPORT = "operational_report"
    TACTICAL_REPORT = "tactical_report"
    EXECUTIVE_SUMMARY = "executive_summary"
    INDICATOR_LIST = "indicator_list"
    IOC_BULLETIN = "ioc_bulletin"
    TTP_ANALYSIS = "ttp_analysis"
    CAMPAIGN_REPORT = "campaign_report"
    THREAT_ACTOR_PROFILE = "threat_actor_profile"
    MALWARE_ANALYSIS = "malware_analysis"
    VULNERABILITY_ADVISORY = "vulnerability_advisory"
    INFRASTRUCTURE_REPORT = "infrastructure_report"


class ProductStatus(Enum):
    """Product status."""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    VALIDATED = "validated"
    APPROVED = "approved"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class ClassificationLevel(Enum):
    """Classification level."""
    UNCLASSIFIED = "unclassified"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class SensitivityLevel(Enum):
    """Sensitivity level."""
    PUBLIC = "public"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    SENSITIVE = "sensitive"
    PERSONAL = "personal"


class AudienceType(Enum):
    """Target audience type."""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    TACTICAL = "tactical"
    GENERAL = "general"
    SPECIALIZED = "specialized"


class AssertionStatus(Enum):
    """Assertion status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"
    REFUTED = "refuted"
    UNVERIFIED = "unverified"


class AssertionType(Enum):
    """Assertion type."""
    FINDING = "finding"
    ASSESSMENT = "assessment"
    RECOMMENDATION = "recommendation"
    OBSERVATION = "observation"
    CONCLUSION = "conclusion"


class CreationMethod(Enum):
    """Product creation method."""
    MANUAL = "manual"
    AUTOMATED = "automated"
    HYBRID = "hybrid"
    AI_ASSISTED = "ai_assisted"
