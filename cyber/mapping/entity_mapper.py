"""
cyber/mapping/entity_mapper.py

Entity Mapper.

Maps cyber domain entities to knowledge graph entities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from cyber.mapping.models import (
    EntityMapping,
    CyberKnowledgeMapping,
    KnowledgeReference,
    OntologyBinding,
    MappingMetadata,
    MappingStatus,
    CyberEntityType,
    MappingType,
)

if TYPE_CHECKING:
    from cyber.mapping.registry import MappingRegistry


@dataclass(frozen=True)
class EntityMappingResult:
    """Result of entity mapping."""
    entity_mapping: EntityMapping | None = None
    bindings: tuple[OntologyBinding, ...] = ()
    errors: tuple[str, ...] = ()
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_mapping": self.entity_mapping.to_dict() if self.entity_mapping else None,
            "bindings": [b.to_dict() for b in self.bindings],
            "errors": list(self.errors),
        }


class BaseEntityMapper:
    """
    Base class for entity mappers.
    
    Each mapper creates semantic bindings only.
    No reasoning. No enrichment.
    """
    
    entity_type: CyberEntityType = CyberEntityType.INDICATOR
    knowledge_entity_type: str = "Entity"
    knowledge_namespace: str = "cyber"
    cyber_namespace: str = "cyber"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """
        Map a cyber entity to a knowledge entity.
        
        Args:
            entity_id: Cyber entity ID
            attributes: Entity attributes
            metadata: Optional metadata
            
        Returns:
            Entity mapping result
        """
        raise NotImplementedError("Subclasses must implement map()")
    
    def _create_reference(self, entity_id: str) -> KnowledgeReference:
        """Create knowledge reference."""
        return KnowledgeReference(
            entity_id=entity_id,
            entity_type=self.knowledge_entity_type,
            namespace=self.knowledge_namespace,
        )
    
    def _create_binding(
        self,
        cyber_concept: str,
        knowledge_concept: str,
    ) -> OntologyBinding:
        """Create ontology binding."""
        return OntologyBinding(
            cyber_concept=cyber_concept,
            knowledge_concept=knowledge_concept,
            cyber_namespace=self.cyber_namespace,
            knowledge_namespace=self.knowledge_namespace,
        )


class IndicatorMapper(BaseEntityMapper):
    """Mapper for indicator entities."""
    
    entity_type = CyberEntityType.INDICATOR
    knowledge_entity_type = "Indicator"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map indicator to knowledge."""
        bindings = (
            self._create_binding("indicator", "Indicator"),
            self._create_binding("pattern", "IndicatorPattern"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class ObservableMapper(BaseEntityMapper):
    """Mapper for observable entities."""
    
    entity_type = CyberEntityType.OBSERVABLE
    knowledge_entity_type = "Observable"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map observable to knowledge."""
        bindings = (
            self._create_binding("observable", "Observable"),
            self._create_binding("object", "CyberObject"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class ThreatActorMapper(BaseEntityMapper):
    """Mapper for threat actor entities."""
    
    entity_type = CyberEntityType.THREAT_ACTOR
    knowledge_entity_type = "Actor"
    knowledge_namespace = "cyber"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map threat actor to knowledge."""
        bindings = (
            self._create_binding("threat_actor", "Actor"),
            self._create_binding("threat_actor_type", "ActorType"),
            self._create_binding("aliases", "ActorAlias"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class MalwareMapper(BaseEntityMapper):
    """Mapper for malware entities."""
    
    entity_type = CyberEntityType.MALWARE
    knowledge_entity_type = "Malware"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map malware to knowledge."""
        bindings = (
            self._create_binding("malware", "Malware"),
            self._create_binding("malware_family", "MalwareFamily"),
            self._create_binding("capabilities", "MalwareCapability"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class InfrastructureMapper(BaseEntityMapper):
    """Mapper for infrastructure entities."""
    
    entity_type = CyberEntityType.INFRASTRUCTURE
    knowledge_entity_type = "Infrastructure"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map infrastructure to knowledge."""
        bindings = (
            self._create_binding("infrastructure", "Infrastructure"),
            self._create_binding("host", "Host"),
            self._create_binding("network", "Network"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class TechniqueMapper(BaseEntityMapper):
    """Mapper for technique entities."""
    
    entity_type = CyberEntityType.TECHNIQUE
    knowledge_entity_type = "Technique"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map technique to knowledge."""
        bindings = (
            self._create_binding("technique", "Technique"),
            self._create_binding("tactic", "Tactic"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class VulnerabilityMapper(BaseEntityMapper):
    """Mapper for vulnerability entities."""
    
    entity_type = CyberEntityType.VULNERABILITY
    knowledge_entity_type = "Vulnerability"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map vulnerability to knowledge."""
        bindings = (
            self._create_binding("vulnerability", "Vulnerability"),
            self._create_binding("cve", "CVE"),
            self._create_binding("severity", "Severity"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class ToolMapper(BaseEntityMapper):
    """Mapper for tool entities."""
    
    entity_type = CyberEntityType.TOOL
    knowledge_entity_type = "Tool"
    
    def map(
        self,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> EntityMappingResult:
        """Map tool to knowledge."""
        bindings = (
            self._create_binding("tool", "Tool"),
            self._create_binding("software", "Software"),
        )
        
        reference = self._create_reference(entity_id)
        
        entity_mapping = EntityMapping(
            source_entity_type=self.entity_type.value,
            source_entity_id=entity_id,
            source_attributes=tuple(attributes.keys()),
            target_knowledge=reference,
            ontology_bindings=bindings,
            status=MappingStatus.MAPPED,
            metadata=metadata or MappingMetadata(),
        )
        
        return EntityMappingResult(
            entity_mapping=entity_mapping,
            bindings=bindings,
        )


class EntityMapperRegistry:
    """
    Registry for entity mappers.
    
    Maps entity types to their respective mappers.
    """
    
    _mappers: dict[CyberEntityType, type[BaseEntityMapper]] = {
        CyberEntityType.INDICATOR: IndicatorMapper,
        CyberEntityType.OBSERVABLE: ObservableMapper,
        CyberEntityType.THREAT_ACTOR: ThreatActorMapper,
        CyberEntityType.MALWARE: MalwareMapper,
        CyberEntityType.INFRASTRUCTURE: InfrastructureMapper,
        CyberEntityType.TECHNIQUE: TechniqueMapper,
        CyberEntityType.VULNERABILITY: VulnerabilityMapper,
        CyberEntityType.TOOL: ToolMapper,
    }
    
    @classmethod
    def get_mapper(cls, entity_type: CyberEntityType) -> BaseEntityMapper | None:
        """Get mapper for entity type."""
        mapper_class = cls._mappers.get(entity_type)
        if mapper_class:
            return mapper_class()
        return None
    
    @classmethod
    def register(cls, entity_type: CyberEntityType, mapper_class: type[BaseEntityMapper]) -> None:
        """Register a mapper for entity type."""
        cls._mappers[entity_type] = mapper_class
    
    @classmethod
    def list_types(cls) -> list[CyberEntityType]:
        """List all registered entity types."""
        return list(cls._mappers.keys())
