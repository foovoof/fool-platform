"""
workbench/models/enums.py

Workbench Enums.
"""
from __future__ import annotations

from enum import Enum


class ProductLifecycleStatus(Enum):
    """Product lifecycle status."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class ReviewStatus(Enum):
    """Review status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ApprovalStatus(Enum):
    """Approval status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PublicationStatus(Enum):
    """Publication status."""
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    WITHDRAWN = "withdrawn"


class CollectionStatus(Enum):
    """Collection status."""
    ACTIVE = "active"
    ARCHIVED = "archived"


class SourceReliability(Enum):
    """Source reliability rating."""
    A = "a"  # Fully reliable
    B = "b"  # Usually reliable
    C = "c"  # Fairly reliable
    D = "d"  # Not usually reliable
    E = "e"  # Unreliable
    F = "f"  # Reliability cannot be judged


class ConfidenceLevel(Enum):
    """Confidence level."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"
