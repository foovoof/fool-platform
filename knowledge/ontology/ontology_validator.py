from __future__ import annotations

"""
knowledge/ontology/ontology_validator.py

Ontology validator for the Knowledge Layer.

Validates entities and relationships against ontology definitions.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.ontology.ontology_loader import (
    OntologyLoader,
    OntologyEntity,
    OntologyRelationship,
)


@dataclass
class ValidationError:
    """An ontology validation error."""
    error_type: str
    message: str
    entity_type: str | None = None
    attribute: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of ontology validation."""
    is_valid: bool
    entity_type: str
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def success(cls, entity_type: str) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, entity_type=entity_type)

    @classmethod
    def failure(
        cls,
        entity_type: str,
        errors: list[ValidationError],
    ) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(
            is_valid=False,
            entity_type=entity_type,
            errors=errors,
        )


class OntologyValidator:
    """
    Validates entities and relationships against ontology definitions.
    """

    def __init__(self, loader: OntologyLoader | None = None) -> None:
        """
        Initialize the ontology validator.
        
        Args:
            loader: Optional ontology loader
        """
        self._loader = loader or OntologyLoader()

    def validate_ontology(self) -> dict[str, Any]:
        """
        Validate the ontology itself.
        
        Returns:
            Validation results dictionary
        """
        results = {
            "is_valid": True,
            "concepts": {"count": 0, "errors": []},
            "entities": {"count": 0, "errors": []},
            "relationships": {"count": 0, "errors": []},
            "classifications": {"count": 0, "errors": []},
        }

        concepts = self._loader.load_concepts()
        results["concepts"]["count"] = len(concepts)
        
        entities = self._loader.load_entities()
        results["entities"]["count"] = len(entities)
        
        for entity in entities.values():
            if not entity.identity_keys:
                results["entities"]["errors"].append(
                    f"Entity '{entity.entity_type}' has no identity keys"
                )
        
        relationships = self._loader.load_relationships()
        results["relationships"]["count"] = len(relationships)
        
        classifications = self._loader.load_classifications()
        results["classifications"]["count"] = len(classifications)

        if any(r["errors"] for r in results.values() if isinstance(r, dict)):
            results["is_valid"] = False

        return results

    def validate_entity_type(self, entity_type: str) -> bool:
        """
        Check if an entity type is defined in ontology.
        
        Args:
            entity_type: The entity type to check
            
        Returns:
            True if valid
        """
        return self._loader.get_entity(entity_type) is not None

    def validate_relationship_type(self, relationship_type: str) -> bool:
        """
        Check if a relationship type is defined in ontology.
        
        Args:
            relationship_type: The relationship type to check
            
        Returns:
            True if valid
        """
        return self._loader.get_relationship(relationship_type) is not None

    def validate_entity(
        self,
        entity: dict[str, Any],
        entity_type: str,
    ) -> ValidationResult:
        """
        Validate an entity against ontology.
        
        Args:
            entity: The entity to validate
            entity_type: The expected entity type
            
        Returns:
            ValidationResult
        """
        errors: list[ValidationError] = []
        
        entity_def = self._loader.get_entity(entity_type)
        if not entity_def:
            return ValidationResult.failure(
                entity_type,
                [ValidationError(
                    error_type="unknown_type",
                    message=f"Entity type '{entity_type}' not found in ontology",
                    entity_type=entity_type,
                )],
            )

        for attr in entity_def.required_attributes:
            if attr not in entity.get("attributes", {}):
                errors.append(ValidationError(
                    error_type="missing_required_attribute",
                    message=f"Required attribute '{attr}' missing",
                    entity_type=entity_type,
                    attribute=attr,
                ))

        validation_rules = entity_def.validations
        for attr, rules in validation_rules.items():
            if attr in entity.get("attributes", {}):
                value = entity["attributes"][attr]
                
                if "type" in rules:
                    expected_type = rules["type"]
                    if not isinstance(value, eval(expected_type)):  # noqa: S307
                        errors.append(ValidationError(
                            error_type="invalid_type",
                            message=f"Attribute '{attr}' has wrong type",
                            entity_type=entity_type,
                            attribute=attr,
                            details={"expected": expected_type, "actual": type(value).__name__},
                        ))
                
                if "min_length" in rules:
                    if len(str(value)) < rules["min_length"]:
                        errors.append(ValidationError(
                            error_type="too_short",
                            message=f"Attribute '{attr}' too short",
                            entity_type=entity_type,
                            attribute=attr,
                            details={"min_length": rules["min_length"]},
                        ))
                
                if "max_length" in rules:
                    if len(str(value)) > rules["max_length"]:
                        errors.append(ValidationError(
                            error_type="too_long",
                            message=f"Attribute '{attr}' too long",
                            entity_type=entity_type,
                            attribute=attr,
                            details={"max_length": rules["max_length"]},
                        ))

        warnings: list[str] = []
        if not entity.get("identity_refs"):
            warnings.append("Entity has no identity references")

        return ValidationResult(
            is_valid=len(errors) == 0,
            entity_type=entity_type,
            errors=errors,
            warnings=warnings,
        )

    def validate_relationship(
        self,
        source_entity_type: str,
        target_entity_type: str,
        relationship_type: str,
    ) -> ValidationResult:
        """
        Validate a relationship against ontology.
        
        Args:
            source_entity_type: Source entity type
            target_entity_type: Target entity type
            relationship_type: Relationship type
            
        Returns:
            ValidationResult
        """
        errors: list[ValidationError] = []
        
        relationship_def = self._loader.get_relationship(relationship_type)
        if not relationship_def:
            return ValidationResult.failure(
                relationship_type,
                [ValidationError(
                    error_type="unknown_type",
                    message=f"Relationship type '{relationship_type}' not found",
                    details={"source": source_entity_type, "target": target_entity_type},
                )],
            )

        if not relationship_def.is_symmetric:
            if relationship_def.source_entity_types:
                if source_entity_type not in relationship_def.source_entity_types:
                    errors.append(ValidationError(
                        error_type="invalid_source_type",
                        message=f"Source type '{source_entity_type}' not allowed",
                        entity_type=relationship_type,
                        details={"allowed_types": relationship_def.source_entity_types},
                    ))

            if relationship_def.target_entity_types:
                if target_entity_type not in relationship_def.target_entity_types:
                    errors.append(ValidationError(
                        error_type="invalid_target_type",
                        message=f"Target type '{target_entity_type}' not allowed",
                        entity_type=relationship_type,
                        details={"allowed_types": relationship_def.target_entity_types},
                    ))

        return ValidationResult(
            is_valid=len(errors) == 0,
            entity_type=relationship_type,
            errors=errors,
        )
