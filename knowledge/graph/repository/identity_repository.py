from __future__ import annotations

"""
knowledge/graph/repository/identity_repository.py

Identity repository implementation.

In-memory storage for identity resolution.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class IdentityRecord:
    """Record of an identity in the system."""
    identity_id: str = field(default_factory=lambda: str(uuid4()))
    identity_type: str = ""
    raw_value: str = ""
    normalized_value: str = ""
    entity_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    resolved: bool = False
    resolved_at: str | None = None


class IdentityRepository:
    """
    In-memory repository for identity records.
    
    Provides storage and retrieval of identity information.
    """

    def __init__(self) -> None:
        """Initialize the repository."""
        self._identities: dict[str, IdentityRecord] = {}
        self._value_index: dict[str, list[str]] = {}
        self._entity_ref_index: dict[str, list[str]] = {}

    def create(self, identity: IdentityRecord) -> IdentityRecord:
        """
        Create a new identity record.
        
        Args:
            identity: The identity to create
            
        Returns:
            The created identity
        """
        if identity.identity_id in self._identities:
            raise ValueError(f"Identity {identity.identity_id} already exists")
        
        self._identities[identity.identity_id] = identity
        
        # Update value index
        if identity.normalized_value:
            if identity.normalized_value not in self._value_index:
                self._value_index[identity.normalized_value] = []
            self._value_index[identity.normalized_value].append(identity.identity_id)
        
        return identity

    def update(self, identity: IdentityRecord) -> IdentityRecord:
        """
        Update an existing identity.
        
        Args:
            identity: The identity to update
            
        Returns:
            The updated identity
        """
        if identity.identity_id not in self._identities:
            raise ValueError(f"Identity {identity.identity_id} not found")
        self._identities[identity.identity_id] = identity
        return identity

    def delete(self, identity_id: str) -> bool:
        """
        Delete an identity by ID.
        
        Args:
            identity_id: The ID of the identity to delete
            
        Returns:
            True if deleted
        """
        if identity_id not in self._identities:
            return False
        
        identity = self._identities[identity_id]
        
        # Remove from value index
        if identity.normalized_value in self._value_index:
            self._value_index[identity.normalized_value] = [
                i for i in self._value_index[identity.normalized_value]
                if i != identity_id
            ]
        
        # Remove from entity ref index
        for entity_ref in identity.entity_refs:
            if entity_ref in self._entity_ref_index:
                self._entity_ref_index[entity_ref] = [
                    i for i in self._entity_ref_index[entity_ref]
                    if i != identity_id
                ]
        
        del self._identities[identity_id]
        return True

    def get_by_id(self, identity_id: str) -> IdentityRecord | None:
        """Get an identity by ID."""
        return self._identities.get(identity_id)

    def get_by_value(self, normalized_value: str) -> list[IdentityRecord]:
        """
        Get identities by normalized value.
        
        Args:
            normalized_value: The normalized value to search for
            
        Returns:
            List of matching identities
        """
        identity_ids = self._value_index.get(normalized_value, [])
        return [
            self._identities[iid]
            for iid in identity_ids
            if iid in self._identities
        ]

    def get_by_entity_ref(self, entity_ref: str) -> list[IdentityRecord]:
        """
        Get identities linked to an entity.
        
        Args:
            entity_ref: The entity reference to search for
            
        Returns:
            List of matching identities
        """
        identity_ids = self._entity_ref_index.get(entity_ref, [])
        return [
            self._identities[iid]
            for iid in identity_ids
            if iid in self._identities
        ]

    def link_to_entity(self, identity_id: str, entity_ref: str) -> bool:
        """
        Link an identity to an entity.
        
        Args:
            identity_id: The identity ID
            entity_ref: The entity reference to link
            
        Returns:
            True if linked
        """
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        if entity_ref not in identity.entity_refs:
            identity.entity_refs.append(entity_ref)
        
        if entity_ref not in self._entity_ref_index:
            self._entity_ref_index[entity_ref] = []
        if identity_id not in self._entity_ref_index[entity_ref]:
            self._entity_ref_index[entity_ref].append(identity_id)
        
        return True

    def unlink_from_entity(self, identity_id: str, entity_ref: str) -> bool:
        """
        Unlink an identity from an entity.
        
        Args:
            identity_id: The identity ID
            entity_ref: The entity reference to unlink
            
        Returns:
            True if unlinked
        """
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        if entity_ref in identity.entity_refs:
            identity.entity_refs.remove(entity_ref)
        
        if entity_ref in self._entity_ref_index:
            self._entity_ref_index[entity_ref] = [
                i for i in self._entity_ref_index[entity_ref]
                if i != identity_id
            ]
        
        return True

    def mark_resolved(self, identity_id: str) -> bool:
        """
        Mark an identity as resolved.
        
        Args:
            identity_id: The identity ID
            
        Returns:
            True if marked
        """
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        identity.resolved = True
        identity.resolved_at = datetime.now(timezone.utc).isoformat()
        return True

    def list(self, **kwargs: Any) -> list[IdentityRecord]:
        """
        List identities with optional filtering.
        
        Args:
            **kwargs: Optional filters:
                - resolved: Filter by resolved status
                - identity_type: Filter by type
                
        Returns:
            List of matching identities
        """
        results = list(self._identities.values())
        
        resolved = kwargs.get("resolved")
        if resolved is not None:
            results = [i for i in results if i.resolved == resolved]
        
        identity_type = kwargs.get("identity_type")
        if identity_type:
            results = [
                i for i in results if i.identity_type == identity_type
            ]
        
        return results

    def exists(self, identity_id: str) -> bool:
        """Check if an identity exists."""
        return identity_id in self._identities

    def count(self, **kwargs: Any) -> int:
        """Count identities matching criteria."""
        return len(self.list(**kwargs))

    def clear(self) -> None:
        """Clear all identities."""
        self._identities.clear()
        self._value_index.clear()
        self._entity_ref_index.clear()
