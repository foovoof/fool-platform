"""
cyber/standards/tests/test_cyber_standards.py

Tests for Cyber Standards Integration.
"""
import pytest

from cyber.standards.models import (
    StandardType,
    StandardVersion,
    StandardMetadata,
    StandardValidationResult,
    StandardMappingResult,
)
from cyber.standards.registry import CyberStandardRegistry, StandardInfo, MappingInfo
from cyber.standards.services import (
    StandardIntegrationService,
    ValidationService,
    MappingService,
    SerializationService,
)
from cyber.standards.events import (
    CyberStandardEvent,
    CyberStandardEventType,
    CyberStandardEventEmitter,
)


class TestStandardModels:
    """Test standard models."""
    
    def test_standard_type_enum(self):
        """Test StandardType enum."""
        assert StandardType.STIX.value == "stix"
        assert StandardType.ATTACK.value == "attack"
        assert StandardType.CVE.value == "cve"
        assert StandardType.CWE.value == "cwe"
        assert StandardType.CAPEC.value == "capec"
        assert StandardType.SIGMA.value == "sigma"
        assert StandardType.YARA.value == "yara"
        assert StandardType.OPENIOC.value == "openioc"
    
    def test_standard_metadata_creation(self):
        """Test StandardMetadata creation."""
        metadata = StandardMetadata(
            standard_type=StandardType.STIX,
            version="2.1",
            source="MITRE",
            author="Test",
        )
        assert metadata.standard_type == StandardType.STIX
        assert metadata.version == "2.1"
        assert metadata.source == "MITRE"
    
    def test_standard_metadata_to_dict(self):
        """Test StandardMetadata serialization."""
        metadata = StandardMetadata(
            standard_type=StandardType.ATTACK,
            version="13.0",
        )
        data = metadata.to_dict()
        assert data["standard_type"] == "attack"
        assert data["version"] == "13.0"
    
    def test_validation_result_valid(self):
        """Test validation result for valid object."""
        result = StandardValidationResult(is_valid=True)
        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
    
    def test_validation_result_invalid(self):
        """Test validation result for invalid object."""
        result = StandardValidationResult(
            is_valid=False,
            errors=("Error 1", "Error 2"),
            warnings=("Warning 1",),
        )
        assert not result.is_valid
        assert len(result.errors) == 2
        assert len(result.warnings) == 1
    
    def test_mapping_result_success(self):
        """Test mapping result for successful mapping."""
        result = StandardMappingResult(
            success=True,
            source_standard=StandardType.STIX,
            target_type="malware",
            mapped_object={"id": "test"},
        )
        assert result.success
        assert result.source_standard == StandardType.STIX
        assert result.mapped_object["id"] == "test"
    
    def test_mapping_result_failure(self):
        """Test mapping result for failed mapping."""
        result = StandardMappingResult(
            success=False,
            source_standard=StandardType.CVE,
            errors=("Invalid CVE",),
        )
        assert not result.success
        assert len(result.errors) == 1


class TestStixModule:
    """Test STIX module."""
    
    def test_stix_validator_valid_object(self):
        """Test STIX validator with valid object."""
        from cyber.standards.stix.validators import StixValidator
        
        obj = {
            "type": "indicator",
            "id": "indicator--c410e480-e42b-47d1-9476-85307c12bcbf",
            "created": "2024-01-01T00:00:00Z",
            "modified": "2024-01-01T00:00:00Z",
        }
        
        result = StixValidator.validate_object(obj)
        assert result.is_valid
    
    def test_stix_validator_missing_required(self):
        """Test STIX validator with missing required fields."""
        from cyber.standards.stix.validators import StixValidator
        
        obj = {
            "type": "indicator",
        }
        
        result = StixValidator.validate_object(obj)
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_stix_mapper_to_fool_domain(self):
        """Test STIX mapper to FOOL domain."""
        from cyber.standards.stix.mappers import StixMapper
        
        stix_obj = {
            "type": "malware",
            "id": "malware--c410e480-e42b-47d1-9476-85307c12bcbf",
            "name": "Emotet",
            "description": "Banking trojan",
        }
        
        result = StixMapper.to_fool_domain(stix_obj)
        assert result.success
        assert result.target_type == "malware"
        assert result.mapped_object["name"] == "Emotet"
    
    def test_stix_serializer_serialize(self):
        """Test STIX serializer."""
        from cyber.standards.stix.serializers import StixSerializer
        
        obj = {"type": "indicator", "id": "test"}
        json_str = StixSerializer.serialize(obj)
        assert '"type": "indicator"' in json_str


class TestAttackModule:
    """Test ATT&CK module."""
    
    def test_attack_validator_valid_technique(self):
        """Test ATT&CK validator with valid technique."""
        from cyber.standards.attack.validators import AttackValidator
        
        technique = {
            "id": "T1566",
            "name": "Phishing",
        }
        
        result = AttackValidator.validate_technique(technique)
        assert result.is_valid
    
    def test_attack_mapper_to_fool_domain(self):
        """Test ATT&CK mapper to FOOL domain."""
        from cyber.standards.attack.mappers import AttackMapper
        
        attack_obj = {
            "id": "T1566",
            "name": "Phishing",
            "description": "Phishing attack",
        }
        
        result = AttackMapper.to_fool_domain(attack_obj)
        assert result.success
        assert result.target_type == "technique"


class TestCveModule:
    """Test CVE module."""
    
    def test_cve_validator_valid(self):
        """Test CVE validator with valid CVE."""
        from cyber.standards.cve.validators import CveValidator
        
        cve = {
            "cve_id": "CVE-2024-1234",
            "description": "Test vulnerability",
        }
        
        result = CveValidator.validate(cve)
        assert result.is_valid
    
    def test_cve_validator_invalid(self):
        """Test CVE validator with invalid CVE."""
        from cyber.standards.cve.validators import CveValidator
        
        cve = {
            "cve_id": "INVALID",
        }
        
        result = CveValidator.validate(cve)
        assert not result.is_valid
    
    def test_cve_mapper_to_fool_domain(self):
        """Test CVE mapper to FOOL domain."""
        from cyber.standards.cve.mappers import CveMapper
        
        cve = {
            "cve_id": "CVE-2024-1234",
            "description": "Buffer overflow",
            "severity": "HIGH",
            "cvss_score": 7.5,
        }
        
        result = CveMapper.to_fool_domain(cve)
        assert result.success
        assert result.target_type == "vulnerability"


class TestCweModule:
    """Test CWE module."""
    
    def test_cwe_validator_valid(self):
        """Test CWE validator."""
        from cyber.standards.cwe.validators import CweValidator
        
        cwe = {
            "cwe_id": "CWE-79",
            "name": "Cross-site Scripting",
        }
        
        result = CweValidator.validate(cwe)
        assert result.is_valid


class TestCapecModule:
    """Test CAPEC module."""
    
    def test_capec_validator_valid(self):
        """Test CAPEC validator."""
        from cyber.standards.capec.validators import CapecValidator
        
        capec = {
            "capec_id": "CAPEC-1",
            "name": "Buffer Overflow",
        }
        
        result = CapecValidator.validate(capec)
        assert result.is_valid


class TestSigmaModule:
    """Test Sigma module."""
    
    def test_sigma_validator_valid(self):
        """Test Sigma validator."""
        from cyber.standards.sigma.validators import SigmaValidator
        
        rule = {
            "title": "Suspicious Process",
            "detection": {"selection": {"CommandLine": "*evil*"}},
        }
        
        result = SigmaValidator.validate(rule)
        assert result.is_valid
    
    def test_sigma_mapper_to_fool_domain(self):
        """Test Sigma mapper to FOOL domain."""
        from cyber.standards.sigma.mappers import SigmaMapper
        
        rule = {
            "id": "sigma-1",
            "title": "Suspicious Process",
            "description": "Detects suspicious process",
            "level": "high",
        }
        
        result = SigmaMapper.to_fool_domain(rule)
        assert result.success
        assert result.target_type == "detection_rule"


class TestYaraModule:
    """Test YARA module."""
    
    def test_yara_validator_valid(self):
        """Test YARA validator."""
        from cyber.standards.yara.validators import YaraValidator
        
        rule = {
            "rule_name": "test_rule",
            "condition": "true",
        }
        
        result = YaraValidator.validate(rule)
        assert result.is_valid


class TestOpenIOCModule:
    """Test OpenIOC module."""
    
    def test_openioc_validator_valid(self):
        """Test OpenIOC validator."""
        from cyber.standards.openioc.validators import OpenIOCValidator
        
        ioc = {
            "ioc_id": "ioc-1",
            "name": "Malicious IP",
        }
        
        result = OpenIOCValidator.validate(ioc)
        assert result.is_valid


class TestRegistry:
    """Test standard registry."""
    
    def test_registry_creation(self):
        """Test registry creation."""
        registry = CyberStandardRegistry()
        assert len(registry.list_standards()) > 0
    
    def test_registry_has_stix(self):
        """Test registry has STIX."""
        registry = CyberStandardRegistry()
        stix_info = registry.get_standard(StandardType.STIX)
        assert stix_info is not None
        assert stix_info.name == "STIX 2.x"
    
    def test_registry_supports_standard(self):
        """Test registry supports standard."""
        registry = CyberStandardRegistry()
        assert registry.supports_standard(StandardType.STIX)
        assert registry.supports_standard(StandardType.ATTACK)
        assert registry.supports_standard(StandardType.CVE)
    
    def test_registry_supports_version(self):
        """Test registry supports version."""
        registry = CyberStandardRegistry()
        assert registry.supports_version(StandardType.STIX, "2.1")
        assert not registry.supports_version(StandardType.STIX, "3.0")


class TestServices:
    """Test services."""
    
    def test_validation_service_stix(self):
        """Test validation service for STIX."""
        service = ValidationService()
        
        obj = {
            "type": "indicator",
            "id": "indicator--c410e480-e42b-47d1-9476-85307c12bcbf",
            "created": "2024-01-01T00:00:00Z",
            "modified": "2024-01-01T00:00:00Z",
        }
        
        result = service.validate(StandardType.STIX, obj)
        assert result.is_valid
    
    def test_validation_service_cve(self):
        """Test validation service for CVE."""
        service = ValidationService()
        
        obj = {
            "cve_id": "CVE-2024-1234",
        }
        
        result = service.validate(StandardType.CVE, obj)
        assert result.is_valid
    
    def test_mapping_service_stix(self):
        """Test mapping service for STIX."""
        service = MappingService()
        
        obj = {
            "type": "malware",
            "id": "malware--test",
            "name": "Test",
        }
        
        result = service.to_fool_domain(StandardType.STIX, obj)
        assert result.success
    
    def test_serialization_service(self):
        """Test serialization service."""
        service = SerializationService()
        
        obj = {"type": "test", "id": "123"}
        json_str = service.serialize(StandardType.STIX, obj)
        assert "test" in json_str
        
        deserialized = service.deserialize(StandardType.STIX, json_str)
        assert deserialized["type"] == "test"


class TestEvents:
    """Test event integration."""
    
    def test_event_emitter_creation(self):
        """Test event emitter creation."""
        emitter = CyberStandardEventEmitter()
        assert emitter is not None
    
    def test_emit_loaded(self):
        """Test emit loaded event."""
        emitter = CyberStandardEventEmitter()
        emitter.emit_loaded("stix", "2.1")
        
        events = emitter.get_events()
        assert len(events) == 1
        assert events[0].event_type == CyberStandardEventType.LOADED
    
    def test_emit_validated(self):
        """Test emit validated event."""
        emitter = CyberStandardEventEmitter()
        emitter.emit_validated("stix", True)
        
        events = emitter.get_events()
        assert len(events) == 1
        assert events[0].event_type == CyberStandardEventType.VALIDATED
    
    def test_emit_mapping_created(self):
        """Test emit mapping created event."""
        emitter = CyberStandardEventEmitter()
        emitter.emit_mapping_created("stix", "src-1", "tgt-1")
        
        events = emitter.get_events()
        assert len(events) == 1
        assert events[0].event_type == CyberStandardEventType.MAPPING_CREATED
    
    def test_emit_mapping_failed(self):
        """Test emit mapping failed event."""
        emitter = CyberStandardEventEmitter()
        emitter.emit_mapping_failed("stix", "src-1", "Error")
        
        events = emitter.get_events()
        assert len(events) == 1
        assert events[0].event_type == CyberStandardEventType.MAPPING_FAILED
    
    def test_disable_events(self):
        """Test disabling events."""
        emitter = CyberStandardEventEmitter()
        emitter.disable()
        emitter.emit_loaded("stix", "2.1")
        
        events = emitter.get_events()
        assert len(events) == 0
    
    def test_clear_events(self):
        """Test clearing events."""
        emitter = CyberStandardEventEmitter()
        emitter.emit_loaded("stix", "2.1")
        emitter.emit_loaded("attack", "13.0")
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_intelligence_imports(self):
        """Test that standards does not import intelligence."""
        import cyber.standards.models
        import cyber.standards.registry
        import cyber.standards.services
        import cyber.standards.events
        
        source_files = [
            cyber.standards.models.__file__,
            cyber.standards.registry.__file__,
            cyber.standards.services.__file__,
            cyber.standards.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from intelligence" not in content
            assert "import intelligence" not in content
    
    def test_no_ai_imports(self):
        """Test that standards does not import AI."""
        import cyber.standards.models
        import cyber.standards.registry
        import cyber.standards.services
        import cyber.standards.events
        
        source_files = [
            cyber.standards.models.__file__,
            cyber.standards.registry.__file__,
            cyber.standards.services.__file__,
            cyber.standards.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_connector_imports(self):
        """Test that standards does not import connectors."""
        import cyber.standards.models
        import cyber.standards.registry
        import cyber.standards.services
        import cyber.standards.events
        
        source_files = [
            cyber.standards.models.__file__,
            cyber.standards.registry.__file__,
            cyber.standards.services.__file__,
            cyber.standards.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_detection_imports(self):
        """Test that standards does not import detection."""
        import cyber.standards.models
        import cyber.standards.registry
        import cyber.standards.services
        import cyber.standards.events
        
        source_files = [
            cyber.standards.models.__file__,
            cyber.standards.registry.__file__,
            cyber.standards.services.__file__,
            cyber.standards.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('"""'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "detection" not in line.lower()
