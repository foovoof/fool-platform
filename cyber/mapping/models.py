"""
cyber/mapping/models.py

Cyber Knowledge Mapping Models.

Immutable dataclass models for mapping cyber domain entities
to knowledge graph entities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class MappingType(Enum):
    """Type of mapping."""
    ENTITY = "entity"
    RELATIONSHIP = "relationship"
    ONTOLOGY = "ontology"
    ATTRIBUTE = "attribute"


class MappingStatus(Enum):
    """Mapping status."""
    PENDING = "pending"
    MAPPED = "mapped"
    VALIDATED = "validated"
    INVALID = "invalid"


@dataclass(frozen=True)
class MappingMetadata:
    """Metadata for a mapping."""
    version: str = "1.0.0"
    source: str = ""
    author: str = ""
    description: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "source": self.source,
            "author": self.author,
            "description": self.description,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class KnowledgeReference:
    """Reference to a knowledge graph entity."""
    entity_id: str = ""
    entity_type: str = ""
    namespace: str = ""
    version: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "namespace": self.namespace,
            "version": self.version,
        }


@dataclass(frozen=True)
class OntologyBinding:
    """Binding between cyber and knowledge ontology."""
    binding_id: str = field(default_factory=lambda: str(uuid4()))
    cyber_concept: str = ""
    knowledge_concept: str = ""
    cyber_namespace: str = ""
    knowledge_namespace: str = ""
    mapping_type: MappingType = MappingType.ONTOLOGY
    metadata: MappingMetadata = field(default_factory=MappingMetadata)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "cyber_concept": self.cyber_concept,
            "knowledge_concept": self.knowledge_concept,
            "cyber_namespace": self.cyber_namespace,
            "knowledge_namespace": self.knowledge_namespace,
            "mapping_type": self.mapping_type.value,
            "metadata": self.metadata.to_dict(),
        }


@dataclass(frozen=True)
class EntityMapping:
    """Mapping of a cyber entity to a knowledge entity."""
    mapping_id: str = field(default_factory=lambda: str(uuid4()))
    source_entity_type: str = ""
    source_entity_id: str = ""
    source_attributes: tuple[str, ...] = field(default_factory=tuple)
    target_knowledge: KnowledgeReference = field(default_factory=KnowledgeReference)
    ontology_bindings: tuple[OntologyBinding, ...] = field(default_factory=tuple)
    status: MappingStatus = MappingStatus.PENDING
    metadata: MappingMetadata = field(default_factory=MappingMetadata)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "mapping_id": self.mapping_id,
            "source_entity_type": self.source_entity_type,
            "source_entity_id": self.source_entity_id,
            "source_attributes": list(self.source_attributes),
            "target_knowledge": self.target_knowledge.to_dict(),
            "ontology_bindings": [b.to_dict() for b in self.ontology_bindings],
            "status": self.status.value,
            "metadata": self.metadata.to_dict(),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class RelationshipMapping:
    """Mapping of cyber relationships to knowledge relationships."""
    mapping_id: str = field(default_factory=lambda: str(uuid4()))
    source_relationship_type: str = ""
    source_entity_a_type: str = ""
    source_entity_b_type: str = ""
    target_relationship_type: str = ""
    target_knowledge: KnowledgeReference = field(default_factory=KnowledgeReference)
    mapping_direction: str = "bidirectional"
    metadata: MappingMetadata = field(default_factory=MappingMetadata)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "mapping_id": self.mapping_id,
            "source_relationship_type": self.source_relationship_type,
            "source_entity_a_type": self.source_entity_a_type,
            "source_entity_b_type": self.source_entity_b_type,
            "target_relationship_type": self.target_relationship_type,
            "target_knowledge": self.target_knowledge.to_dict(),
            "mapping_direction": self.mapping_direction,
            "metadata": self.metadata.to_dict(),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class CyberKnowledgeMapping:
    """Complete mapping of a cyber entity to knowledge graph."""
    mapping_id: str = field(default_factory=lambda: str(uuid4()))
    entity_mapping: EntityMapping | None = None
    relationship_mappings: tuple[RelationshipMapping, ...] = field(default_factory=tuple)
    ontology_bindings: tuple[OntologyBinding, ...] = field(default_factory=tuple)
    status: MappingStatus = MappingStatus.PENDING
    metadata: MappingMetadata = field(default_factory=MappingMetadata)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "mapping_id": self.mapping_id,
            "entity_mapping": self.entity_mapping.to_dict() if self.entity_mapping else None,
            "relationship_mappings": [r.to_dict() for r in self.relationship_mappings],
            "ontology_bindings": [b.to_dict() for b in self.ontology_bindings],
            "status": self.status.value,
            "metadata": self.metadata.to_dict(),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class MappingResult:
    """Result of a mapping operation."""
    success: bool = False
    mapping: CyberKnowledgeMapping | None = None
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    execution_time_ms: float = 0.0
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "mapping": self.mapping.to_dict() if self.mapping else None,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "execution_time_ms": self.execution_time_ms,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ValidationIssue:
    """Validation issue for mappings."""
    severity: str = "error"
    code: str = ""
    message: str = ""
    path: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class ValidationResult:
    """Result of mapping validation."""
    is_valid: bool = True
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [i.to_dict() for i in self.issues],
            "metadata": self.metadata,
        }


class CyberEntityType(Enum):
    """Cyber entity types for mapping."""
    INDICATOR = "indicator"
    OBSERVABLE = "observable"
    THREAT_ACTOR = "threat_actor"
    CAMPAIGN = "campaign"
    MALWARE = "malware"
    INFRASTRUCTURE = "infrastructure"
    IDENTITY = "identity"
    VICTIM = "victim"
    ORGANIZATION = "organization"
    TECHNIQUE = "technique"
    TACTIC = "tactic"
    PROCEDURE = "procedure"
    ATTACK_PATTERN = "attack_pattern"
    EVIDENCE = "evidence"
    FINDING = "finding"
    ARTIFACT = "artifact"
    VULNERABILITY = "vulnerability"
    TOOL = "tool"
    REPORT = "report"
    COURSE_OF_ACTION = "course_of_action"
