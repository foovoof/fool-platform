from __future__ import annotations

"""
knowledge/resolution/relationship_resolution.py

Relationship resolution engine for deterministic relationship matching.

Provides deterministic matching based on:
- Source-target pair matching
- Relationship type matching
- Contract-defined relationship keys
- Ontology-defined relationship rules
"""
from dataclasses import dataclass, field
from enum import Enum

from knowledge.graph.models import RelationshipType


class RelationshipMatchType(Enum):
    """Types of relationship matches."""
    EXACT = "exact"
    SYMMETRIC = "symmetric"
    TYPE_MATCH = "type_match"
    NO_MATCH = "no_match"


@dataclass
class RelationshipMatch:
    """Result of relationship matching."""
    source_entity_ref: str
    target_entity_ref: str
    relationship_type: str
    is_match: bool
    match_type: RelationshipMatchType = RelationshipMatchType.NO_MATCH
    confidence: float = 0.0
    match_reason: str = ""


class RelationshipResolutionEngine:
    """
    Deterministic relationship resolution engine.
    
    Resolution is based on:
    - Source-target pair matching
    - Relationship type matching
    - Ontology-defined relationship rules
    """

    def __init__(
        self,
        symmetric_relationships: set[str] | None = None,
    ) -> None:
        """
        Initialize the relationship resolution engine.
        
        Args:
            symmetric_relationships: Set of relationship types that are symmetric
        """
        self._symmetric_relationships = symmetric_relationships or {
            "related_to",
            "similar_to",
            "connected_to",
            "associated_with",
        }

    def is_symmetric(self, relationship_type: str) -> bool:
        """Check if a relationship type is symmetric."""
        return relationship_type in self._symmetric_relationships

    def match_exact(
        self,
        source_ref: str,
        target_ref: str,
        rel_type: str,
        other_source: str,
        other_target: str,
        other_type: str,
    ) -> RelationshipMatch:
        """
        Perform exact relationship matching.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            rel_type: Relationship type
            other_source: Other source reference
            other_target: Other target reference
            other_type: Other relationship type
            
        Returns:
            RelationshipMatch result
        """
        if (
            source_ref == other_source
            and target_ref == other_target
            and rel_type == other_type
        ):
            return RelationshipMatch(
                source_entity_ref=source_ref,
                target_entity_ref=target_ref,
                relationship_type=rel_type,
                is_match=True,
                match_type=RelationshipMatchType.EXACT,
                confidence=1.0,
                match_reason="Exact relationship match",
            )

        return RelationshipMatch(
            source_entity_ref=source_ref,
            target_entity_ref=target_ref,
            relationship_type=rel_type,
            is_match=False,
            match_type=RelationshipMatchType.NO_MATCH,
            confidence=0.0,
            match_reason="Relationships do not match exactly",
        )

    def match_symmetric(
        self,
        source_ref: str,
        target_ref: str,
        rel_type: str,
        other_source: str,
        other_target: str,
        other_type: str,
    ) -> RelationshipMatch:
        """
        Perform symmetric relationship matching.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            rel_type: Relationship type
            other_source: Other source reference
            other_target: Other target reference
            other_type: Other relationship type
            
        Returns:
            RelationshipMatch result
        """
        if not self.is_symmetric(rel_type):
            return RelationshipMatch(
                source_entity_ref=source_ref,
                target_entity_ref=target_ref,
                relationship_type=rel_type,
                is_match=False,
                match_type=RelationshipMatchType.NO_MATCH,
                confidence=0.0,
                match_reason=f"Relationship type '{rel_type}' is not symmetric",
            )

        forward_match = (
            source_ref == other_source
            and target_ref == other_target
            and rel_type == other_type
        )
        
        reverse_match = (
            source_ref == other_target
            and target_ref == other_source
            and rel_type == other_type
        )

        is_match = forward_match or reverse_match
        
        return RelationshipMatch(
            source_entity_ref=source_ref,
            target_entity_ref=target_ref,
            relationship_type=rel_type,
            is_match=is_match,
            match_type=RelationshipMatchType.SYMMETRIC if is_match else RelationshipMatchType.NO_MATCH,
            confidence=1.0 if is_match else 0.0,
            match_reason="Symmetric relationship match" if is_match else "Symmetric check failed",
        )

    def match_by_type(
        self,
        source_ref: str,
        target_ref: str,
        rel_type: str,
        other_source: str,
        other_target: str,
        other_type: str,
    ) -> RelationshipMatch:
        """
        Perform relationship matching by type.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            rel_type: Relationship type
            other_source: Other source reference
            other_target: Other target reference
            other_type: Other relationship type
            
        Returns:
            RelationshipMatch result
        """
        type_match = rel_type == other_type
        
        if not type_match:
            return RelationshipMatch(
                source_entity_ref=source_ref,
                target_entity_ref=target_ref,
                relationship_type=rel_type,
                is_match=False,
                match_type=RelationshipMatchType.NO_MATCH,
                confidence=0.0,
                match_reason=f"Relationship type mismatch: {rel_type} != {other_type}",
            )

        pair_match = (
            source_ref == other_source and target_ref == other_target
        )
        
        symmetric_match = (
            source_ref == other_target and target_ref == other_source
        ) if self.is_symmetric(rel_type) else False

        is_match = pair_match or symmetric_match

        return RelationshipMatch(
            source_entity_ref=source_ref,
            target_entity_ref=target_ref,
            relationship_type=rel_type,
            is_match=is_match,
            match_type=RelationshipMatchType.TYPE_MATCH if is_match else RelationshipMatchType.NO_MATCH,
            confidence=1.0 if is_match else 0.0,
            match_reason="Type and pair match" if is_match else "Type matches but pair does not",
        )

    def match(
        self,
        source_ref: str,
        target_ref: str,
        rel_type: str,
        other_source: str,
        other_target: str,
        other_type: str,
        strict: bool = True,
    ) -> RelationshipMatch:
        """
        Perform relationship matching.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            rel_type: Relationship type
            other_source: Other source reference
            other_target: Other target reference
            other_type: Other relationship type
            strict: Whether to use strict matching
            
        Returns:
            RelationshipMatch result
        """
        if strict:
            return self.match_exact(
                source_ref, target_ref, rel_type,
                other_source, other_target, other_type,
            )
        
        return self.match_by_type(
            source_ref, target_ref, rel_type,
            other_source, other_target, other_type,
        )

    def find_duplicates(
        self,
        relationships: list[dict[str, str]],
    ) -> list[RelationshipMatch]:
        """
        Find duplicate relationships in a list.
        
        Args:
            relationships: List of relationships to check
            
        Returns:
            List of RelationshipMatch results for duplicates
        """
        duplicates: list[RelationshipMatch] = []
        checked: set[str] = set()

        for i, source_rel in enumerate(relationships):
            source_key = self._make_relationship_key(
                source_rel.get("source", ""),
                source_rel.get("target", ""),
                source_rel.get("type", ""),
            )
            
            for j, target_rel in enumerate(relationships):
                if i >= j:
                    continue
                
                target_key = self._make_relationship_key(
                    target_rel.get("source", ""),
                    target_rel.get("target", ""),
                    target_rel.get("type", ""),
                )
                
                if target_key in checked:
                    continue
                
                checked.add(source_key)
                
                match_result = self.match(
                    source_rel.get("source", ""),
                    source_rel.get("target", ""),
                    source_rel.get("type", ""),
                    target_rel.get("source", ""),
                    target_rel.get("target", ""),
                    target_rel.get("type", ""),
                    strict=False,
                )
                
                if match_result.is_match:
                    duplicates.append(match_result)

        return duplicates

    def _make_relationship_key(
        self,
        source: str,
        target: str,
        rel_type: str,
    ) -> str:
        """Create a normalized key for a relationship."""
        if self.is_symmetric(rel_type):
            pair = tuple(sorted([source, target]))
            return f"{rel_type}:{pair[0]}:{pair[1]}"
        return f"{rel_type}:{source}:{target}"
