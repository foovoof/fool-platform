from __future__ import annotations

"""
knowledge/ontology/__init__.py

Ontology implementations for the Knowledge Layer.

Provides ontology loading, mapping, and validation.
"""
from knowledge.ontology.ontology_loader import (
    OntologyLoader,
    OntologyConcept,
    OntologyEntity,
    OntologyRelationship,
    OntologyClassification,
)
from knowledge.ontology.ontology_mapper import (
    OntologyMapper,
    MappingResult,
)
from knowledge.ontology.ontology_validator import (
    OntologyValidator,
    ValidationResult,
    ValidationError,
)

__all__ = [
    "OntologyLoader",
    "OntologyConcept",
    "OntologyEntity",
    "OntologyRelationship",
    "OntologyClassification",
    "OntologyMapper",
    "MappingResult",
    "OntologyValidator",
    "ValidationResult",
    "ValidationError",
]
