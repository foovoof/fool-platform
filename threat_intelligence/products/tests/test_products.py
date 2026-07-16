"""
threat_intelligence/products/tests/test_products.py

Tests for Intelligence Products Module.
"""
import pytest

from threat_intelligence.products.models import (
    IntelligenceProduct,
    ThreatReport,
    TechnicalReport,
    StrategicReport,
    ProductAssertion,
    ProductEvidence,
    ProductConfidence,
)

from threat_intelligence.products.models.enums import (
    ProductType,
    ProductStatus,
    ClassificationLevel,
)

from threat_intelligence.products.registries import (
    ProductTypeRegistry,
    ClassificationRegistry,
    LifecycleRegistry,
    RelationshipRegistry,
    VersionRegistry,
)

from threat_intelligence.products.service import ProductService, LifecycleService

from threat_intelligence.products.validation import (
    ProductValidator,
    LifecycleValidator,
    ReferenceValidator,
    ValidationResult,
)

from threat_intelligence.products.events import (
    ProductEventEmitter,
    ProductEventType,
)

from threat_intelligence.products.queries import ProductQueryService


class TestProductModel:
    """Test IntelligenceProduct model."""
    
    def test_create_product(self):
        """Test creating product."""
        product = IntelligenceProduct(
            name="Threat Report Q1",
            product_type=ProductType.THREAT_REPORT.value,
            title="Q1 2024 Threat Report",
            description="Quarterly threat analysis",
            author="analyst",
        )
        
        assert product.name == "Threat Report Q1"
        assert product.product_type == "threat_report"
        assert product.id is not None
    
    def test_product_to_dict(self):
        """Test product serialization."""
        product = IntelligenceProduct(
            name="Test Report",
            product_type="technical_report",
            title="Test Title",
        )
        
        data = product.to_dict()
        assert data["name"] == "Test Report"
        assert data["product_type"] == "technical_report"


class TestThreatReport:
    """Test ThreatReport model."""
    
    def test_create_threat_report(self):
        """Test creating threat report."""
        report = ThreatReport(
            product_id="prod-1",
            report_type="threat_report",
            title="APT29 Analysis",
            executive_summary="APT29 continues to operate",
            threat_actor_refs=("actor-1",),
            malware_refs=("malware-1",),
        )
        
        assert report.product_id == "prod-1"
        assert report.title == "APT29 Analysis"


class TestTechnicalReport:
    """Test TechnicalReport model."""
    
    def test_create_technical_report(self):
        """Test creating technical report."""
        report = TechnicalReport(
            product_id="prod-1",
            title="Malware Technical Analysis",
            technical_summary="Detailed technical findings",
            indicator_refs=("ioc-1",),
            malware_refs=("malware-1",),
        )
        
        assert report.product_id == "prod-1"
        assert "ioc-1" in report.indicator_refs


class TestStrategicReport:
    """Test StrategicReport model."""
    
    def test_create_strategic_report(self):
        """Test creating strategic report."""
        report = StrategicReport(
            product_id="prod-1",
            title="Annual Threat Landscape",
            strategic_summary="Yearly threat overview",
            risk_assessment="Elevated risk",
            trend_analysis="Increasing sophistication",
        )
        
        assert report.product_id == "prod-1"
        assert report.risk_assessment == "Elevated risk"


class TestProductAssertion:
    """Test ProductAssertion model."""
    
    def test_create_assertion(self):
        """Test creating assertion."""
        assertion = ProductAssertion(
            product_id="prod-1",
            assertion_type="finding",
            assertion="APT29 targets financial institutions",
            status="confirmed",
        )
        
        assert assertion.product_id == "prod-1"
        assert assertion.assertion_type == "finding"
        assert assertion.status == "confirmed"


class TestProductEvidence:
    """Test ProductEvidence model."""
    
    def test_create_evidence(self):
        """Test creating evidence."""
        evidence = ProductEvidence(
            product_id="prod-1",
            assertion_id="assertion-1",
            evidence_type="log",
            title="Access Log Evidence",
            description="Server access log showing malicious activity",
        )
        
        assert evidence.product_id == "prod-1"
        assert evidence.evidence_type == "log"


class TestProductConfidence:
    """Test ProductConfidence model."""
    
    def test_create_confidence(self):
        """Test creating confidence binding."""
        confidence = ProductConfidence(
            product_id="prod-1",
            confidence_level="high",
            confidence_score=0.85,
            confidence_explanation="Based on multiple sources",
            evidence_refs=("evidence-1", "evidence-2"),
        )
        
        assert confidence.product_id == "prod-1"
        assert confidence.confidence_score == 0.85


class TestProductService:
    """Test ProductService."""
    
    def test_create(self):
        """Test creating product."""
        service = ProductService()
        
        product = service.create(
            name="Test Report",
            product_type="threat_report",
            title="Test Title",
            author="test",
        )
        
        assert product.name == "Test Report"
        assert product.author == "test"
    
    def test_get(self):
        """Test getting product."""
        service = ProductService()
        
        created = service.create(
            name="Test",
            product_type="technical_report",
            title="Test Title",
        )
        
        retrieved = service.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_search(self):
        """Test searching product."""
        service = ProductService()
        
        prod1 = service.create(
            name="Report 1",
            product_type="threat_report",
            title="Report 1",
            status="draft",
        )
        
        prod2 = service.create(
            name="Report 2",
            product_type="technical_report",
            title="Report 2",
            status="published",
        )
        
        results = service.find_by_type("threat_report")
        assert any(r.id == prod1.id for r in results)
        
        # Clean up
        service.delete(prod1.id)
        service.delete(prod2.id)
    
    def test_find_by_status(self):
        """Test finding by status."""
        service = ProductService()
        
        product = service.create(
            name="Published Report",
            product_type="strategic_report",
            title="Published",
            status="published",
        )
        
        results = service.find_by_status("published")
        assert any(r.id == product.id for r in results)
        
        service.delete(product.id)


class TestLifecycleService:
    """Test LifecycleService."""
    
    def test_lifecycle_transitions(self):
        """Test lifecycle transitions."""
        service = LifecycleService()
        
        success, msg = service.transition(
            "prod-1",
            "under_review",
            reason="Ready for review",
            transitioned_by="user",
        )
        
        assert success
        
        status = service.get_status("prod-1")
        assert status == "under_review"
    
    def test_valid_transitions(self):
        """Test valid transitions."""
        service = LifecycleService()
        
        assert service.can_transition("draft", "under_review")
        assert service.can_transition("under_review", "validated")
        assert service.can_transition("validated", "approved")
        assert service.can_transition("approved", "published")
        
        assert not service.can_transition("draft", "published")
        assert not service.can_transition("archived", "draft")


class TestLifecycleValidator:
    """Test LifecycleValidator."""
    
    def test_can_transition(self):
        """Test transition validation."""
        assert LifecycleValidator.can_transition("draft", "under_review")
        assert LifecycleValidator.can_transition("validated", "approved")
        assert LifecycleValidator.can_transition("approved", "published")


class TestValidation:
    """Test validation."""
    
    def test_valid_product(self):
        """Test valid product."""
        product = IntelligenceProduct(
            name="Valid Report",
            product_type="threat_report",
            title="Valid Title",
        )
        
        result = ProductValidator.validate(product)
        assert result.is_valid
    
    def test_invalid_product(self):
        """Test invalid product."""
        product = IntelligenceProduct(
            name="",
            product_type="threat_report",
            title="Valid Title",
        )
        
        result = ProductValidator.validate(product)
        assert not result.is_valid
        assert len(result.issues) > 0


class TestReferenceValidator:
    """Test ReferenceValidator."""
    
    def test_validate_references(self):
        """Test validating references."""
        product = IntelligenceProduct(
            name="Test",
            product_type="threat_report",
            title="Test",
            indicator_refs=("ioc-1", "ioc-2"),
            actor_refs=("actor-1",),
        )
        
        result = ReferenceValidator.validate_references(product)
        assert result.is_valid


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = ProductEventEmitter()
        
        emitter.emit_created("prod-1")
        emitter.emit_updated("prod-1")
        emitter.emit_published("prod-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestQueryService:
    """Test query service."""
    
    def test_query_service(self):
        """Test query service."""
        service = ProductQueryService()
        
        results = service.find_by_type("threat_report")
        assert isinstance(results, list)
        
        results = service.find_by_status("published")
        assert isinstance(results, list)
    
    def test_find_published(self):
        """Test finding published products."""
        service = ProductQueryService()
        
        results = service.find_published()
        assert isinstance(results, list)
    
    def test_find_by_author(self):
        """Test finding by author."""
        service = ProductQueryService()
        
        results = service.find_by_author("analyst")
        assert isinstance(results, list)


class TestRegistries:
    """Test registries."""
    
    def test_product_type_registry(self):
        """Test product type registry."""
        types = ProductTypeRegistry.get_types()
        assert "threat_report" in types
        assert "technical_report" in types
        assert "strategic_report" in types
    
    def test_classification_registry(self):
        """Test classification registry."""
        levels = ClassificationRegistry.get_levels()
        assert "unclassified" in levels
        assert "confidential" in levels
        assert "secret" in levels
    
    def test_lifecycle_registry(self):
        """Test lifecycle registry."""
        states = LifecycleRegistry.get_states()
        assert "draft" in states
        assert "published" in states
        
        transitions = LifecycleRegistry.get_valid_transitions()
        assert "draft" in transitions
        assert "published" in transitions
    
    def test_relationship_registry(self):
        """Test relationship registry."""
        rels = RelationshipRegistry.get_relationships()
        assert "supersedes" in rels
        assert "superseded_by" in rels
        assert "related_to" in rels
    
    def test_version_registry(self):
        """Test version registry."""
        components = VersionRegistry.get_components()
        assert "major" in components
        assert "minor" in components
        assert "patch" in components
        
        version = VersionRegistry.parse_version("1.2.3")
        assert version == (1, 2, 3)


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import threat_intelligence.products.models
        import threat_intelligence.products.service
        import threat_intelligence.products.validation
        import threat_intelligence.products.queries
        import threat_intelligence.products.events
        
        source_files = [
            threat_intelligence.products.models.__file__,
            threat_intelligence.products.service.__file__,
            threat_intelligence.products.validation.__file__,
            threat_intelligence.products.queries.__file__,
            threat_intelligence.products.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_connector_imports(self):
        """Test no connector imports."""
        import threat_intelligence.products.models
        import threat_intelligence.products.service
        
        source_files = [
            threat_intelligence.products.models.__file__,
            threat_intelligence.products.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_exchange_imports(self):
        """Test no exchange imports."""
        import threat_intelligence.products.models
        import threat_intelligence.products.service
        
        source_files = [
            threat_intelligence.products.models.__file__,
            threat_intelligence.products.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from exchange" not in content
            assert "import exchange" not in content
            assert "taxii" not in content.lower()
            assert "stix" not in content.lower()
    
    def test_no_rendering_imports(self):
        """Test no rendering imports."""
        import threat_intelligence.products.models
        import threat_intelligence.products.service
        
        source_files = [
            threat_intelligence.products.models.__file__,
            threat_intelligence.products.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "markdown" not in content.lower()
            assert "jinja" not in content.lower()
            assert "pdfkit" not in content.lower()
            assert "weasyprint" not in content.lower()
