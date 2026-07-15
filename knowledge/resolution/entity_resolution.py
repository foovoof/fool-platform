from __future__ import annotations

"""
knowledge/resolution/entity_resolution.py

Entity resolution engine for deterministic entity matching.

Provides deterministic matching based on:
- Exact identifier match
- Normalized identifier match
- Exact attribute match
- Case-insensitive attribute match
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re


class EntityMatchType(Enum):
    """Types of entity matches."""
    EXACT = "exact"
    NORMALIZED = "normalized"
    ATTRIBUTE_MATCH = "attribute_match"
    CASE_INSENSITIVE = "case_insensitive"
    NO_MATCH = "no_match"


@dataclass
class MatchExplanation:
    """Explanation of a match decision."""
    match_type: EntityMatchType
    criteria: str
    source_value: str
    target_value: str
    is_match: bool
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class EntityMatch:
    """Result of entity matching."""
    source_entity_id: str
    target_entity_id: str
    match_type: EntityMatchType
    is_match: bool
    confidence: float = 0.0
    explanations: list[MatchExplanation] = field(default_factory=list)

    def add_explanation(self, explanation: MatchExplanation) -> None:
        """Add a match explanation."""
        self.explanations.append(explanation)

    def get_primary_explanation(self) -> MatchExplanation | None:
        """Get the primary explanation (first match explanation)."""
        return self.explanations[0] if self.explanations else None


class EntityResolutionEngine:
    """
    Deterministic entity resolution engine.
    
    Resolution is based on:
    - Exact identifier matching
    - Normalized identifier matching
    - Attribute matching
    - Ontology-defined matching criteria
    """

    def __init__(
        self,
        case_sensitive: bool = True,
        normalize_whitespace: bool = True,
    ) -> None:
        """
        Initialize the entity resolution engine.
        
        Args:
            case_sensitive: Whether matching is case sensitive
            normalize_whitespace: Whether to normalize whitespace
        """
        self._case_sensitive = case_sensitive
        self._normalize_whitespace = normalize_whitespace

    def normalize(self, value: str) -> str:
        """
        Normalize a value for matching.
        
        Args:
            value: The value to normalize
            
        Returns:
            Normalized value
        """
        if not value:
            return ""
        
        result = value
        
        if not self._case_sensitive:
            result = result.lower()
        
        if self._normalize_whitespace:
            result = re.sub(r"\s+", " ", result).strip()
        
        return result

    def match_identifiers(
        self,
        source_ids: list[str],
        target_ids: list[str],
    ) -> EntityMatch:
        """
        Match entities based on identifiers.
        
        Args:
            source_ids: Source entity identifiers
            target_ids: Target entity identifiers
            
        Returns:
            EntityMatch result
        """
        if not source_ids or not target_ids:
            return EntityMatch(
                source_entity_id="",
                target_entity_id="",
                match_type=EntityMatchType.NO_MATCH,
                is_match=False,
            )

        source_id = source_ids[0]
        target_id = target_ids[0]

        for src in source_ids:
            for tgt in target_ids:
                if src == tgt:
                    return EntityMatch(
                        source_entity_id=source_id,
                        target_entity_id=target_id,
                        match_type=EntityMatchType.EXACT,
                        is_match=True,
                        confidence=1.0,
                        explanations=[
                            MatchExplanation(
                                match_type=EntityMatchType.EXACT,
                                criteria="identifier",
                                source_value=src,
                                target_value=tgt,
                                is_match=True,
                            )
                        ],
                    )

        return EntityMatch(
            source_entity_id=source_id,
            target_entity_id=target_id,
            match_type=EntityMatchType.NO_MATCH,
            is_match=False,
        )

    def match_normalized(
        self,
        source_value: str,
        target_value: str,
    ) -> EntityMatch:
        """
        Match entities based on normalized values.
        
        Args:
            source_value: Source value
            target_value: Target value
            
        Returns:
            EntityMatch result
        """
        if not source_value or not target_value:
            return EntityMatch(
                source_entity_id="",
                target_entity_id="",
                match_type=EntityMatchType.NO_MATCH,
                is_match=False,
            )

        source_normalized = self.normalize(source_value)
        target_normalized = self.normalize(target_value)

        is_match = source_normalized == target_normalized
        match_type = EntityMatchType.NORMALIZED if is_match else EntityMatchType.NO_MATCH

        return EntityMatch(
            source_entity_id=source_value,
            target_entity_id=target_value,
            match_type=match_type,
            is_match=is_match,
            confidence=1.0 if is_match else 0.0,
            explanations=[
                MatchExplanation(
                    match_type=match_type,
                    criteria="normalized",
                    source_value=source_normalized,
                    target_value=target_normalized,
                    is_match=is_match,
                    details={"original_source": source_value, "original_target": target_value},
                )
            ],
        )

    def match_attributes(
        self,
        source_attrs: dict[str, Any],
        target_attrs: dict[str, Any],
        required_keys: list[str] | None = None,
    ) -> EntityMatch:
        """
        Match entities based on attributes.
        
        Args:
            source_attrs: Source entity attributes
            target_attrs: Target entity attributes
            required_keys: Keys that must match (optional)
            
        Returns:
            EntityMatch result
        """
        if not source_attrs or not target_attrs:
            return EntityMatch(
                source_entity_id="",
                target_entity_id="",
                match_type=EntityMatchType.NO_MATCH,
                is_match=False,
            )

        explanations: list[MatchExplanation] = []
        match_count = 0
        total_count = 0

        if required_keys:
            total_count = len(required_keys)
            for key in required_keys:
                src_val = source_attrs.get(key)
                tgt_val = target_attrs.get(key)
                
                if src_val == tgt_val:
                    match_count += 1
                    explanations.append(
                        MatchExplanation(
                            match_type=EntityMatchType.EXACT,
                            criteria=f"attribute.{key}",
                            source_value=str(src_val),
                            target_value=str(tgt_val),
                            is_match=True,
                        )
                    )
                else:
                    explanations.append(
                        MatchExplanation(
                            match_type=EntityMatchType.EXACT,
                            criteria=f"attribute.{key}",
                            source_value=str(src_val),
                            target_value=str(tgt_val),
                            is_match=False,
                        )
                    )
        else:
            all_keys = set(source_attrs.keys()) & set(target_attrs.keys())
            total_count = len(all_keys)
            
            for key in all_keys:
                src_val = source_attrs[key]
                tgt_val = target_attrs[key]
                
                if src_val == tgt_val:
                    match_count += 1
                    explanations.append(
                        MatchExplanation(
                            match_type=EntityMatchType.EXACT,
                            criteria=f"attribute.{key}",
                            source_value=str(src_val),
                            target_value=str(tgt_val),
                            is_match=True,
                        )
                    )

        if required_keys and match_count == total_count:
            return EntityMatch(
                source_entity_id="source",
                target_entity_id="target",
                match_type=EntityMatchType.ATTRIBUTE_MATCH,
                is_match=True,
                confidence=1.0,
                explanations=explanations,
            )

        if match_count > 0 and not required_keys:
            confidence = match_count / total_count if total_count > 0 else 0.0
            return EntityMatch(
                source_entity_id="source",
                target_entity_id="target",
                match_type=EntityMatchType.ATTRIBUTE_MATCH,
                is_match=confidence == 1.0,
                confidence=confidence,
                explanations=explanations,
            )

        return EntityMatch(
            source_entity_id="source",
            target_entity_id="target",
            match_type=EntityMatchType.NO_MATCH,
            is_match=False,
            explanations=explanations,
        )

    def match(
        self,
        source_entity: dict[str, Any],
        target_entity: dict[str, Any],
        match_mode: str = "strict",
    ) -> EntityMatch:
        """
        Perform entity matching.
        
        Args:
            source_entity: Source entity with identifiers and attributes
            target_entity: Target entity with identifiers and attributes
            match_mode: Matching mode ("strict", "loose", "attributes_only")
            
        Returns:
            EntityMatch result
        """
        if match_mode == "strict":
            source_ids = source_entity.get("identifiers", [])
            target_ids = target_entity.get("identifiers", [])
            
            id_match = self.match_identifiers(source_ids, target_ids)
            if id_match.is_match:
                return id_match
            
            attr_match = self.match_attributes(
                source_entity.get("attributes", {}),
                target_entity.get("attributes", {}),
            )
            return attr_match

        elif match_mode == "attributes_only":
            return self.match_attributes(
                source_entity.get("attributes", {}),
                target_entity.get("attributes", {}),
            )

        else:
            source_name = source_entity.get("name", "")
            target_name = target_entity.get("name", "")
            
            return self.match_normalized(source_name, target_name)

    def find_duplicates(
        self,
        entities: list[dict[str, Any]],
        match_mode: str = "strict",
    ) -> list[EntityMatch]:
        """
        Find duplicate entities in a list.
        
        Args:
            entities: List of entities to check
            match_mode: Matching mode
            
        Returns:
            List of EntityMatch results for duplicates
        """
        duplicates: list[EntityMatch] = []
        checked: set[tuple[str, str]] = set()

        for i, source in enumerate(entities):
            source_id = source.get("id", f"entity_{i}")
            
            for j, target in enumerate(entities):
                if i >= j:
                    continue
                
                target_id = target.get("id", f"entity_{j}")
                pair = tuple(sorted([source_id, target_id]))
                
                if pair in checked:
                    continue
                
                checked.add(pair)
                
                match_result = self.match(source, target, match_mode)
                match_result.source_entity_id = source_id
                match_result.target_entity_id = target_id
                
                if match_result.is_match:
                    duplicates.append(match_result)

        return duplicates

    def resolve(
        self,
        entity: dict[str, Any],
        candidate_pool: list[dict[str, Any]],
        match_mode: str = "strict",
    ) -> EntityMatch | None:
        """
        Resolve an entity against a candidate pool.
        
        Args:
            entity: The entity to resolve
            candidate_pool: List of candidate entities
            match_mode: Matching mode
            
        Returns:
            Best EntityMatch or None
        """
        best_match: EntityMatch | None = None

        for candidate in candidate_pool:
            match_result = self.match(entity, candidate, match_mode)
            
            if match_result.is_match:
                if best_match is None or match_result.confidence > best_match.confidence:
                    best_match = match_result

        return best_match
