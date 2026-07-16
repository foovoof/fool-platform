"""
cyber/mapping/relationship_mapper.py

Relationship Mapper.

Maps cyber domain relationships to knowledge relationships.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cyber.mapping.models import (
    RelationshipMapping,
    KnowledgeReference,
    MappingMetadata,
    MappingStatus,
    CyberEntityType,
)


@dataclass(frozen=True)
class RelationshipMappingResult:
    """Result of relationship mapping."""
    relationship_mapping: RelationshipMapping | None = None
    errors: tuple[str, ...] = ()
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_mapping": self.relationship_mapping.to_dict() if self.relationship_mapping else None,
            "errors": list(self.errors),
        }


@dataclass(frozen=True)
class RelationshipBinding:
    """Binding for a relationship type."""
    source_type: str
    target_type: str
    knowledge_relationship: str
    direction: str = "bidirectional"


class BaseRelationshipMapper:
    """
    Base class for relationship mappers.
    
    Creates canonical relationship bindings only.
    """
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """
        Map a cyber relationship to a knowledge relationship.
        
        Args:
            source_type: Source entity type
            target_type: Target entity type
            relationship_type: Type of relationship
            metadata: Optional metadata
            
        Returns:
            Relationship mapping result
        """
        raise NotImplementedError("Subclasses must implement map()")
    
    def _create_reference(self, relationship_id: str, entity_type: str = "Relationship") -> KnowledgeReference:
        """Create knowledge reference."""
        return KnowledgeReference(
            entity_id=relationship_id,
            entity_type=entity_type,
            namespace="cyber",
        )


class ThreatActorMalwareMapper(BaseRelationshipMapper):
    """Maps threat actor -> malware relationships."""
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """Map threat actor to malware relationship."""
        if source_type == CyberEntityType.THREAT_ACTOR.value and target_type == CyberEntityType.MALWARE.value:
            target_relationship = "uses_malware"
        elif source_type == CyberEntityType.MALWARE.value and target_type == CyberEntityType.THREAT_ACTOR.value:
            target_relationship = "used_by"
        else:
            target_relationship = "related_to"
        
        reference = self._create_reference(f"{source_type}_{relationship_type}_{target_type}")
        
        mapping = RelationshipMapping(
            source_relationship_type=relationship_type,
            source_entity_a_type=source_type,
            source_entity_b_type=target_type,
            target_relationship_type=target_relationship,
            target_knowledge=reference,
            mapping_direction="directed",
            metadata=metadata or MappingMetadata(),
        )
        
        return RelationshipMappingResult(relationship_mapping=mapping)


class ActorInfrastructureMapper(BaseRelationshipMapper):
    """Maps threat actor -> infrastructure relationships."""
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """Map threat actor to infrastructure relationship."""
        if source_type == CyberEntityType.THREAT_ACTOR.value and target_type == CyberEntityType.INFRASTRUCTURE.value:
            target_relationship = "uses_infrastructure"
        elif source_type == CyberEntityType.INFRASTRUCTURE.value and target_type == CyberEntityType.THREAT_ACTOR.value:
            target_relationship = "used_by"
        else:
            target_relationship = "related_to"
        
        reference = self._create_reference(f"{source_type}_{relationship_type}_{target_type}")
        
        mapping = RelationshipMapping(
            source_relationship_type=relationship_type,
            source_entity_a_type=source_type,
            source_entity_b_type=target_type,
            target_relationship_type=target_relationship,
            target_knowledge=reference,
            mapping_direction="directed",
            metadata=metadata or MappingMetadata(),
        )
        
        return RelationshipMappingResult(relationship_mapping=mapping)


class MalwareTechniqueMapper(BaseRelationshipMapper):
    """Maps malware -> technique relationships."""
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """Map malware to technique relationship."""
        if source_type == CyberEntityType.MALWARE.value and target_type == CyberEntityType.TECHNIQUE.value:
            target_relationship = "uses_technique"
        elif source_type == CyberEntityType.TECHNIQUE.value and target_type == CyberEntityType.MALWARE.value:
            target_relationship = "used_by_malware"
        else:
            target_relationship = "related_to"
        
        reference = self._create_reference(f"{source_type}_{relationship_type}_{target_type}")
        
        mapping = RelationshipMapping(
            source_relationship_type=relationship_type,
            source_entity_a_type=source_type,
            source_entity_b_type=target_type,
            target_relationship_type=target_relationship,
            target_knowledge=reference,
            mapping_direction="directed",
            metadata=metadata or MappingMetadata(),
        )
        
        return RelationshipMappingResult(relationship_mapping=mapping)


class IndicatorObservableMapper(BaseRelationshipMapper):
    """Maps indicator -> observable relationships."""
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """Map indicator to observable relationship."""
        if source_type == CyberEntityType.INDICATOR.value and target_type == CyberEntityType.OBSERVABLE.value:
            target_relationship = "based_on"
        elif source_type == CyberEntityType.OBSERVABLE.value and target_type == CyberEntityType.INDICATOR.value:
            target_relationship = "generates"
        else:
            target_relationship = "related_to"
        
        reference = self._create_reference(f"{source_type}_{relationship_type}_{target_type}")
        
        mapping = RelationshipMapping(
            source_relationship_type=relationship_type,
            source_entity_a_type=source_type,
            source_entity_b_type=target_type,
            target_relationship_type=target_relationship,
            target_knowledge=reference,
            mapping_direction="bidirectional",
            metadata=metadata or MappingMetadata(),
        )
        
        return RelationshipMappingResult(relationship_mapping=mapping)


class GenericRelationshipMapper(BaseRelationshipMapper):
    """Generic relationship mapper for unmapped types."""
    
    def map(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> RelationshipMappingResult:
        """Map generic relationship."""
        reference = self._create_reference(f"{source_type}_{relationship_type}_{target_type}")
        
        mapping = RelationshipMapping(
            source_relationship_type=relationship_type,
            source_entity_a_type=source_type,
            source_entity_b_type=target_type,
            target_relationship_type="related_to",
            target_knowledge=reference,
            mapping_direction="bidirectional",
            metadata=metadata or MappingMetadata(),
        )
        
        return RelationshipMappingResult(relationship_mapping=mapping)


class RelationshipMapperRegistry:
    """
    Registry for relationship mappers.
    """
    
    _mappers: dict[tuple[str, str], type[BaseRelationshipMapper]] = {
        (CyberEntityType.THREAT_ACTOR.value, CyberEntityType.MALWARE.value): ThreatActorMalwareMapper,
        (CyberEntityType.MALWARE.value, CyberEntityType.THREAT_ACTOR.value): ThreatActorMalwareMapper,
        (CyberEntityType.THREAT_ACTOR.value, CyberEntityType.INFRASTRUCTURE.value): ActorInfrastructureMapper,
        (CyberEntityType.INFRASTRUCTURE.value, CyberEntityType.THREAT_ACTOR.value): ActorInfrastructureMapper,
        (CyberEntityType.MALWARE.value, CyberEntityType.TECHNIQUE.value): MalwareTechniqueMapper,
        (CyberEntityType.TECHNIQUE.value, CyberEntityType.MALWARE.value): MalwareTechniqueMapper,
        (CyberEntityType.INDICATOR.value, CyberEntityType.OBSERVABLE.value): IndicatorObservableMapper,
        (CyberEntityType.OBSERVABLE.value, CyberEntityType.INDICATOR.value): IndicatorObservableMapper,
    }
    
    @classmethod
    def get_mapper(cls, source_type: str, target_type: str) -> BaseRelationshipMapper:
        """Get mapper for entity type pair."""
        key = (source_type, target_type)
        mapper_class = cls._mappers.get(key)
        if mapper_class:
            return mapper_class()
        return GenericRelationshipMapper()
    
    @classmethod
    def register(
        cls,
        source_type: str,
        target_type: str,
        mapper_class: type[BaseRelationshipMapper],
    ) -> None:
        """Register a mapper for entity type pair."""
        cls._mappers[(source_type, target_type)] = mapper_class
    
    @classmethod
    def list_bindings(cls) -> list[tuple[str, str]]:
        """List all registered bindings."""
        return list(cls._mappers.keys())
