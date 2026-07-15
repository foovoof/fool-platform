"""
knowledge/graph/repository/entity_repository.py

Entity repository implementation.

In-memory storage for knowledge entities.
"""
from __future__ import annotations

from typing import Any

from knowledge.graph.models import Node, NodeType
from knowledge.graph.repository.base import KnowledgeRepository


class EntityRepository(KnowledgeRepository[Node]):
    """
    In-memory repository for entity nodes.
    
    Provides storage and retrieval of entity nodes by type and attributes.
    """

    def __init__(self) -> None:
        """Initialize the repository."""
        self._entities: dict[str, Node] = {}
        self._type_index: dict[str, list[str]] = {}

    def create(self, entity: Node) -> Node:
        """
        Create a new entity.
        
        Args:
            entity: The entity to create
            
        Returns:
            The created entity
        """
        if entity.node_id in self._entities:
            raise ValueError(f"Entity {entity.node_id} already exists")
        
        self._entities[entity.node_id] = entity
        
        # Update type index
        node_type = entity.node_type.value
        if node_type not in self._type_index:
            self._type_index[node_type] = []
        if entity.node_id not in self._type_index[node_type]:
            self._type_index[node_type].append(entity.node_id)
        
        return entity

    def update(self, entity: Node) -> Node:
        """
        Update an existing entity.
        
        Args:
            entity: The entity to update
            
        Returns:
            The updated entity
        """
        if entity.node_id not in self._entities:
            raise ValueError(f"Entity {entity.node_id} not found")
        self._entities[entity.node_id] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by ID.
        
        Args:
            entity_id: The ID of the entity to delete
            
        Returns:
            True if deleted
        """
        if entity_id not in self._entities:
            return False
        
        entity = self._entities[entity_id]
        
        # Remove from type index
        node_type = entity.node_type.value
        if node_type in self._type_index:
            self._type_index[node_type] = [
                e for e in self._type_index[node_type] if e != entity_id
            ]
        
        del self._entities[entity_id]
        return True

    def get_by_id(self, entity_id: str) -> Node | None:
        """
        Get an entity by ID.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            The entity or None
        """
        return self._entities.get(entity_id)

    def list(self, **kwargs: Any) -> list[Node]:
        """
        List entities with optional filtering.
        
        Args:
            **kwargs: Optional filters:
                - node_type: Filter by NodeType
                - attribute_key: Filter by attribute existence
                - attribute_value: Filter by attribute value
                
        Returns:
            List of matching entities
        """
        results = list(self._entities.values())
        
        node_type = kwargs.get("node_type")
        if node_type:
            if isinstance(node_type, str):
                node_type = NodeType(node_type)
            results = [e for e in results if e.node_type == node_type]
        
        attribute_key = kwargs.get("attribute_key")
        if attribute_key:
            results = [
                e for e in results if attribute_key in e.attributes
            ]
        
        attribute_value = kwargs.get("attribute_value")
        if attribute_value is not None:
            results = [
                e for e in results
                if e.attributes.get(attribute_key) == attribute_value
            ]
        
        return results

    def search(self, query: str, **kwargs: Any) -> list[Node]:
        """
        Search entities by query.
        
        Args:
            query: Search query
            **kwargs: Ignored
            
        Returns:
            Matching entities
        """
        query_lower = query.lower()
        return [
            e for e in self._entities.values()
            if query_lower in e.node_id.lower()
            or query_lower in e.node_type.value.lower()
            or any(
                query_lower in str(v).lower()
                for v in e.attributes.values()
            )
        ]

    def exists(self, entity_id: str) -> bool:
        """Check if an entity exists."""
        return entity_id in self._entities

    def count(self, **kwargs: Any) -> int:
        """Count entities matching criteria."""
        return len(self.list(**kwargs))

    def clear(self) -> None:
        """Clear all entities."""
        self._entities.clear()
        self._type_index.clear()

    def find_by_type(self, node_type: NodeType) -> list[Node]:
        """
        Find all entities of a specific type.
        
        Args:
            node_type: The node type to filter by
            
        Returns:
            List of entities
        """
        if isinstance(node_type, str):
            node_type = NodeType(node_type)
        entity_ids = self._type_index.get(node_type.value, [])
        return [self._entities[eid] for eid in entity_ids if eid in self._entities]

    def find_by_attribute(
        self, key: str, value: Any | None = None
    ) -> list[Node]:
        """
        Find entities by attribute.
        
        Args:
            key: Attribute key
            value: Optional attribute value to match
            
        Returns:
            List of matching entities
        """
        if value is None:
            return [e for e in self._entities.values() if key in e.attributes]
        return [
            e for e in self._entities.values()
            if e.attributes.get(key) == value
        ]

    def find_by_identity_ref(self, identity_ref: str) -> list[Node]:
        """
        Find entities with a specific identity reference.
        
        Args:
            identity_ref: The identity reference to search for
            
        Returns:
            List of matching entities
        """
        return [
            e for e in self._entities.values()
            if identity_ref in e.identity_refs
        ]
