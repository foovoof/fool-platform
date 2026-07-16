"""
cyber/mapping/tests/test_cyber_mapping.py

Tests for Cyber Knowledge Mapping.
"""
from __future__ import annotations

import pytest
from datetime import datetime, timezone

from cyber.mapping.models import (
    MappingType,
    MappingStatus,
    MappingMetadata,
    KnowledgeReference,
    OntologyBinding,
    EntityMapping,
    RelationshipMapping,
    CyberKnowledgeMapping,
    MappingResult,
    ValidationIssue,
    ValidationResult,
    CyberEntityType,
)
from cyber.mapping.entity_mapper import (
    BaseEntityMapper,
    EntityMapperRegistry,
    IndicatorMapper,
    ObservableMapper,
    ThreatActorMapper,
    MalwareMapper,
    InfrastructureMapper,
    TechniqueMapper,
    VulnerabilityMapper,
    ToolMapper,
)
from cyber.mapping.relationship_mapper import (
    BaseRelationshipMapper,
    RelationshipMapperRegistry,
    ThreatActorMalwareMapper,
    GenericRelationshipMapper,
)
from cyber.mapping.ontology_mapper import (
    CyberOntologyMapper,
    OntologyBindingRegistry,
    OntologyBindingValidator,
)
from cyber.mapping.registry import MappingRegistry
from cyber.mapping.validation import (
    MappingValidator,
    OntologyConsistencyValidator,
    EntityConsistencyValidator,
    RelationshipConsistencyValidator,
)
from cyber.mapping.events import (
    MappingEventEmitter,
    MappingEventType,
    MappingEvent,
)
from cyber.mapping.services import (
    CyberMappingService,
    OntologyBindingService,
    MappingValidationService,
)
from cyber.mapping.mapper import CyberKnowledgeMapper


class TestMappingModels:
    """Test mapping models."""
    
    def test_mapping_metadata(self):
        """Test metadata creation."""
        metadata = MappingMetadata(
            source="test",
            author="tester",
        )
        assert metadata.source == "test"
        assert metadata.version == "1.0.0"
    
    def test_knowledge_reference(self):
        """Test knowledge reference."""
        ref = KnowledgeReference(
            entity_id="entity-1",
            entity_type="Indicator",
        )
        assert ref.entity_id == "entity-1"
    
    def test_ontology_binding(self):
        """Test ontology binding."""
        binding = OntologyBinding(
            cyber_concept="indicator",
            knowledge_concept="Indicator",
        )
        assert binding.cyber_concept == "indicator"
        assert binding.binding_id
    
    def test_entity_mapping(self):
        """Test entity mapping."""
        ref = KnowledgeReference(entity_id="test")
        mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-1",
            target_knowledge=ref,
        )
        assert mapping.source_entity_type == "indicator"
        assert mapping.status == MappingStatus.PENDING
    
    def test_relationship_mapping(self):
        """Test relationship mapping."""
        ref = KnowledgeReference(entity_id="rel-1")
        mapping = RelationshipMapping(
            source_relationship_type="uses",
            source_entity_a_type="actor",
            source_entity_b_type="malware",
            target_relationship_type="uses_malware",
            target_knowledge=ref,
        )
        assert mapping.source_relationship_type == "uses"
    
    def test_cyber_knowledge_mapping(self):
        """Test complete mapping."""
        mapping = CyberKnowledgeMapping()
        assert mapping.mapping_id
        assert mapping.status == MappingStatus.PENDING
    
    def test_mapping_result(self):
        """Test mapping result."""
        result = MappingResult(
            success=True,
            execution_time_ms=10.5,
        )
        assert result.success
        assert result.execution_time_ms == 10.5
    
    def test_validation_issue(self):
        """Test validation issue."""
        issue = ValidationIssue(
            severity="error",
            code="TEST",
            message="Test error",
        )
        assert issue.severity == "error"
    
    def test_validation_result(self):
        """Test validation result."""
        result = ValidationResult(is_valid=True)
        assert result.is_valid
    
    def test_cyber_entity_type(self):
        """Test entity type enum."""
        assert CyberEntityType.INDICATOR.value == "indicator"
        assert CyberEntityType.MALWARE.value == "malware"


class TestEntityMappers:
    """Test entity mappers."""
    
    def test_indicator_mapper(self):
        """Test indicator mapper."""
        mapper = IndicatorMapper()
        result = mapper.map("ind-1", {"type": "ipv4", "value": "1.2.3.4"})
        
        assert result.entity_mapping is not None
        assert result.entity_mapping.source_entity_id == "ind-1"
        assert len(result.bindings) >= 1
    
    def test_observable_mapper(self):
        """Test observable mapper."""
        mapper = ObservableMapper()
        result = mapper.map("obs-1", {"type": "domain", "value": "evil.com"})
        
        assert result.entity_mapping is not None
    
    def test_threat_actor_mapper(self):
        """Test threat actor mapper."""
        mapper = ThreatActorMapper()
        result = mapper.map("actor-1", {"name": "APT1"})
        
        assert result.entity_mapping is not None
        assert result.entity_mapping.source_entity_type == "threat_actor"
    
    def test_malware_mapper(self):
        """Test malware mapper."""
        mapper = MalwareMapper()
        result = mapper.map("mal-1", {"name": "Emotet"})
        
        assert result.entity_mapping is not None
    
    def test_infrastructure_mapper(self):
        """Test infrastructure mapper."""
        mapper = InfrastructureMapper()
        result = mapper.map("inf-1", {"type": "ip"})
        
        assert result.entity_mapping is not None
    
    def test_technique_mapper(self):
        """Test technique mapper."""
        mapper = TechniqueMapper()
        result = mapper.map("tech-1", {"name": "Phishing"})
        
        assert result.entity_mapping is not None
    
    def test_vulnerability_mapper(self):
        """Test vulnerability mapper."""
        mapper = VulnerabilityMapper()
        result = mapper.map("cve-1", {"cve_id": "CVE-2021-12345"})
        
        assert result.entity_mapping is not None
    
    def test_tool_mapper(self):
        """Test tool mapper."""
        mapper = ToolMapper()
        result = mapper.map("tool-1", {"name": "nmap"})
        
        assert result.entity_mapping is not None
    
    def test_entity_mapper_registry(self):
        """Test entity mapper registry."""
        mapper = EntityMapperRegistry.get_mapper(CyberEntityType.INDICATOR)
        assert mapper is not None
        assert isinstance(mapper, IndicatorMapper)
    
    def test_entity_mapper_registry_unknown(self):
        """Test unknown entity type."""
        mapper = EntityMapperRegistry.get_mapper(CyberEntityType.CAMPAIGN)
        assert mapper is None
    
    def test_entity_mapper_registry_list(self):
        """Test listing registered types."""
        types = EntityMapperRegistry.list_types()
        assert CyberEntityType.INDICATOR in types


class TestRelationshipMappers:
    """Test relationship mappers."""
    
    def test_threat_actor_malware_mapper(self):
        """Test threat actor malware mapper."""
        mapper = ThreatActorMalwareMapper()
        result = mapper.map("threat_actor", "malware", "uses")
        
        assert result.relationship_mapping is not None
        assert result.relationship_mapping.target_relationship_type == "uses_malware"
    
    def test_generic_relationship_mapper(self):
        """Test generic mapper for unknown types."""
        mapper = GenericRelationshipMapper()
        result = mapper.map("unknown", "unknown", "relates")
        
        assert result.relationship_mapping is not None
        assert result.relationship_mapping.target_relationship_type == "related_to"
    
    def test_relationship_mapper_registry(self):
        """Test relationship mapper registry."""
        mapper = RelationshipMapperRegistry.get_mapper(
            CyberEntityType.THREAT_ACTOR.value,
            CyberEntityType.MALWARE.value,
        )
        assert isinstance(mapper, ThreatActorMalwareMapper)


class TestOntologyMappers:
    """Test ontology mappers."""
    
    def test_cyber_ontology_mapper(self):
        """Test ontology mapper."""
        mapper = CyberOntologyMapper()
        result = mapper.map_concept("indicator")
        
        assert len(result.bindings) >= 1
        assert result.errors == ()
    
    def test_cyber_ontology_mapper_unknown(self):
        """Test unknown concept."""
        mapper = CyberOntologyMapper()
        result = mapper.map_concept("unknown_concept")
        
        assert len(result.bindings) == 0
        assert len(result.errors) >= 1
    
    def test_get_mapping_for_entity(self):
        """Test getting mappings for entity."""
        mapper = CyberOntologyMapper()
        concepts = mapper.get_mapping_for_entity("malware")
        
        assert len(concepts) >= 1
        assert "Malware" in concepts
    
    def test_is_mapped(self):
        """Test concept mapping check."""
        mapper = CyberOntologyMapper()
        
        assert mapper.is_mapped("indicator")
        assert not mapper.is_mapped("unknown")
    
    def test_ontology_binding_registry(self):
        """Test binding registry."""
        registry = OntologyBindingRegistry()
        
        binding = OntologyBinding(
            cyber_concept="test",
            knowledge_concept="Test",
        )
        registry.register(binding)
        
        bindings = registry.get("test")
        assert len(bindings) == 1
        
        assert registry.count() == 1
    
    def test_ontology_binding_validator(self):
        """Test binding validator."""
        validator = OntologyBindingValidator()
        
        binding = OntologyBinding(
            cyber_concept="test",
            knowledge_concept="Test",
            cyber_namespace="cyber",
            knowledge_namespace="knowledge",
        )
        is_valid, errors = validator.validate(binding)
        
        assert is_valid
        assert errors == []


class TestRegistry:
    """Test mapping registry."""
    
    def test_registry_creation(self):
        """Test registry creation."""
        registry = MappingRegistry()
        assert registry.count() == 0
    
    def test_register_mapping(self):
        """Test mapping registration."""
        registry = MappingRegistry()
        
        mapping = CyberKnowledgeMapping()
        success = registry.register(mapping)
        
        assert success
        assert registry.count() == 1
    
    def test_get_mapping(self):
        """Test getting mapping."""
        registry = MappingRegistry()
        
        mapping = CyberKnowledgeMapping()
        registry.register(mapping)
        
        retrieved = registry.get(mapping.mapping_id)
        assert retrieved is not None
        assert retrieved.mapping_id == mapping.mapping_id
    
    def test_find_by_entity_id(self):
        """Test finding by entity ID."""
        registry = MappingRegistry()
        
        from cyber.mapping.models import KnowledgeReference
        
        entity_mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-123",
            target_knowledge=KnowledgeReference(entity_id="test"),
        )
        
        mapping = CyberKnowledgeMapping(entity_mapping=entity_mapping)
        registry.register(mapping)
        
        results = registry.find_by_entity_id("ind-123")
        assert len(results) == 1
    
    def test_clear_registry(self):
        """Test clearing registry."""
        registry = MappingRegistry()
        registry.register(CyberKnowledgeMapping())
        
        registry.clear()
        assert registry.count() == 0


class TestValidation:
    """Test validation."""
    
    def test_ontology_consistency_validator(self):
        """Test ontology consistency validator."""
        validator = OntologyConsistencyValidator()
        
        from cyber.mapping.models import KnowledgeReference
        
        entity_mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-1",
            target_knowledge=KnowledgeReference(entity_id="test"),
        )
        
        mapping = CyberKnowledgeMapping(
            entity_mapping=entity_mapping,
            ontology_bindings=(
                OntologyBinding(
                    cyber_concept="indicator",
                    knowledge_concept="Indicator",
                    cyber_namespace="cyber",
                    knowledge_namespace="knowledge",
                ),
            ),
        )
        
        result = validator.validate(mapping)
        assert result.is_valid
    
    def test_entity_consistency_validator(self):
        """Test entity consistency validator."""
        validator = EntityConsistencyValidator()
        
        from cyber.mapping.models import KnowledgeReference
        
        entity_mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-1",
            target_knowledge=KnowledgeReference(entity_id="test"),
        )
        
        mapping = CyberKnowledgeMapping(entity_mapping=entity_mapping)
        
        result = validator.validate(mapping)
        assert result.is_valid
    
    def test_mapping_validator(self):
        """Test main mapping validator."""
        validator = MappingValidator()
        
        from cyber.mapping.models import KnowledgeReference
        
        entity_mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-1",
            target_knowledge=KnowledgeReference(entity_id="test"),
        )
        
        mapping = CyberKnowledgeMapping(entity_mapping=entity_mapping)
        
        result = validator.validate(mapping)
        assert result.is_valid


class TestEvents:
    """Test events."""
    
    def test_event_emitter_creation(self):
        """Test event emitter creation."""
        emitter = MappingEventEmitter()
        assert emitter is not None
    
    def test_emit_event(self):
        """Test event emission."""
        emitter = MappingEventEmitter()
        result = emitter.emit(
            MappingEventType.CREATED,
            mapping_id="test-1",
            entity_type="indicator",
        )
        assert result
    
    def test_emit_created(self):
        """Test emit created."""
        emitter = MappingEventEmitter()
        result = emitter.emit_created("test-1", "indicator")
        assert result
    
    def test_get_events(self):
        """Test getting events."""
        emitter = MappingEventEmitter()
        emitter.emit_created("test-1", "indicator")
        
        events = emitter.get_events()
        assert len(events) == 1


class TestServices:
    """Test services."""
    
    def test_cyber_mapping_service(self):
        """Test mapping service."""
        service = CyberMappingService()
        
        result = service.map_entity(
            CyberEntityType.INDICATOR,
            "ind-1",
            {"type": "ipv4"},
        )
        
        assert result.success
    
    def test_cyber_mapping_service_unknown_type(self):
        """Test mapping unknown entity type."""
        service = CyberMappingService()
        
        result = service.map_entity(
            CyberEntityType.CAMPAIGN,
            "camp-1",
            {},
        )
        
        assert not result.success
    
    def test_ontology_binding_service(self):
        """Test ontology binding service."""
        service = OntologyBindingService()
        
        bindings = service.bind_concept("indicator")
        assert len(bindings) >= 1
    
    def test_mapping_validation_service(self):
        """Test validation service."""
        service = MappingValidationService()
        
        from cyber.mapping.models import KnowledgeReference
        
        entity_mapping = EntityMapping(
            source_entity_type="indicator",
            source_entity_id="ind-1",
            target_knowledge=KnowledgeReference(entity_id="test"),
        )
        
        mapping = CyberKnowledgeMapping(entity_mapping=entity_mapping)
        
        result = service.validate_mapping(mapping)
        assert result.is_valid


class TestMapper:
    """Test main mapper."""
    
    def test_mapper_creation(self):
        """Test mapper creation."""
        mapper = CyberKnowledgeMapper()
        assert mapper is not None
    
    def test_map_entity(self):
        """Test entity mapping."""
        mapper = CyberKnowledgeMapper()
        
        result = mapper.map_entity(
            CyberEntityType.MALWARE,
            "mal-1",
            {"name": "Test"},
        )
        
        assert result.success
    
    def test_map_relationship(self):
        """Test relationship mapping."""
        mapper = CyberKnowledgeMapper()
        
        result = mapper.map_relationship(
            "threat_actor",
            "malware",
            "uses",
        )
        
        assert result.success
    
    def test_bind_concept(self):
        """Test concept binding."""
        mapper = CyberKnowledgeMapper()
        
        bindings = mapper.bind_concept("indicator")
        assert len(bindings) >= 1
    
    def test_count_mappings(self):
        """Test counting mappings."""
        mapper = CyberKnowledgeMapper()
        
        initial_count = mapper.count_mappings()
        
        mapper.map_entity(CyberEntityType.INDICATOR, "ind-1", {})
        
        assert mapper.count_mappings() == initial_count + 1


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_intelligence_imports(self):
        """Verify no intelligence imports."""
        from pathlib import Path
        
        mapping_dir = Path(__file__).parent.parent
        for py_file in mapping_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "intelligence" not in line.lower()
                    assert "from intelligence" not in line
    
    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        mapping_dir = Path(__file__).parent.parent
        for py_file in mapping_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "openai" not in line.lower()
                    assert "anthropic" not in line.lower()
                    assert "langchain" not in line.lower()
    
    def test_no_detection_imports(self):
        """Verify no detection imports."""
        from pathlib import Path
        
        mapping_dir = Path(__file__).parent.parent
        for py_file in mapping_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "detection" not in line.lower()
                    assert "sigma" not in line.lower()
                    assert "yara" not in line.lower()
    
    def test_no_correlation_imports(self):
        """Verify no correlation imports."""
        from pathlib import Path
        
        mapping_dir = Path(__file__).parent.parent
        for py_file in mapping_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "correlation" not in line.lower()
    
    def test_no_inference_imports(self):
        """Verify no inference imports."""
        from pathlib import Path
        
        mapping_dir = Path(__file__).parent.parent
        for py_file in mapping_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "inference" not in line.lower()
