"""
analyst_workspace/models/enums.py

Workspace Enums.
"""
from __future__ import annotations

from enum import Enum


class WorkspaceStatus(Enum):
    """Workspace status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    IDLE = "idle"
    SAVING = "saving"
    RESTORING = "restoring"
    CLOSED = "closed"


class ViewType(Enum):
    """View types."""
    KNOWLEDGE = "knowledge"
    ENTITY = "entity"
    RELATIONSHIP = "relationship"
    EVIDENCE = "evidence"
    REPORT = "report"
    INVESTIGATION = "investigation"
    SEARCH = "search"
    TIMELINE = "timeline"
    GRAPH = "graph"
    ANALYTICS = "analytics"
    CUSTOM = "custom"


class PanelType(Enum):
    """Panel types."""
    ENTITY_DETAILS = "entity_details"
    RELATIONSHIP_DETAILS = "relationship_details"
    EVIDENCE_PANEL = "evidence_panel"
    PROPERTIES = "properties"
    METADATA = "metadata"
    HISTORY = "history"
    AUDIT_TRAIL = "audit_trail"
    CONFIDENCE = "confidence"
    ASSERTIONS = "assertions"
    REFERENCES = "references"
    NOTES = "notes"
    CUSTOM = "custom"


class CommandScope(Enum):
    """Command scope."""
    WORKSPACE = "workspace"
    SESSION = "session"
    VIEW = "view"
    PANEL = "panel"
    NAVIGATION = "navigation"
    SELECTION = "selection"
    GLOBAL = "global"


class NotificationLevel(Enum):
    """Notification level."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class Theme(Enum):
    """Theme options."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class Language(Enum):
    """Language options."""
    ENGLISH = "en"
    ARABIC = "ar"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    RUSSIAN = "ru"


class TimeFormat(Enum):
    """Time format options."""
    ISO8601 = "iso8601"
    LOCAL = "local"
    UTC = "utc"
    HUMAN = "human"
