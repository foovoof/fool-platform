from __future__ import annotations

"""
knowledge/resolution/deduplication.py

Deduplication engine for finding and grouping duplicate entities.

Provides deterministic deduplication based on:
- Identifier matching
- Attribute matching
- Ontology-defined matching criteria
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.resolution.entity_resolution import (
    EntityResolutionEngine,
    EntityMatch,
    EntityMatchType,
)
from knowledge.resolution.identity_resolution import (
    IdentityResolutionEngine,
    IdentityMatch,
)


@dataclass
class DuplicateCandidate:
    """A candidate for deduplication."""
    entity_id: str
    identifiers: list[str]
    attributes: dict[str, Any]
    match_score: float = 0.0
    matched_with: str | None = None


@dataclass
class DuplicateGroup:
    """A group of duplicate entities."""
    group_id: str
    entity_ids: list[str]
    primary_entity_id: str | None = None
    match_type: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_entity(self, entity_id: str) -> None:
        """Add an entity to the group."""
        if entity_id not in self.entity_ids:
            self.entity_ids.append(entity_id)

    def get_size(self) -> int:
        """Get the number of entities in the group."""
        return len(self.entity_ids)


class DeduplicationEngine:
    """
    Deterministic deduplication engine.
    
    Uses resolution engines to find and group duplicates.
    """

    def __init__(
        self,
        entity_engine: EntityResolutionEngine | None = None,
        identity_engine: IdentityResolutionEngine | None = None,
    ) -> None:
        """
        Initialize the deduplication engine.
        
        Args:
            entity_engine: Optional entity resolution engine
            identity_engine: Optional identity resolution engine
        """
        self._entity_engine = entity_engine or EntityResolutionEngine()
        self._identity_engine = identity_engine or IdentityResolutionEngine()

    def find_duplicates_by_identity(
        self,
        entities: list[dict[str, Any]],
    ) -> list[DuplicateGroup]:
        """
        Find duplicate entities by identity.
        
        Args:
            entities: List of entities with identifiers
            
        Returns:
            List of duplicate groups
        """
        groups: list[DuplicateGroup] = []
        assigned: set[str] = set()

        for i, entity in enumerate(entities):
            entity_id = entity.get("id", f"entity_{i}")
            
            if entity_id in assigned:
                continue

            group = DuplicateGroup(
                group_id=f"group_{len(groups)}",
                entity_ids=[entity_id],
                match_type="identity",
            )
            group.add_entity(entity_id)
            assigned.add(entity_id)

            identifiers = entity.get("identifiers", [])
            
            for j, other in enumerate(entities):
                if i >= j:
                    continue
                
                other_id = other.get("id", f"entity_{j}")
                
                if other_id in assigned:
                    continue
                
                other_identifiers = other.get("identifiers", [])
                
                match = self._identity_engine.match_normalized(
                    ",".join(identifiers),
                    ",".join(other_identifiers),
                )
                
                if match.is_match:
                    group.add_entity(other_id)
                    assigned.add(other_id)

            if group.get_size() > 1:
                groups.append(group)

        return groups

    def find_duplicates_by_attributes(
        self,
        entities: list[dict[str, Any]],
        required_attributes: list[str],
    ) -> list[DuplicateGroup]:
        """
        Find duplicate entities by required attributes.
        
        Args:
            entities: List of entities with attributes
            required_attributes: List of attribute keys that must match
            
        Returns:
            List of duplicate groups
        """
        groups: list[DuplicateGroup] = []
        assigned: set[str] = set()

        for i, entity in enumerate(entities):
            entity_id = entity.get("id", f"entity_{i}")
            
            if entity_id in assigned:
                continue

            group = DuplicateGroup(
                group_id=f"group_{len(groups)}",
                entity_ids=[entity_id],
                match_type="attributes",
            )
            group.add_entity(entity_id)
            assigned.add(entity_id)

            source_attrs = entity.get("attributes", {})
            
            for j, other in enumerate(entities):
                if i >= j:
                    continue
                
                other_id = other.get("id", f"entity_{j}")
                
                if other_id in assigned:
                    continue
                
                target_attrs = other.get("attributes", {})
                
                match = self._entity_engine.match_attributes(
                    source_attrs,
                    target_attrs,
                    required_keys=required_attributes,
                )
                
                if match.is_match:
                    group.add_entity(other_id)
                    assigned.add(other_id)

            if group.get_size() > 1:
                groups.append(group)

        return groups

    def find_duplicates(
        self,
        entities: list[dict[str, Any]],
        match_mode: str = "strict",
    ) -> list[DuplicateGroup]:
        """
        Find duplicate entities.
        
        Args:
            entities: List of entities to check
            match_mode: Matching mode for entity resolution
            
        Returns:
            List of duplicate groups
        """
        groups: list[DuplicateGroup] = []
        assigned: set[str] = set()

        for i, entity in enumerate(entities):
            entity_id = entity.get("id", f"entity_{i}")
            
            if entity_id in assigned:
                continue

            group = DuplicateGroup(
                group_id=f"group_{len(groups)}",
                entity_ids=[entity_id],
                match_type=match_mode,
            )
            group.add_entity(entity_id)
            assigned.add(entity_id)

            for j, other in enumerate(entities):
                if i >= j:
                    continue
                
                other_id = other.get("id", f"entity_{j}")
                
                if other_id in assigned:
                    continue
                
                match = self._entity_engine.match(entity, other, match_mode)
                
                if match.is_match:
                    group.add_entity(other_id)
                    assigned.add(other_id)

            if group.get_size() > 1:
                groups.append(group)

        return groups

    def merge_duplicates(
        self,
        group: DuplicateGroup,
        strategy: str = "keep_first",
    ) -> dict[str, Any]:
        """
        Merge duplicate entities in a group.
        
        Args:
            group: The duplicate group
            strategy: Merge strategy
            
        Returns:
            Merged entity
        """
        if not group.entity_ids:
            return {}
        
        if strategy == "keep_first":
            return {"id": group.entity_ids[0]}
        
        if strategy == "keep_last":
            return {"id": group.entity_ids[-1]}
        
        if strategy == "keep_min":
            return {"id": min(group.entity_ids)}
        
        if strategy == "keep_max":
            return {"id": max(group.entity_ids)}
        
        return {"ids": group.entity_ids}
