from __future__ import annotations

"""
knowledge/graph/queries/identity_queries.py

Identity queries for the Knowledge Layer.
"""
from typing import Any

from knowledge.graph.models import Graph, Node
from knowledge.graph.queries.query_context import QueryContext


class IdentityQueries:
    """
    Identity query operations.
    
    Provides query operations for identities in the graph.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize identity queries.
        
        Args:
            graph: The graph to query
        """
        self._graph = graph

    def find_by_identity_ref(
        self,
        identity_ref: str,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes by identity reference.
        
        Args:
            identity_ref: The identity reference to search for
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        results = self._graph.get_nodes_by_identity(identity_ref)
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_with_identities(
        self,
        identity_refs: list[str],
        match_all: bool = False,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes with specific identity references.
        
        Args:
            identity_refs: List of identity references to match
            match_all: If True, all identities must match
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        all_nodes = self._graph.list_nodes()
        
        if match_all:
            results = [
                node for node in all_nodes
                if all(ref in node.identity_refs for ref in identity_refs)
            ]
        else:
            results = [
                node for node in all_nodes
                if any(ref in node.identity_refs for ref in identity_refs)
            ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_by_normalized_identity(
        self,
        identity_ref: str,
        normalize_fn: callable | None = None,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes by normalized identity reference.
        
        Args:
            identity_ref: The identity reference
            normalize_fn: Optional normalization function
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        if normalize_fn:
            normalized = normalize_fn(identity_ref)
        else:
            normalized = identity_ref.lower().strip()
        
        all_nodes = self._graph.list_nodes()
        results = []
        
        for node in all_nodes:
            for ref in node.identity_refs:
                normalized_ref = normalize_fn(ref) if normalize_fn else ref.lower().strip()
                if normalized_ref == normalized:
                    results.append(node)
                    break
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def get_identity_summary(
        self,
        node_id: str,
    ) -> dict[str, Any]:
        """
        Get summary of all identities for a node.
        
        Args:
            node_id: The node ID
            
        Returns:
            Dictionary with identity summary
        """
        node = self._graph.get_node(node_id)
        if not node:
            return {"found": False}
        
        return {
            "found": True,
            "node_id": node_id,
            "identity_refs": node.identity_refs,
            "identity_count": len(node.identity_refs),
        }
