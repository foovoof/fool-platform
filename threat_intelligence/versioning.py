"""
threat_intelligence/versioning.py

Versioning Module.

Provides versioning support for threat intelligence entities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Version:
    """Version information."""
    version: int
    created_at: str
    author: str
    reason: str
    changes: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "created_at": self.created_at,
            "author": self.author,
            "reason": self.reason,
            "changes": self.changes,
        }


class VersionHistory:
    """
    Version history for an entity.
    
    Tracks all changes to an entity over time.
    """
    
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        self._versions: list[Version] = []
    
    def add_version(
        self,
        version: int,
        author: str = "",
        reason: str = "",
        changes: dict[str, Any] | None = None,
    ) -> None:
        """Add a version to history."""
        v = Version(
            version=version,
            created_at=datetime.now(timezone.utc).isoformat(),
            author=author,
            reason=reason,
            changes=changes or {},
        )
        self._versions.append(v)
    
    def get_version(self, version: int) -> Version | None:
        """Get a specific version."""
        for v in self._versions:
            if v.version == version:
                return v
        return None
    
    def get_latest_version(self) -> Version | None:
        """Get the latest version."""
        if self._versions:
            return self._versions[-1]
        return None
    
    def get_all_versions(self) -> list[Version]:
        """Get all versions."""
        return list(self._versions)
    
    def get_version_count(self) -> int:
        """Get number of versions."""
        return len(self._versions)


class VersioningService:
    """
    Service for managing entity versions.
    
    Provides versioning capabilities without persistence.
    """
    
    def __init__(self) -> None:
        self._histories: dict[str, VersionHistory] = {}
    
    def get_or_create_history(self, entity_id: str) -> VersionHistory:
        """Get or create version history for an entity."""
        if entity_id not in self._histories:
            self._histories[entity_id] = VersionHistory(entity_id)
        return self._histories[entity_id]
    
    def record_version(
        self,
        entity_id: str,
        version: int,
        author: str = "",
        reason: str = "",
        changes: dict[str, Any] | None = None,
    ) -> None:
        """Record a new version."""
        history = self.get_or_create_history(entity_id)
        history.add_version(version, author, reason, changes)
    
    def get_history(self, entity_id: str) -> VersionHistory | None:
        """Get version history for an entity."""
        return self._histories.get(entity_id)
    
    def get_version_count(self, entity_id: str) -> int:
        """Get version count for an entity."""
        history = self._histories.get(entity_id)
        if history:
            return history.get_version_count()
        return 0
    
    def rollback_info(
        self, entity_id: str, target_version: int
    ) -> dict[str, Any] | None:
        """
        Get rollback metadata for a target version.
        
        Args:
            entity_id: Entity ID
            target_version: Target version number
            
        Returns:
            Rollback metadata or None if not found
        """
        history = self._histories.get(entity_id)
        if not history:
            return None
        
        version = history.get_version(target_version)
        if not version:
            return None
        
        return {
            "entity_id": entity_id,
            "target_version": target_version,
            "rollback_created_at": datetime.now(timezone.utc).isoformat(),
            "rollback_author": version.author,
            "rollback_reason": f"Rollback to version {target_version}",
            "original_version": version.to_dict(),
        }
