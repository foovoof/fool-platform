from __future__ import annotations

"""
knowledge/ontology/ontology_loader.py

Ontology loader for the Knowledge Layer.

Loads ontology definitions from standards.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OntologyConcept:
    """Represents an ontology concept."""
    concept_id: str
    name: str
    description: str = ""
    parent_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyEntity:
    """Represents an ontology entity type."""
    entity_type: str
    name: str
    description: str = ""
    identity_keys: list[str] = field(default_factory=list)
    required_attributes: list[str] = field(default_factory=list)
    validations: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyRelationship:
    """Represents an ontology relationship type."""
    relationship_type: str
    name: str
    description: str = ""
    source_entity_types: list[str] = field(default_factory=list)
    target_entity_types: list[str] = field(default_factory=list)
    is_symmetric: bool = False
    is_reflexive: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyClassification:
    """Represents an ontology classification."""
    classification_id: str
    name: str
    description: str = ""
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class OntologyLoader:
    """
    Loads ontology definitions from standards.
    
    Ontology source is standards/.
    No hardcoded ontology definitions.
    """

    def __init__(self, standards_path: Path | None = None) -> None:
        """
        Initialize the ontology loader.
        
        Args:
            standards_path: Path to standards directory
        """
        self._standards_path = standards_path or Path("standards")
        self._concepts: dict[str, OntologyConcept] = {}
        self._entities: dict[str, OntologyEntity] = {}
        self._relationships: dict[str, OntologyRelationship] = {}
        self._classifications: dict[str, OntologyClassification] = {}

    def load_concepts(self) -> dict[str, OntologyConcept]:
        """
        Load ontology concepts from standards.
        
        Returns:
            Dictionary of concept_id -> OntologyConcept
        """
        self._concepts.clear()
        
        concepts_file = self._standards_path / "ontology_concepts.json"
        if concepts_file.exists():
            import json
            data = json.loads(concepts_file.read_text())
            for item in data.get("concepts", []):
                concept = OntologyConcept(
                    concept_id=item["id"],
                    name=item["name"],
                    description=item.get("description", ""),
                    parent_id=item.get("parent_id"),
                    metadata=item.get("metadata", {}),
                )
                self._concepts[concept.concept_id] = concept
        
        return self._concepts.copy()

    def load_entities(self) -> dict[str, OntologyEntity]:
        """
        Load ontology entity types from standards.
        
        Returns:
            Dictionary of entity_type -> OntologyEntity
        """
        self._entities.clear()
        
        entities_file = self._standards_path / "ontology_entities.json"
        if entities_file.exists():
            import json
            data = json.loads(entities_file.read_text())
            for item in data.get("entities", []):
                entity = OntologyEntity(
                    entity_type=item["type"],
                    name=item["name"],
                    description=item.get("description", ""),
                    identity_keys=item.get("identity_keys", []),
                    required_attributes=item.get("required_attributes", []),
                    validations=item.get("validations", {}),
                    metadata=item.get("metadata", {}),
                )
                self._entities[entity.entity_type] = entity
        
        return self._entities.copy()

    def load_relationships(self) -> dict[str, OntologyRelationship]:
        """
        Load ontology relationship types from standards.
        
        Returns:
            Dictionary of relationship_type -> OntologyRelationship
        """
        self._relationships.clear()
        
        relationships_file = self._standards_path / "ontology_relationships.json"
        if relationships_file.exists():
            import json
            data = json.loads(relationships_file.read_text())
            for item in data.get("relationships", []):
                relationship = OntologyRelationship(
                    relationship_type=item["type"],
                    name=item["name"],
                    description=item.get("description", ""),
                    source_entity_types=item.get("source_types", []),
                    target_entity_types=item.get("target_types", []),
                    is_symmetric=item.get("is_symmetric", False),
                    is_reflexive=item.get("is_reflexive", False),
                    metadata=item.get("metadata", {}),
                )
                self._relationships[relationship.relationship_type] = relationship
        
        return self._relationships.copy()

    def load_classifications(self) -> dict[str, OntologyClassification]:
        """
        Load ontology classifications from standards.
        
        Returns:
            Dictionary of classification_id -> OntologyClassification
        """
        self._classifications.clear()
        
        classifications_file = self._standards_path / "ontology_classifications.json"
        if classifications_file.exists():
            import json
            data = json.loads(classifications_file.read_text())
            for item in data.get("classifications", []):
                classification = OntologyClassification(
                    classification_id=item["id"],
                    name=item["name"],
                    description=item.get("description", ""),
                    parent_id=item.get("parent_id"),
                    children_ids=item.get("children_ids", []),
                    metadata=item.get("metadata", {}),
                )
                self._classifications[classification.classification_id] = classification
        
        return self._classifications.copy()

    def load_all(self) -> dict[str, Any]:
        """
        Load all ontology definitions.
        
        Returns:
            Dictionary with concepts, entities, relationships, classifications
        """
        return {
            "concepts": self.load_concepts(),
            "entities": self.load_entities(),
            "relationships": self.load_relationships(),
            "classifications": self.load_classifications(),
        }

    def get_concept(self, concept_id: str) -> OntologyConcept | None:
        """Get a concept by ID."""
        if not self._concepts:
            self.load_concepts()
        return self._concepts.get(concept_id)

    def get_entity(self, entity_type: str) -> OntologyEntity | None:
        """Get an entity by type."""
        if not self._entities:
            self.load_entities()
        return self._entities.get(entity_type)

    def get_relationship(self, relationship_type: str) -> OntologyRelationship | None:
        """Get a relationship by type."""
        if not self._relationships:
            self.load_relationships()
        return self._relationships.get(relationship_type)

    def get_classification(self, classification_id: str) -> OntologyClassification | None:
        """Get a classification by ID."""
        if not self._classifications:
            self.load_classifications()
        return self._classifications.get(classification_id)

    def get_entity_identity_keys(self, entity_type: str) -> list[str]:
        """
        Get identity keys for an entity type.
        
        Args:
            entity_type: The entity type
            
        Returns:
            List of identity key names
        """
        entity = self.get_entity(entity_type)
        if entity:
            return entity.identity_keys
        return []

    def get_required_attributes(self, entity_type: str) -> list[str]:
        """
        Get required attributes for an entity type.
        
        Args:
            entity_type: The entity type
            
        Returns:
            List of required attribute names
        """
        entity = self.get_entity(entity_type)
        if entity:
            return entity.required_attributes
        return []
