from __future__ import annotations

"""
knowledge/services/__init__.py

Knowledge services for the Knowledge Layer.

Provides orchestration of knowledge operations.
"""
from knowledge.services.knowledge_graph_service import KnowledgeGraphService
from knowledge.services.entity_resolution_service import EntityResolutionService
from knowledge.services.identity_resolution_service import IdentityResolutionService
from knowledge.services.relationship_resolution_service import RelationshipResolutionService
from knowledge.services.ontology_service import OntologyService

__all__ = [
    "KnowledgeGraphService",
    "EntityResolutionService",
    "IdentityResolutionService",
    "RelationshipResolutionService",
    "OntologyService",
]
