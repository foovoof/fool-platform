"""
threat_intelligence/query.py

Query Module.

Provides query capabilities for threat intelligence.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.repository import (
    IndicatorRepository,
    ThreatActorRepository,
    MalwareRepository,
    RelationshipRepository,
)


class QueryService:
    """
    Query service for threat intelligence.
    
    Provides advanced search and traversal capabilities.
    """
    
    def __init__(
        self,
        indicator_repository: IndicatorRepository | None = None,
        actor_repository: ThreatActorRepository | None = None,
        malware_repository: MalwareRepository | None = None,
        relationship_repository: RelationshipRepository | None = None,
    ) -> None:
        self._indicator_repo = indicator_repository or IndicatorRepository()
        self._actor_repo = actor_repository or ThreatActorRepository()
        self._malware_repo = malware_repository or MalwareRepository()
        self._relationship_repo = relationship_repository or RelationshipRepository()
    
    def search_indicators(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Search indicators."""
        indicators = self._indicator_repo.search(query)
        return [ind.to_dict() for ind in indicators]
    
    def search_actors(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Search threat actors."""
        actors = self._actor_repo.search(query)
        return [act.to_dict() for act in actors]
    
    def search_malware(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Search malware."""
        malware = self._malware_repo.search(query)
        return [mal.to_dict() for mal in malware]
    
    def find_relationships(
        self, source_id: str | None = None, target_id: str | None = None
    ) -> list[dict[str, Any]]:
        """Find relationships."""
        query = {}
        if source_id:
            query["source_id"] = source_id
        if target_id:
            query["target_id"] = target_id
        
        relationships = self._relationship_repo.search(query)
        return [rel.to_dict() for rel in relationships]
    
    def traverse_relationships(
        self, entity_id: str, max_depth: int = 2
    ) -> dict[str, Any]:
        """
        Traverse relationships from an entity.
        
        Args:
            entity_id: Starting entity ID
            max_depth: Maximum traversal depth
            
        Returns:
            Traversal result
        """
        visited = set()
        result = {
            "entity_id": entity_id,
            "depth": 0,
            "relationships": [],
            "entities": [],
        }
        
        current_level = [(entity_id, 0)]
        
        while current_level:
            next_level = []
            for current_id, depth in current_level:
                if depth >= max_depth:
                    continue
                if current_id in visited:
                    continue
                visited.add(current_id)
                
                rels = self._relationship_repo.search({"source_id": current_id})
                for rel in rels:
                    result["relationships"].append(rel.to_dict())
                    next_level.append((rel.target_id, depth + 1))
            
            current_level = next_level
        
        return result
    
    def get_related_entities(
        self, entity_id: str, relationship_type: str | None = None
    ) -> dict[str, list[str]]:
        """
        Get entities related to a given entity.
        
        Args:
            entity_id: Entity ID
            relationship_type: Optional relationship type filter
            
        Returns:
            Dictionary of entity types to entity IDs
        """
        query = {"source_id": entity_id}
        if relationship_type:
            query["relationship_type"] = relationship_type
        
        relationships = self._relationship_repo.search(query)
        
        result: dict[str, list[str]] = {}
        for rel in relationships:
            target_type = rel.target_type
            if target_type not in result:
                result[target_type] = []
            result[target_type].append(rel.target_id)
        
        return result
