"""
workbench/tests/test_workbench.py

Tests for Threat Intelligence Workbench Module.
"""
import pytest

from workbench.models import (
    IntelligenceProduct,
    IntelligenceCollection,
    AssertionReference,
    EvidencePackageReference,
    KnowledgeReference,
    Reviewer,
    ReviewCycle,
    ApprovalRecord,
    Publication,
    SourceAssessment,
    ConfidenceReview,
    GovernanceDecision,
)

from workbench.models.enums import (
    ProductLifecycleStatus,
    ReviewStatus,
    ApprovalStatus,
)

from workbench.runtime import (
    ProductManager,
    CollectionManager,
    ReviewManager,
    ApprovalManager,
    PublicationManager,
    GovernanceManager,
)

from workbench.events import (
    WorkbenchEventEmitter,
    WorkbenchEventType,
)


class TestIntelligenceProductModel:
    """Test IntelligenceProduct model."""
    
    def test_create_product(self):
        """Test creating product."""
        product = IntelligenceProduct(
            product_type="threat_report",
            title="APT29 Analysis",
            description="Analysis of APT29 activity",
            owner="analyst-1",
            status="draft",
        )
        
        assert product.product_type == "threat_report"
        assert product.title == "APT29 Analysis"
        assert product.status == "draft"
        assert product.id is not None
    
    def test_product_to_dict(self):
        """Test product serialization."""
        product = IntelligenceProduct(
            product_type="technical_report",
            title="Test Report",
            description="Test description",
            owner="test",
        )
        
        data = product.to_dict()
        assert data["product_type"] == "technical_report"
        assert data["title"] == "Test Report"
        assert data["status"] == "draft"


class TestIntelligenceCollectionModel:
    """Test IntelligenceCollection model."""
    
    def test_create_collection(self):
        """Test creating collection."""
        collection = IntelligenceCollection(
            name="APT Collection",
            description="Collection of APT-related products",
            owner="analyst-1",
        )
        
        assert collection.name == "APT Collection"
        assert collection.status == "active"


class TestReferenceModels:
    """Test reference models."""
    
    def test_create_assertion_reference(self):
        """Test creating assertion reference."""
        ref = AssertionReference(
            product_id="prod-1",
            assertion_ref="assertion-123",
            source_system="cti_platform",
        )
        
        assert ref.product_id == "prod-1"
        assert ref.assertion_ref == "assertion-123"
        assert ref.source_system == "cti_platform"
    
    def test_create_evidence_reference(self):
        """Test creating evidence reference."""
        ref = EvidencePackageReference(
            product_id="prod-1",
            evidence_ref="evidence-456",
            source_system="evidence_platform",
        )
        
        assert ref.product_id == "prod-1"
        assert ref.evidence_ref == "evidence-456"
        assert ref.source_system == "evidence_platform"
    
    def test_create_knowledge_reference(self):
        """Test creating knowledge reference."""
        ref = KnowledgeReference(
            product_id="prod-1",
            knowledge_ref="entity-789",
            source_system="knowledge_graph",
        )
        
        assert ref.product_id == "prod-1"
        assert ref.knowledge_ref == "entity-789"
        assert ref.source_system == "knowledge_graph"


class TestReviewerModel:
    """Test Reviewer model."""
    
    def test_create_reviewer(self):
        """Test creating reviewer."""
        reviewer = Reviewer(
            user_id="user-1",
            name="John Doe",
            email="john@example.com",
            role="senior_analyst",
        )
        
        assert reviewer.user_id == "user-1"
        assert reviewer.name == "John Doe"


class TestReviewCycleModel:
    """Test ReviewCycle model."""
    
    def test_create_review_cycle(self):
        """Test creating review cycle."""
        reviewer = Reviewer(
            user_id="user-1",
            name="John Doe",
            role="reviewer",
        )
        
        review = ReviewCycle(
            product_id="prod-1",
            status="pending",
            reviewers=(reviewer,),
        )
        
        assert review.product_id == "prod-1"
        assert review.status == "pending"


class TestApprovalRecordModel:
    """Test ApprovalRecord model."""
    
    def test_create_approval_record(self):
        """Test creating approval record."""
        approval = ApprovalRecord(
            product_id="prod-1",
            approval_type="final_approval",
            status="pending",
        )
        
        assert approval.product_id == "prod-1"
        assert approval.status == "pending"


class TestPublicationModel:
    """Test Publication model."""
    
    def test_create_publication(self):
        """Test creating publication."""
        publication = Publication(
            product_id="prod-1",
            status="draft",
        )
        
        assert publication.product_id == "prod-1"
        assert publication.status == "draft"


class TestSourceAssessmentModel:
    """Test SourceAssessment model."""
    
    def test_create_source_assessment(self):
        """Test creating source assessment."""
        assessor = Reviewer(
            user_id="user-1",
            name="John Doe",
            role="assessor",
        )
        
        assessment = SourceAssessment(
            source_id="source-1",
            source_name="External Feed",
            reliability="b",
            assessor=assessor,
        )
        
        assert assessment.source_id == "source-1"
        assert assessment.reliability == "b"


class TestConfidenceReviewModel:
    """Test ConfidenceReview model."""
    
    def test_create_confidence_review(self):
        """Test creating confidence review."""
        reviewer = Reviewer(
            user_id="user-1",
            name="John Doe",
            role="reviewer",
        )
        
        review = ConfidenceReview(
            product_id="prod-1",
            assertion_id="assertion-1",
            confidence_level="high",
            reviewer=reviewer,
        )
        
        assert review.confidence_level == "high"


class TestGovernanceDecisionModel:
    """Test GovernanceDecision model."""
    
    def test_create_decision(self):
        """Test creating governance decision."""
        decision_maker = Reviewer(
            user_id="user-1",
            name="John Doe",
            role="decision_maker",
        )
        
        decision = GovernanceDecision(
            product_id="prod-1",
            decision_type="publish",
            decision="approved",
            decision_made_by=decision_maker,
        )
        
        assert decision.decision == "approved"


class TestProductManager:
    """Test ProductManager."""
    
    def test_create_product(self):
        """Test creating product."""
        manager = ProductManager()
        
        product = manager.create(
            product_type="threat_report",
            title="Test Report",
            owner="analyst-1",
            description="Test description",
        )
        
        assert product.title == "Test Report"
        assert product.status == "draft"
    
    def test_get_product(self):
        """Test getting product."""
        manager = ProductManager()
        
        created = manager.create(
            product_type="threat_report",
            title="Test",
            owner="analyst",
        )
        
        retrieved = manager.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_transition_status(self):
        """Test status transition."""
        manager = ProductManager()
        
        product = manager.create(
            product_type="threat_report",
            title="Test",
            owner="analyst",
        )
        
        updated = manager.transition_status(
            product.id,
            "in_review",
            reason="Ready for review",
            actor="analyst",
        )
        
        assert updated is not None
        assert updated.status == "in_review"
    
    def test_attach_assertion_reference(self):
        """Test attaching assertion reference."""
        manager = ProductManager()
        
        product = manager.create(
            product_type="threat_report",
            title="Test",
            owner="analyst",
        )
        
        updated = manager.attach_assertion(
            product.id,
            "assertion-123",
            "cti_platform",
        )
        
        assert updated is not None
        assert len(updated.assertion_refs) == 1
        assert updated.assertion_refs[0].assertion_ref == "assertion-123"
    
    def test_attach_evidence_reference(self):
        """Test attaching evidence reference."""
        manager = ProductManager()
        
        product = manager.create(
            product_type="threat_report",
            title="Test",
            owner="analyst",
        )
        
        updated = manager.attach_evidence(
            product.id,
            "evidence-456",
            "evidence_platform",
        )
        
        assert updated is not None
        assert len(updated.evidence_refs) == 1
        assert updated.evidence_refs[0].evidence_ref == "evidence-456"


class TestCollectionManager:
    """Test CollectionManager."""
    
    def test_create_collection(self):
        """Test creating collection."""
        manager = CollectionManager()
        
        collection = manager.create(
            name="Test Collection",
            owner="analyst-1",
            description="Test description",
        )
        
        assert collection.name == "Test Collection"
        assert collection.status == "active"
    
    def test_add_product_reference(self):
        """Test adding product reference."""
        manager = CollectionManager()
        product_manager = ProductManager()
        
        collection = manager.create(
            name="Test Collection",
            owner="analyst",
        )
        
        product = product_manager.create(
            product_type="threat_report",
            title="Test",
            owner="analyst",
        )
        
        updated = manager.add_product(collection.id, product.id)
        
        assert updated is not None
        assert product.id in updated.product_refs


class TestReviewManager:
    """Test ReviewManager."""
    
    def test_create_review(self):
        """Test creating review."""
        manager = ReviewManager()
        reviewer = Reviewer(
            user_id="user-1",
            name="John Doe",
            role="reviewer",
        )
        
        review = manager.create_review(
            product_id="prod-1",
            reviewers=[reviewer],
        )
        
        assert review.product_id == "prod-1"
        assert review.status == "pending"


class TestApprovalManager:
    """Test ApprovalManager."""
    
    def test_create_approval(self):
        """Test creating approval."""
        manager = ApprovalManager()
        
        approval = manager.create_approval(
            product_id="prod-1",
            approval_type="final",
        )
        
        assert approval.product_id == "prod-1"
        assert approval.status == "pending"


class TestPublicationManager:
    """Test PublicationManager."""
    
    def test_create_publication(self):
        """Test creating publication."""
        manager = PublicationManager()
        
        publication = manager.create(product_id="prod-1")
        
        assert publication.product_id == "prod-1"
        assert publication.status == "draft"


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = WorkbenchEventEmitter()
        
        emitter.emit_product_created("prod-1", "analyst")
        emitter.emit_product_review_started("prod-1", "review-1")
        emitter.emit_product_approved("prod-1", "approval-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_cti_ownership(self):
        """Test no CTI ownership."""
        import workbench.models
        import workbench.runtime
        
        source_files = [
            workbench.models.__file__,
            workbench.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            # Workbench should only reference, not own
            assert "class Indicator" not in content
            assert "class ThreatActor" not in content
            assert "class Malware" not in content
            assert "class Campaign" not in content
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import workbench.models
        import workbench.runtime
        
        source_files = [
            workbench.models.__file__,
            workbench.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_detection_imports(self):
        """Test no detection imports."""
        import workbench.models
        import workbench.runtime
        
        source_files = [
            workbench.models.__file__,
            workbench.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "detection" not in content.lower()
            assert "sigma" not in content.lower()
    
    def test_no_external_imports(self):
        """Test no external imports."""
        import workbench.models
        import workbench.runtime
        
        source_files = [
            workbench.models.__file__,
            workbench.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_reference_only_models(self):
        """Test that reference models exist."""
        from workbench.models import (
            AssertionReference,
            EvidencePackageReference,
            KnowledgeReference,
        )
        
        # These should exist and be reference-only
        ref = AssertionReference(
            product_id="test",
            assertion_ref="test",
            source_system="test",
        )
        # Reference models should exist
        assert ref.assertion_ref == "test"
