from __future__ import annotations

"""
knowledge/services/entity_resolution_service.py

Entity Resolution Service for the Knowledge Layer.

Orchestrates entity resolution operations.
"""
from typing import Any

from knowledge.graph.models import Graph
from knowledge.graph.repository import EntityRepository
from knowledge.resolution import (
    EntityResolutionEngine,
    EntityMatch,
    DeduplicationEngine,
    DuplicateGroup,
)
from knowledge.events import KnowledgeEventEmitter


class EntityResolutionService:
    """
    Service for entity resolution.
    
    Orchestrates:
    - Entity matching
    - Deduplication
    - Event emission
    """

    def __init__(
        self,
        entity_repository: EntityRepository | None = None,
        resolution_engine: EntityResolutionEngine | None = None,
        event_emitter: KnowledgeEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            entity_repository: Optional entity repository
            resolution_engine: Optional resolution engine
            event_emitter: Optional event emitter
        """
        self._repository = entity_repository or EntityRepository()
        self._engine = resolution_engine or EntityResolutionEngine()
        self._deduplication_engine = DeduplicationEngine(entity_engine=self._engine)
        self._event_emitter = event_emitter or KnowledgeEventEmitter()

    def match_entities(
        self,
        source: dict[str, Any],
        target: dict[str, Any],
        match_mode: str = "strict",
    ) -> EntityMatch:
        """
        Match two entities.
        
        Args:
            source: Source entity
            target: Target entity
            match_mode: Matching mode
            
        Returns:
            EntityMatch result
        """
        result = self._engine.match(source, target, match_mode)
        
        if result.is_match:
            self._event_emitter.emit_entity_resolved(
                result.source_entity_id,
                result.target_entity_id,
                result.match_type.value,
                result.confidence,
            )
        
        return result

    def find_duplicates(
        self,
        entities: list[dict[str, Any]],
        match_mode: str = "strict",
    ) -> list[EntityMatch]:
        """
        Find duplicate entities.
        
        Args:
            entities: List of entities to check
            match_mode: Matching mode
            
        Returns:
            List of duplicate matches
        """
        return self._engine.find_duplicates(entities, match_mode)

    def deduplicate(
        self,
        entities: list[dict[str, Any]],
        strategy: str = "keep_first",
    ) -> list[DuplicateGroup]:
        """
        Deduplicate entities.
        
        Args:
            entities: List of entities
            strategy: Merge strategy
            
        Returns:
            List of duplicate groups
        """
        groups = self._deduplication_engine.find_duplicates(entities)
        
        for group in groups:
            if group.entity_ids:
                self._event_emitter.emit_identity_merged(
                    identity_ref="",
                    merged_node_ids=group.entity_ids,
                )
        
        return groups

    def get_entity(self, entity_id: str) -> Any | None:
        """Get an entity by ID."""
        node = self._repository.get_by_id(entity_id)
        if node:
            return {
                "id": node.node_id,
                "type": node.node_type.value,
                "identifiers": node.identity_refs,
                "attributes": node.attributes,
            }
        return None
