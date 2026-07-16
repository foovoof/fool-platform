"""
threat_hunting/tests/test_threat_hunting.py

Tests for Threat Hunting Module.
"""
import pytest

from threat_hunting.models import (
    Hunt,
    HuntSession,
    HuntScope,
    HuntObjective,
    HuntHypothesis,
    HuntObservation,
    HuntFinding,
    HuntRecommendation,
    EvidenceBundle,
    EvidenceReference,
    ThreatHuntReport,
)

from threat_hunting.models.enums import (
    HuntStatus,
    HypothesisStatus,
    FindingSeverity,
    RecommendationType,
)

from threat_hunting.service import (
    HuntService,
    HypothesisService,
    ObservationService,
    FindingService,
    ReportService,
)

from threat_hunting.validation import (
    HuntValidator,
    HypothesisValidator,
    ObservationValidator,
    FindingValidator,
    ValidationResult,
)

from threat_hunting.events import (
    HuntEventEmitter,
    HuntEventType,
)


class TestHuntModel:
    """Test Hunt model."""
    
    def test_create_hunt(self):
        """Test creating hunt."""
        hunt = Hunt(
            name="APT Investigation",
            title="Investigate APT29 Activity",
            description="Hunt for APT29 indicators",
            author="analyst",
        )
        
        assert hunt.name == "APT Investigation"
        assert hunt.title == "Investigate APT29 Activity"
        assert hunt.id is not None
        assert hunt.status == "draft"
    
    def test_hunt_to_dict(self):
        """Test hunt serialization."""
        hunt = Hunt(
            name="Test Hunt",
            title="Test Title",
            description="Test description",
        )
        
        data = hunt.to_dict()
        assert data["name"] == "Test Hunt"
        assert data["title"] == "Test Title"


class TestHuntScope:
    """Test HuntScope model."""
    
    def test_create_scope(self):
        """Test creating scope."""
        scope = HuntScope(
            scope_id="scope-1",
            scope_type="indicator",
            description="Scope for indicators",
            entity_refs=("ioc-1", "ioc-2"),
        )
        
        assert scope.scope_id == "scope-1"
        assert len(scope.entity_refs) == 2


class TestHuntObjective:
    """Test HuntObjective model."""
    
    def test_create_objective(self):
        """Test creating objective."""
        objective = HuntObjective(
            objective_id="obj-1",
            hunt_id="hunt-1",
            title="Verify Indicators",
            description="Verify all IOCs are active",
            priority=1,
        )
        
        assert objective.objective_id == "obj-1"
        assert objective.priority == 1


class TestHuntSession:
    """Test HuntSession model."""
    
    def test_create_session(self):
        """Test creating session."""
        session = HuntSession(
            hunt_id="hunt-1",
            session_type="investigation",
            status="active",
        )
        
        assert session.hunt_id == "hunt-1"
        assert session.status == "active"


class TestHypothesisModel:
    """Test HuntHypothesis model."""
    
    def test_create_hypothesis(self):
        """Test creating hypothesis."""
        hypothesis = HuntHypothesis(
            hunt_id="hunt-1",
            title="APT29 Hypothesis",
            hypothesis_text="APT29 is targeting our infrastructure",
            assumptions=("APT29 is active", "They use specific malware"),
            status="draft",
        )
        
        assert hypothesis.hunt_id == "hunt-1"
        assert hypothesis.title == "APT29 Hypothesis"
        assert hypothesis.status == "draft"
    
    def test_hypothesis_to_dict(self):
        """Test hypothesis serialization."""
        hypothesis = HuntHypothesis(
            hunt_id="hunt-1",
            title="Test Hypothesis",
            hypothesis_text="Test text",
        )
        
        data = hypothesis.to_dict()
        assert data["hunt_id"] == "hunt-1"
        assert data["title"] == "Test Hypothesis"


class TestObservationModel:
    """Test HuntObservation model."""
    
    def test_create_observation(self):
        """Test creating observation."""
        observation = HuntObservation(
            hunt_id="hunt-1",
            description="Found suspicious traffic",
            source="network_monitor",
            confidence_score=0.7,
        )
        
        assert observation.hunt_id == "hunt-1"
        assert observation.confidence_score == 0.7


class TestFindingModel:
    """Test HuntFinding model."""
    
    def test_create_finding(self):
        """Test creating finding."""
        finding = HuntFinding(
            hunt_id="hunt-1",
            title="Suspicious Activity Detected",
            description="Found unusual network traffic patterns",
            severity="high",
            confidence_score=0.8,
        )
        
        assert finding.hunt_id == "hunt-1"
        assert finding.severity == "high"


class TestRecommendationModel:
    """Test HuntRecommendation model."""
    
    def test_create_recommendation(self):
        """Test creating recommendation."""
        recommendation = HuntRecommendation(
            hunt_id="hunt-1",
            finding_id="finding-1",
            recommendation_type="review_indicator",
            title="Review Indicator",
            description="Review the identified indicator",
        )
        
        assert recommendation.recommendation_type == "review_indicator"


class TestEvidenceBundle:
    """Test EvidenceBundle model."""
    
    def test_create_evidence_bundle(self):
        """Test creating evidence bundle."""
        evidence_ref = EvidenceReference(
            bundle_id="bundle-1",
            evidence_type="indicator",
            entity_type="ip_address",
            entity_id="1.2.3.4",
            description="Suspicious IP",
        )
        
        bundle = EvidenceBundle(
            hunt_id="hunt-1",
            finding_id="finding-1",
            title="Evidence Bundle 1",
            description="Collection of evidence",
            evidence_refs=(evidence_ref,),
        )
        
        assert bundle.hunt_id == "hunt-1"
        assert len(bundle.evidence_refs) == 1


class TestHuntReport:
    """Test ThreatHuntReport model."""
    
    def test_create_report(self):
        """Test creating report."""
        report = ThreatHuntReport(
            hunt_id="hunt-1",
            title="Hunt Report Q1",
            executive_summary="Summary of hunt findings",
            confidence_score=0.75,
        )
        
        assert report.hunt_id == "hunt-1"
        assert report.confidence_score == 0.75


class TestHuntService:
    """Test HuntService."""
    
    def test_create_hunt(self):
        """Test creating hunt."""
        service = HuntService()
        
        hunt = service.create(
            name="Test Hunt",
            title="Test Title",
            description="Test description",
            author="test",
        )
        
        assert hunt.name == "Test Hunt"
        assert hunt.author == "test"
    
    def test_get_hunt(self):
        """Test getting hunt."""
        service = HuntService()
        
        created = service.create(
            name="Test",
            title="Test Title",
        )
        
        retrieved = service.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_start_hunt(self):
        """Test starting hunt."""
        service = HuntService()
        
        hunt = service.create(
            name="Test",
            title="Test",
        )
        
        started = service.start_hunt(hunt.id)
        assert started is not None
        assert started.status == "in_progress"
    
    def test_complete_hunt(self):
        """Test completing hunt."""
        service = HuntService()
        
        hunt = service.create(
            name="Test",
            title="Test",
        )
        
        started = service.start_hunt(hunt.id)
        completed = service.complete_hunt(started.id)
        assert completed is not None
        assert completed.status == "completed"


class TestHypothesisService:
    """Test HypothesisService."""
    
    def test_create_hypothesis(self):
        """Test creating hypothesis."""
        service = HypothesisService()
        
        hypothesis = service.create(
            hunt_id="hunt-1",
            title="Test Hypothesis",
            hypothesis_text="Test hypothesis text",
            author="test",
        )
        
        assert hypothesis.title == "Test Hypothesis"
    
    def test_find_by_hunt(self):
        """Test finding by hunt."""
        service = HypothesisService()
        
        hypothesis = service.create(
            hunt_id="hunt-1",
            title="Test",
            hypothesis_text="Test",
        )
        
        results = service.find_by_hunt("hunt-1")
        assert any(h.id == hypothesis.id for h in results)


class TestObservationService:
    """Test ObservationService."""
    
    def test_create_observation(self):
        """Test creating observation."""
        service = ObservationService()
        
        observation = service.create(
            hunt_id="hunt-1",
            description="Test observation",
            source="test_source",
        )
        
        assert observation.description == "Test observation"


class TestFindingService:
    """Test FindingService."""
    
    def test_create_finding(self):
        """Test creating finding."""
        service = FindingService()
        
        finding = service.create(
            hunt_id="hunt-1",
            title="Test Finding",
            description="Test description",
        )
        
        assert finding.title == "Test Finding"


class TestValidation:
    """Test validation."""
    
    def test_valid_hunt(self):
        """Test valid hunt."""
        hunt = Hunt(
            name="Valid Hunt",
            title="Valid Title",
        )
        
        result = HuntValidator.validate(hunt)
        assert result.is_valid
    
    def test_invalid_hunt(self):
        """Test invalid hunt."""
        hunt = Hunt(
            name="",
            title="Valid Title",
        )
        
        result = HuntValidator.validate(hunt)
        assert not result.is_valid
    
    def test_valid_hypothesis(self):
        """Test valid hypothesis."""
        hypothesis = HuntHypothesis(
            hunt_id="hunt-1",
            title="Valid Hypothesis",
            hypothesis_text="Valid text",
        )
        
        result = HypothesisValidator.validate(hypothesis)
        assert result.is_valid
    
    def test_hypothesis_transition(self):
        """Test hypothesis transition validation."""
        result = HypothesisValidator.validate_transition("draft", "approved")
        assert result.is_valid
        
        result = HypothesisValidator.validate_transition("draft", "validated")
        assert not result.is_valid


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = HuntEventEmitter()
        
        emitter.emit_hunt_started("hunt-1", "analyst")
        emitter.emit_observation_recorded("hunt-1", "obs-1")
        emitter.emit_finding_generated("hunt-1", "finding-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import threat_hunting.models
        import threat_hunting.service
        import threat_hunting.validation
        
        source_files = [
            threat_hunting.models.__file__,
            threat_hunting.service.__file__,
            threat_hunting.validation.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_soar_imports(self):
        """Test no SOAR imports."""
        import threat_hunting.models
        import threat_hunting.service
        
        source_files = [
            threat_hunting.models.__file__,
            threat_hunting.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "soar" not in content.lower()
            assert "playbook" not in content.lower()
            assert "automation" not in content.lower()
    
    def test_no_response_imports(self):
        """Test no response action imports."""
        import threat_hunting.models
        import threat_hunting.service
        
        source_files = [
            threat_hunting.models.__file__,
            threat_hunting.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "containment" not in content.lower()
            assert "remediation" not in content.lower()
            assert "block" not in content.lower()
    
    def test_no_connector_imports(self):
        """Test no connector imports."""
        import threat_hunting.models
        import threat_hunting.service
        
        source_files = [
            threat_hunting.models.__file__,
            threat_hunting.service.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
