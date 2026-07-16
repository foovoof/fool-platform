"""
threat_intelligence/infrastructure/tests/test_infrastructure.py

Tests for Infrastructure Intelligence Module.
"""
import pytest

from threat_intelligence.infrastructure.models import (
    Infrastructure,
    InfrastructureIdentity,
    InfrastructureAlias,
    InfrastructureAssertion,
    InfrastructureEvidence,
    InfrastructureRelationship,
    InfrastructureVersion,
    InfrastructureHistory,
)

from threat_intelligence.infrastructure.models.enums import (
    InfrastructureType,
    InfrastructureRole,
    InfrastructureStatus,
    AssertionStatus,
    AssertionType,
)

from threat_intelligence.infrastructure.taxonomy import (
    InfrastructureTypeRegistry,
    InfrastructureRoleRegistry,
    RelationshipRegistry,
)

from threat_intelligence.infrastructure.service import InfrastructureService

from threat_intelligence.infrastructure.lifecycle import InfrastructureLifecycleService

from threat_intelligence.infrastructure.validation import (
    InfrastructureValidator,
    ValidationResult,
    LifecycleValidator,
)

from threat_intelligence.infrastructure.events import (
    InfrastructureEventEmitter,
    InfrastructureEventType,
)

from threat_intelligence.infrastructure.queries import InfrastructureQueryService


class TestInfrastructureModel:
    """Test Infrastructure model."""
    
    def test_create_infrastructure(self):
        """Test creating infrastructure."""
        infra = Infrastructure(
            name="C2 Server",
            infrastructure_type=InfrastructureType.IP_ADDRESS.value,
            value="1.2.3.4",
            role=InfrastructureRole.COMMAND_CONTROL.value,
        )
        
        assert infra.name == "C2 Server"
        assert infra.infrastructure_type == "ip_address"
        assert infra.value == "1.2.3.4"
        assert infra.id is not None
    
    def test_infrastructure_to_dict(self):
        """Test infrastructure serialization."""
        infra = Infrastructure(
            name="Test Infra",
            infrastructure_type=InfrastructureType.DOMAIN.value,
            value="test.com",
        )
        
        data = infra.to_dict()
        assert data["name"] == "Test Infra"
        assert data["infrastructure_type"] == "domain"


class TestInfrastructureIdentity:
    """Test InfrastructureIdentity model."""
    
    def test_create_identity(self):
        """Test creating identity."""
        identity = InfrastructureIdentity(
            infrastructure_id="infra-1",
            identity_type="domain",
            value="evil.com",
        )
        
        assert identity.infrastructure_id == "infra-1"
        assert identity.identity_type == "domain"


class TestInfrastructureAssertion:
    """Test InfrastructureAssertion model."""
    
    def test_create_assertion(self):
        """Test creating assertion."""
        assertion = InfrastructureAssertion(
            infrastructure_id="infra-1",
            assertion_type=AssertionType.HOSTING.value,
            assertion="Infrastructure hosts malware",
            status=AssertionStatus.PENDING.value,
        )
        
        assert assertion.infrastructure_id == "infra-1"
        assert assertion.status == "pending"


class TestInfrastructureEvidence:
    """Test InfrastructureEvidence model."""
    
    def test_create_evidence(self):
        """Test creating evidence."""
        evidence = InfrastructureEvidence(
            infrastructure_id="infra-1",
            evidence_type="direct",
            title="DNS Query Log",
            description="DNS query evidence",
        )
        
        assert evidence.infrastructure_id == "infra-1"
        assert evidence.evidence_type == "direct"


class TestInfrastructureRelationship:
    """Test InfrastructureRelationship model."""
    
    def test_create_relationship(self):
        """Test creating relationship."""
        relationship = InfrastructureRelationship(
            infrastructure_id="infra-1",
            source_type="infrastructure",
            source_id="infra-1",
            target_type="malware",
            target_id="malware-1",
            relationship_type="hosts",
        )
        
        assert relationship.infrastructure_id == "infra-1"
        assert relationship.relationship_type == "hosts"


class TestInfrastructureService:
    """Test InfrastructureService."""
    
    def test_create(self):
        """Test creating infrastructure."""
        service = InfrastructureService()
        
        infra = service.create(
            name="C2 Server",
            infrastructure_type="ip_address",
            value="1.2.3.4",
            author="test",
        )
        
        assert infra.name == "C2 Server"
        assert infra.author == "test"
    
    def test_get(self):
        """Test getting infrastructure."""
        service = InfrastructureService()
        
        created = service.create(
            name="Test",
            infrastructure_type="domain",
            value="test.com",
        )
        
        retrieved = service.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_search(self):
        """Test searching infrastructure."""
        service = InfrastructureService()
        
        infra1 = service.create(
            name="IP 1",
            infrastructure_type="ip_address",
            value="1.1.1.1",
        )
        
        infra2 = service.create(
            name="Domain 1",
            infrastructure_type="domain",
            value="test.com",
        )
        
        # Test that search returns created infrastructure
        results_ip = service.find_by_type("ip_address")
        assert any(r.id == infra1.id for r in results_ip)
        
        results_domain = service.find_by_type("domain")
        assert any(r.id == infra2.id for r in results_domain)
        
        # Clean up
        service.delete(infra1.id)
        service.delete(infra2.id)
    
    def test_find_by_status(self):
        """Test finding by status."""
        service = InfrastructureService()
        
        service.create(
            name="Active",
            infrastructure_type="ip_address",
            value="1.1.1.1",
            status="active",
        )
        
        results = service.find_by_status("active")
        assert len(results) >= 1


class TestLifecycleService:
    """Test LifecycleService."""
    
    def test_lifecycle_transitions(self):
        """Test lifecycle transitions."""
        service = InfrastructureLifecycleService()
        
        success, msg = service.transition(
            "infra-1",
            "observed",
            reason="Starting observation",
            transitioned_by="user",
        )
        
        assert success
        
        status = service.get_status("infra-1")
        assert status == "observed"
    
    def test_valid_transitions(self):
        """Test valid transitions."""
        service = InfrastructureLifecycleService()
        
        assert service.can_transition("draft", "observed")
        assert service.can_transition("observed", "validated")
        assert service.can_transition("validated", "published")
        assert service.can_transition("published", "active")
        
        assert not service.can_transition("draft", "active")
        assert not service.can_transition("archived", "draft")


class TestLifecycleValidator:
    """Test LifecycleValidator."""
    
    def test_can_transition(self):
        """Test transition validation."""
        assert LifecycleValidator.can_transition("draft", "observed")
        assert LifecycleValidator.can_transition("observed", "validated")
        assert not LifecycleValidator.can_transition("archived", "draft")
        assert LifecycleValidator.can_transition("deprecated", "active")


class TestValidation:
    """Test validation."""
    
    def test_valid_infrastructure(self):
        """Test valid infrastructure."""
        infra = Infrastructure(
            name="Test",
            infrastructure_type="ip_address",
            value="1.2.3.4",
        )
        
        result = InfrastructureValidator.validate(infra)
        assert result.is_valid
    
    def test_invalid_infrastructure(self):
        """Test invalid infrastructure."""
        infra = Infrastructure(
            name="",
            infrastructure_type="ip_address",
            value="1.2.3.4",
        )
        
        result = InfrastructureValidator.validate(infra)
        assert not result.is_valid
        assert len(result.issues) > 0


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = InfrastructureEventEmitter()
        
        emitter.emit_created("infra-1")
        emitter.emit_updated("infra-1")
        emitter.emit_assertion_created("infra-1", "assertion-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestQueryService:
    """Test query service."""
    
    def test_query_service(self):
        """Test query service."""
        service = InfrastructureQueryService()
        
        results = service.find_by_type("ip_address")
        assert isinstance(results, list)
        
        results = service.find_by_status("active")
        assert isinstance(results, list)


class TestTaxonomyRegistries:
    """Test taxonomy registries."""
    
    def test_infrastructure_type_registry(self):
        """Test infrastructure type registry."""
        types = InfrastructureTypeRegistry.get_types()
        assert "ip_address" in types
        assert "domain" in types
        assert "server" in types
    
    def test_infrastructure_role_registry(self):
        """Test infrastructure role registry."""
        roles = InfrastructureRoleRegistry.get_roles()
        assert "command_control" in roles
        assert "delivery" in roles
    
    def test_relationship_registry(self):
        """Test relationship registry."""
        rels = RelationshipRegistry.get_relationships()
        assert "hosts" in rels
        assert "used_by" in rels


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import threat_intelligence.infrastructure.models
        import threat_intelligence.infrastructure.service
        import threat_intelligence.infrastructure.validation
        import threat_intelligence.infrastructure.queries
        import threat_intelligence.infrastructure.events
        import threat_intelligence.infrastructure.taxonomy
        
        source_files = [
            threat_intelligence.infrastructure.models.__file__,
            threat_intelligence.infrastructure.service.__file__,
            threat_intelligence.infrastructure.validation.__file__,
            threat_intelligence.infrastructure.queries.__file__,
            threat_intelligence.infrastructure.events.__file__,
            threat_intelligence.infrastructure.taxonomy.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_connector_imports(self):
        """Test no connector imports."""
        import threat_intelligence.infrastructure.models
        import threat_intelligence.infrastructure.service
        
        source_files = [
            threat_intelligence.infrastructure.models.__file__,
            threat_intelligence.infrastructure.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_network_operations(self):
        """Test no network operations."""
        import threat_intelligence.infrastructure.models
        import threat_intelligence.infrastructure.service
        
        source_files = [
            threat_intelligence.infrastructure.models.__file__,
            threat_intelligence.infrastructure.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "socket" not in content.lower()
            assert "requests" not in content.lower()
            assert "urllib" not in content.lower()
            assert "http.client" not in content.lower()
            assert "dns.resolver" not in content.lower()
