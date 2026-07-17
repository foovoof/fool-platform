"""
executive_portal/models/enums.py

Executive Portal Enums.
"""
from __future__ import annotations

from enum import Enum


class WidgetType(Enum):
    """Widget types."""
    METRIC = "metric"
    CHART = "chart"
    TABLE = "table"
    LIST = "list"
    TIMELINE = "timeline"
    MAP = "map"
    ALERT = "alert"
    NEWS = "news"
    FEED = "feed"
    SUMMARY = "summary"
    STATUS = "status"
    INDICATOR = "indicator"
    REPORT = "report"
    PUBLICATION = "publication"
    EVIDENCE = "evidence"
    CUSTOM = "custom"


class DashboardStatus(Enum):
    """Dashboard status."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    SHARED = "shared"


class BriefingStatus(Enum):
    """Briefing status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    IDLE = "idle"
    ENDED = "ended"


class AuditAction(Enum):
    """Audit action types."""
    VIEWED = "viewed"
    OPENED = "opened"
    PINNED = "pinned"
    BOOKMARKED = "bookmarked"
    EXPORTED = "exported"
    SHARED = "shared"
    LAYOUT_CHANGED = "layout_changed"
    FILTER_APPLIED = "filter_applied"
    SEARCH_EXECUTED = "search_executed"
