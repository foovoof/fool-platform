"""
cyber/mapping/validation.py

Mapping Validation.

Validates cyber knowledge mappings for consistency and correctness.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cyber.mapping.models import (
    CyberKnowledgeMapping,
    EntityMapping,
    RelationshipMapping,
    OntologyBinding,
    ValidationResult,
    ValidationIssue,
    MappingStatus,
)


@dataclass(frozen=True)
class MappingValidationResult:
    """Result of mapping validation."""
    is_valid: bool = True
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    warnings: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [i.to_dict() for i in self.issues],
            "warnings": [w.to_dict() for w in self.warnings],
            "metadata": self.metadata,
        }


class OntologyConsistencyValidator:
    """Validates ontology consistency."""
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate ontology consistency.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        for binding in mapping.ontology_bindings:
            if not binding.cyber_concept:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_CYBER_CONCEPT",
                    message="Ontology binding missing cyber_concept",
                    path=f"ontology_bindings.{binding.binding_id}",
                ))
            
            if not binding.knowledge_concept:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_KNOWLEDGE_CONCEPT",
                    message="Ontology binding missing knowledge_concept",
                    path=f"ontology_bindings.{binding.binding_id}",
                ))
            
            if binding.cyber_namespace == binding.knowledge_namespace:
                warnings.append(ValidationIssue(
                    severity="warning",
                    code="SAME_NAMESPACE",
                    message="Cyber and knowledge namespaces are the same",
                    path=f"ontology_bindings.{binding.binding_id}",
                ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
            warnings=tuple(warnings),
        )


class EntityConsistencyValidator:
    """Validates entity mapping consistency."""
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate entity consistency.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        entity_mapping = mapping.entity_mapping
        if not entity_mapping:
            return MappingValidationResult(
                is_valid=True,
                issues=(),
                warnings=(),
            )
        
        if not entity_mapping.source_entity_type:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_ENTITY_TYPE",
                message="Entity mapping missing source_entity_type",
                path="entity_mapping",
            ))
        
        if not entity_mapping.source_entity_id:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_ENTITY_ID",
                message="Entity mapping missing source_entity_id",
                path="entity_mapping",
            ))
        
        if not entity_mapping.target_knowledge.entity_id:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_TARGET_ID",
                message="Entity mapping missing target_knowledge.entity_id",
                path="entity_mapping.target_knowledge",
            ))
        
        if not entity_mapping.ontology_bindings and entity_mapping.status == MappingStatus.MAPPED:
            warnings.append(ValidationIssue(
                severity="warning",
                code="NO_BINDINGS",
                message="Mapped entity has no ontology bindings",
                path="entity_mapping",
            ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
            warnings=tuple(warnings),
        )


class RelationshipConsistencyValidator:
    """Validates relationship mapping consistency."""
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate relationship consistency.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        for i, rel_mapping in enumerate(mapping.relationship_mappings):
            if not rel_mapping.source_relationship_type:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_REL_TYPE",
                    message="Relationship mapping missing source_relationship_type",
                    path=f"relationship_mappings[{i}]",
                ))
            
            if not rel_mapping.source_entity_a_type:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_SOURCE_TYPE",
                    message="Relationship mapping missing source_entity_a_type",
                    path=f"relationship_mappings[{i}]",
                ))
            
            if not rel_mapping.source_entity_b_type:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_TARGET_TYPE",
                    message="Relationship mapping missing source_entity_b_type",
                    path=f"relationship_mappings[{i}]",
                ))
            
            if not rel_mapping.target_relationship_type:
                issues.append(ValidationIssue(
                    severity="error",
                    code="MISSING_TARGET_REL_TYPE",
                    message="Relationship mapping missing target_relationship_type",
                    path=f"relationship_mappings[{i}]",
                ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
            warnings=tuple(warnings),
        )


class MappingCompletenessValidator:
    """Validates mapping completeness."""
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate mapping completeness.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        if not mapping.entity_mapping and not mapping.relationship_mappings:
            issues.append(ValidationIssue(
                severity="error",
                code="EMPTY_MAPPING",
                message="Mapping has no entity or relationship mappings",
                path="mapping",
            ))
        
        if mapping.entity_mapping and mapping.status == MappingStatus.PENDING:
            warnings.append(ValidationIssue(
                severity="warning",
                code="PENDING_MAPPING",
                message="Entity mapping is still pending",
                path="mapping.status",
            ))
        
        if not mapping.ontology_bindings:
            warnings.append(ValidationIssue(
                severity="warning",
                code="NO_ONTOLOGY_BINDINGS",
                message="Mapping has no ontology bindings",
                path="mapping.ontology_bindings",
            ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
            warnings=tuple(warnings),
        )


class DuplicateMappingValidator:
    """Validates for duplicate mappings."""
    
    def __init__(self) -> None:
        """Initialize validator."""
        self._seen_entity_ids: set[str] = set()
        self._seen_relationships: set[str] = set()
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate for duplicates.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        issues = []
        
        if mapping.entity_mapping:
            entity_key = f"{mapping.entity_mapping.source_entity_type}:{mapping.entity_mapping.source_entity_id}"
            
            if entity_key in self._seen_entity_ids:
                issues.append(ValidationIssue(
                    severity="error",
                    code="DUPLICATE_ENTITY",
                    message=f"Duplicate entity mapping: {entity_key}",
                    path="entity_mapping",
                ))
            
            self._seen_entity_ids.add(entity_key)
        
        for rel_mapping in mapping.relationship_mappings:
            rel_key = f"{rel_mapping.source_entity_a_type}:{rel_mapping.source_relationship_type}:{rel_mapping.source_entity_b_type}"
            
            if rel_key in self._seen_relationships:
                issues.append(ValidationIssue(
                    severity="error",
                    code="DUPLICATE_RELATIONSHIP",
                    message=f"Duplicate relationship mapping: {rel_key}",
                    path="relationship_mappings",
                ))
            
            self._seen_relationships.add(rel_key)
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )
    
    def reset(self) -> None:
        """Reset seen entities/relationships."""
        self._seen_entity_ids.clear()
        self._seen_relationships.clear()


class MappingValidator:
    """
    Main mapping validator.
    
    Coordinates all validation checks.
    """
    
    def __init__(self) -> None:
        """Initialize validator."""
        self._ontology_validator = OntologyConsistencyValidator()
        self._entity_validator = EntityConsistencyValidator()
        self._relationship_validator = RelationshipConsistencyValidator()
        self._completeness_validator = MappingCompletenessValidator()
        self._duplicate_validator = DuplicateMappingValidator()
    
    def validate(self, mapping: CyberKnowledgeMapping) -> MappingValidationResult:
        """
        Validate a complete mapping.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Combined validation result
        """
        all_issues = []
        all_warnings = []
        
        ontology_result = self._ontology_validator.validate(mapping)
        all_issues.extend(ontology_result.issues)
        all_warnings.extend(ontology_result.warnings)
        
        entity_result = self._entity_validator.validate(mapping)
        all_issues.extend(entity_result.issues)
        all_warnings.extend(entity_result.warnings)
        
        relationship_result = self._relationship_validator.validate(mapping)
        all_issues.extend(relationship_result.issues)
        all_warnings.extend(relationship_result.warnings)
        
        completeness_result = self._completeness_validator.validate(mapping)
        all_issues.extend(completeness_result.issues)
        all_warnings.extend(completeness_result.warnings)
        
        duplicate_result = self._duplicate_validator.validate(mapping)
        all_issues.extend(duplicate_result.issues)
        
        return MappingValidationResult(
            is_valid=len(all_issues) == 0,
            issues=tuple(all_issues),
            warnings=tuple(all_warnings),
        )
    
    def validate_entity(self, entity_mapping: EntityMapping) -> MappingValidationResult:
        """Validate an entity mapping."""
        issues = []
        
        if not entity_mapping.source_entity_type:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_ENTITY_TYPE",
                message="Entity mapping missing source_entity_type",
                path="source_entity_type",
            ))
        
        if not entity_mapping.source_entity_id:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_ENTITY_ID",
                message="Entity mapping missing source_entity_id",
                path="source_entity_id",
            ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )
    
    def validate_relationship(self, rel_mapping: RelationshipMapping) -> MappingValidationResult:
        """Validate a relationship mapping."""
        issues = []
        
        if not rel_mapping.source_relationship_type:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_REL_TYPE",
                message="Relationship mapping missing source_relationship_type",
                path="source_relationship_type",
            ))
        
        if not rel_mapping.target_relationship_type:
            issues.append(ValidationIssue(
                severity="error",
                code="MISSING_TARGET_REL_TYPE",
                message="Relationship mapping missing target_relationship_type",
                path="target_relationship_type",
            ))
        
        return MappingValidationResult(
            is_valid=len(issues) == 0,
            issues=tuple(issues),
        )
