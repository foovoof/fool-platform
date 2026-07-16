"""
threat_intelligence/tests/test_threat_intelligence.py

Tests for Threat Intelligence Module.
"""
import pytest

from threat_intelligence.models import (
    Indicator,
    ThreatActor,
    Campaign,
    Malware,
    Tool,
    Infrastructure,
    Vulnerability,
    Relationship,
    EvidenceReference,
    EvidenceBundle,
    IntelligenceFinding,
    ThreatReport,
    ThreatPackage,
    ThreatCollection,
    IndicatorType,
    ThreatActorType,
    MalwareType,
    CampaignStatus,
    ConfidenceLevel,
    ThreatLevel,
    ReportType,
    ReportStatus,
    FindingType,
    EvidenceType,
)

from threat_intelligence.repository import (
    InMemoryRepository,
    IndicatorRepository,
    ThreatActorRepository,
    MalwareRepository,
    RelationshipRepository,
)

from threat_intelligence.services import (
    IndicatorService,
    ThreatActorService,
    MalwareService,
    RelationshipService,
)

from threat_intelligence.events import (
    ThreatIntelligenceEventEmitter,
    ThreatIntelligenceEventType,
)

from threat_intelligence.validation import (
    ValidationService,
    IndicatorValidator,
    ThreatActorValidator,
    RelationshipValidator,
)

from threat_intelligence.query import QueryService

from threat_intelligence.versioning import (
    Version,
    VersionHistory,
    VersioningService,
)

from threat_intelligence.confidence import (
    ConfidenceAssessment,
    SourceAssessment,
    ConfidenceService,
)

from threat_intelligence.lifecycle import (
    LifecycleState,
    LifecycleService,
    IndicatorLifecycle,
    CampaignLifecycle,
    ReportLifecycle,
)

from threat_intelligence.reporting import (
    ReportBuilder,
    ReportValidator,
    ReportExporter,
)

from threat_intelligence.evidence import (
    EvidenceValidator,
    EvidenceChainBuilder,
    EvidenceTimelineBuilder,
    EvidenceLineageBuilder,
)

from threat_intelligence.attribution import (
    AttributionBuilder,
    AttributionSupport,
)


class TestIndicatorModel:
    """Test Indicator model."""
    
    def test_create_indicator(self):
        """Test creating an indicator."""
        indicator = Indicator(
            name="Malicious IP",
            value="1.2.3.4",
            indicator_type=IndicatorType.IPV4_ADDRESS.value,
            description="Known malicious IP",
        )
        
        assert indicator.name == "Malicious IP"
        assert indicator.value == "1.2.3.4"
        assert indicator.indicator_type == "ipv4_addr"
        assert indicator.id is not None
        assert indicator.version == 1
    
    def test_indicator_to_dict(self):
        """Test indicator serialization."""
        indicator = Indicator(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        data = indicator.to_dict()
        assert data["name"] == "Test"
        assert data["value"] == "test.com"
        assert data["indicator_type"] == "domain_name"


class TestThreatActorModel:
    """Test ThreatActor model."""
    
    def test_create_threat_actor(self):
        """Test creating a threat actor."""
        actor = ThreatActor(
            name="APT29",
            alias="Cozy Bear",
            description="Russian threat actor",
            actor_type=ThreatActorType.NATION_STATE.value,
        )
        
        assert actor.name == "APT29"
        assert actor.alias == "Cozy Bear"
        assert actor.actor_type == "nation_state"
    
    def test_threat_actor_to_dict(self):
        """Test threat actor serialization."""
        actor = ThreatActor(
            name="Test Actor",
            actor_type=ThreatActorType.ORGANIZED_CRIME.value,
        )
        
        data = actor.to_dict()
        assert data["name"] == "Test Actor"
        assert data["actor_type"] == "organized_crime"


class TestMalwareModel:
    """Test Malware model."""
    
    def test_create_malware(self):
        """Test creating malware."""
        malware = Malware(
            name="Emotet",
            malware_type=MalwareType.TROJAN.value,
            description="Banking trojan",
        )
        
        assert malware.name == "Emotet"
        assert malware.malware_type == "trojan"
    
    def test_malware_to_dict(self):
        """Test malware serialization."""
        malware = Malware(
            name="Test Malware",
            malware_type=MalwareType.RANSOMWARE.value,
        )
        
        data = malware.to_dict()
        assert data["name"] == "Test Malware"
        assert data["malware_type"] == "ransomware"


class TestCampaignModel:
    """Test Campaign model."""
    
    def test_create_campaign(self):
        """Test creating a campaign."""
        campaign = Campaign(
            name="Operation Aurora",
            description="Cyber espionage operation",
            status=CampaignStatus.COMPLETED.value,
        )
        
        assert campaign.name == "Operation Aurora"
        assert campaign.status == "completed"


class TestRelationshipModel:
    """Test Relationship model."""
    
    def test_create_relationship(self):
        """Test creating a relationship."""
        relationship = Relationship(
            source_type="threat_actor",
            source_id="actor-1",
            target_type="malware",
            target_id="malware-1",
            relationship_type="uses",
        )
        
        assert relationship.source_type == "threat_actor"
        assert relationship.target_type == "malware"
        assert relationship.relationship_type == "uses"


class TestEvidenceModels:
    """Test evidence models."""
    
    def test_create_evidence_reference(self):
        """Test creating evidence reference."""
        evidence = EvidenceReference(
            evidence_type=EvidenceType.DIRECT.value,
            content="Sample evidence content",
            source_system="test_system",
        )
        
        assert evidence.evidence_type == "direct"
        assert evidence.content == "Sample evidence content"
    
    def test_create_evidence_bundle(self):
        """Test creating evidence bundle."""
        bundle = EvidenceBundle(
            title="Evidence Bundle",
            description="Test bundle",
            evidence_items=({"id": "1"}, {"id": "2"}),
        )
        
        assert bundle.title == "Evidence Bundle"
        assert len(bundle.evidence_items) == 2


class TestFindingModel:
    """Test IntelligenceFinding model."""
    
    def test_create_finding(self):
        """Test creating a finding."""
        finding = IntelligenceFinding(
            title="New Threat Actor Activity",
            description="Suspicious activity detected",
            finding_type=FindingType.THREAT_ACTOR.value,
            threat_level=ThreatLevel.HIGH.value,
        )
        
        assert finding.title == "New Threat Actor Activity"
        assert finding.threat_level == "high"


class TestReportModels:
    """Test report models."""
    
    def test_create_threat_report(self):
        """Test creating a threat report."""
        report = ThreatReport(
            title="Weekly Threat Report",
            description="Summary of threats",
            report_type=ReportType.TECHNICAL.value,
            status=ReportStatus.DRAFT.value,
            author="analyst",
        )
        
        assert report.title == "Weekly Threat Report"
        assert report.status == "draft"


class TestRepository:
    """Test repository functionality."""
    
    def test_in_memory_repository(self):
        """Test in-memory repository."""
        repo = InMemoryRepository()
        
        indicator = Indicator(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        created = repo.create(indicator)
        assert created.id == indicator.id
        
        retrieved = repo.get(indicator.id)
        assert retrieved is not None
        assert retrieved.name == "Test"
        
        all_items = repo.list_all()
        assert len(all_items) == 1
        
        assert repo.count() == 1
        assert repo.exists(indicator.id)
        
        deleted = repo.delete(indicator.id)
        assert deleted
        assert repo.count() == 0
    
    def test_search(self):
        """Test repository search."""
        repo = IndicatorRepository()
        
        repo.create(Indicator(
            name="IP 1",
            value="1.1.1.1",
            indicator_type=IndicatorType.IPV4_ADDRESS.value,
        ))
        
        repo.create(Indicator(
            name="Domain 1",
            value="evil.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        ))
        
        results = repo.search({"indicator_type": IndicatorType.DOMAIN_NAME.value})
        assert len(results) == 1
        assert results[0].value == "evil.com"
    
    def test_clear(self):
        """Test clearing repository."""
        repo = IndicatorRepository()
        
        repo.create(Indicator(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        ))
        
        assert repo.count() == 1
        repo.clear()
        assert repo.count() == 0


class TestServices:
    """Test service functionality."""
    
    def test_indicator_service_create(self):
        """Test indicator service create."""
        service = IndicatorService()
        
        indicator = service.create(
            name="Malicious Domain",
            value="evil.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
            author="test",
        )
        
        assert indicator.name == "Malicious Domain"
        assert indicator.author == "test"
    
    def test_indicator_service_get(self):
        """Test indicator service get."""
        service = IndicatorService()
        
        created = service.create(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        retrieved = service.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_indicator_service_search(self):
        """Test indicator service search."""
        service = IndicatorService()
        
        service.create(
            name="IP 1",
            value="1.1.1.1",
            indicator_type=IndicatorType.IPV4_ADDRESS.value,
        )
        
        service.create(
            name="Domain 1",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        results = service.find_by_type(IndicatorType.IPV4_ADDRESS.value)
        assert len(results) == 1
    
    def test_threat_actor_service(self):
        """Test threat actor service."""
        service = ThreatActorService()
        
        actor = service.create(
            name="APT1",
            actor_type=ThreatActorType.NATION_STATE.value,
            author="test",
        )
        
        assert actor.name == "APT1"
        
        retrieved = service.get(actor.id)
        assert retrieved is not None
    
    def test_malware_service(self):
        """Test malware service."""
        service = MalwareService()
        
        malware = service.create(
            name="Trojan",
            malware_type=MalwareType.TROJAN.value,
            author="test",
        )
        
        assert malware.name == "Trojan"
    
    def test_relationship_service(self):
        """Test relationship service."""
        service = RelationshipService()
        
        rel = service.create(
            source_type="threat_actor",
            source_id="actor-1",
            target_type="malware",
            target_id="malware-1",
            relationship_type="uses",
            author="test",
        )
        
        assert rel.relationship_type == "uses"


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = ThreatIntelligenceEventEmitter()
        
        emitter.emit_indicator_created("indicator-1")
        emitter.emit_indicator_updated("indicator-1")
        emitter.emit_actor_created("actor-1")
        emitter.emit_malware_created("malware-1")
        
        events = emitter.get_events()
        assert len(events) == 4
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0
    
    def test_event_disable(self):
        """Test disabling events."""
        emitter = ThreatIntelligenceEventEmitter()
        emitter.disable()
        
        emitter.emit_indicator_created("indicator-1")
        assert len(emitter.get_events()) == 0
        
        emitter.enable()
        emitter.emit_indicator_created("indicator-1")
        assert len(emitter.get_events()) == 1


class TestValidation:
    """Test validation functionality."""
    
    def test_indicator_validator_valid(self):
        """Test valid indicator."""
        indicator = Indicator(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        result = IndicatorValidator.validate(indicator)
        assert result.is_valid
    
    def test_indicator_validator_invalid(self):
        """Test invalid indicator."""
        indicator = Indicator(
            name="Test",
            value="",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        result = IndicatorValidator.validate(indicator)
        assert not result.is_valid
        assert len(result.issues) > 0
    
    def test_validation_service(self):
        """Test validation service."""
        service = ValidationService()
        
        indicator = Indicator(
            name="Test",
            value="test.com",
            indicator_type=IndicatorType.DOMAIN_NAME.value,
        )
        
        result = service.validate_indicator(indicator)
        assert result.is_valid


class TestQuery:
    """Test query functionality."""
    
    def test_query_service(self):
        """Test query service."""
        service = QueryService()
        
        results = service.search_indicators({})
        assert isinstance(results, list)
        
        results = service.search_actors({})
        assert isinstance(results, list)


class TestVersioning:
    """Test versioning functionality."""
    
    def test_version_history(self):
        """Test version history."""
        history = VersionHistory("entity-1")
        
        history.add_version(1, "author", "Initial creation")
        history.add_version(2, "author", "Update 1")
        
        assert history.get_version_count() == 2
        
        v2 = history.get_version(2)
        assert v2 is not None
        assert v2.version == 2
    
    def test_versioning_service(self):
        """Test versioning service."""
        service = VersioningService()
        
        service.record_version("entity-1", 1, "author", "Initial")
        service.record_version("entity-1", 2, "author", "Update")
        
        history = service.get_history("entity-1")
        assert history is not None
        assert history.get_version_count() == 2


class TestConfidence:
    """Test confidence functionality."""
    
    def test_confidence_assessment(self):
        """Test confidence assessment."""
        assessment = ConfidenceAssessment(
            confidence_level="high",
            confidence_score=0.8,
            source_reliability="a",
            information_reliability="confirmed",
        )
        
        assert assessment.confidence_level == "high"
        assert assessment.confidence_score == 0.8
    
    def test_confidence_service_calculate(self):
        """Test confidence calculation."""
        service = ConfidenceService()
        
        level, score = service.calculate_confidence("a", "confirmed")
        
        assert level == "high"
        assert score == 0.9
    
    def test_confidence_history(self):
        """Test confidence history."""
        service = ConfidenceService()
        
        assessment = ConfidenceAssessment(
            confidence_level=ConfidenceLevel.MEDIUM.value,
            confidence_score=0.5,
        )
        
        service.record_confidence("entity-1", assessment)
        
        history = service.get_confidence_history("entity-1")
        assert history is not None
        
        latest = service.get_latest_confidence("entity-1")
        assert latest is not None
        assert latest.confidence_level == "medium"


class TestLifecycle:
    """Test lifecycle functionality."""
    
    def test_indicator_lifecycle_transitions(self):
        """Test indicator lifecycle transitions."""
        assert IndicatorLifecycle.can_transition("new", "in_progress")
        assert not IndicatorLifecycle.can_transition("new", "archived")
    
    def test_lifecycle_service(self):
        """Test lifecycle service."""
        service = LifecycleService()
        
        success, msg = service.transition(
            "entity-1",
            "in_progress",
            reason="Starting",
            transitioned_by="user",
        )
        
        assert success
        
        state = service.get_lifecycle("entity-1")
        assert state.status == "in_progress"


class TestReporting:
    """Test reporting functionality."""
    
    def test_report_builder(self):
        """Test report builder."""
        builder = ReportBuilder()
        
        report = builder.set_title("Test Report") \
            .set_description("Test description") \
            .set_author("analyst") \
            .add_section("Introduction", "Content here") \
            .build()
        
        assert report.title == "Test Report"
        assert len(report.sections) == 1
    
    def test_report_validator(self):
        """Test report validator."""
        report = ThreatReport(
            title="Test",
            report_type=ReportType.TECHNICAL.value,
            author="analyst",
        )
        
        is_valid, errors = ReportValidator.validate(report)
        assert is_valid
    
    def test_report_exporter(self):
        """Test report exporter."""
        report = ThreatReport(
            title="Test",
            report_type=ReportType.TECHNICAL.value,
            author="analyst",
        )
        
        summary = ReportExporter.to_summary(report)
        assert summary["title"] == "Test"
        assert summary["indicator_count"] == 0


class TestEvidence:
    """Test evidence functionality."""
    
    def test_evidence_chain_builder(self):
        """Test evidence chain builder."""
        builder = EvidenceChainBuilder()
        
        bundle = builder.add_evidence("e1", "direct", "Evidence 1") \
            .add_evidence("e2", "circumstantial", "Evidence 2") \
            .build()
        
        assert len(bundle.evidence_items) == 2
    
    def test_evidence_timeline_builder(self):
        """Test evidence timeline builder."""
        builder = EvidenceTimelineBuilder()
        
        timeline = builder.add_entry(
            "2024-01-01",
            "Event 1",
            "Description 1",
        ).add_entry(
            "2024-01-02",
            "Event 2",
            "Description 2",
        ).build()
        
        assert len(timeline.timeline_entries) == 2
    
    def test_evidence_lineage_builder(self):
        """Test evidence lineage builder."""
        builder = EvidenceLineageBuilder("root")
        
        lineage = builder.add_derivation("root", "child1") \
            .add_derivation("child1", "child2") \
            .build()
        
        assert lineage.parent_evidence == "root"
        assert len(lineage.child_evidence) == 2


class TestAttribution:
    """Test attribution functionality."""
    
    def test_attribution_builder(self):
        """Test attribution builder."""
        builder = AttributionBuilder("threat_actor", "actor-1")
        
        support = builder.add_evidence("e1", "direct", "Evidence", 1.0) \
            .add_indicator("i1", "ipv4", "1.2.3.4", 0.8) \
            .set_confidence("high", 0.9, "Multiple sources") \
            .set_explanation("Attribution based on evidence") \
            .build()
        
        assert support.target_type == "threat_actor"
        assert support.target_id == "actor-1"
        assert len(support.evidence) == 1
        assert len(support.indicators) == 1


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import threat_intelligence.models
        import threat_intelligence.services
        import threat_intelligence.events
        import threat_intelligence.validation
        import threat_intelligence.query
        import threat_intelligence.lifecycle
        import threat_intelligence.confidence
        import threat_intelligence.reporting
        import threat_intelligence.evidence
        import threat_intelligence.attribution
        
        source_files = [
            threat_intelligence.models.__file__,
            threat_intelligence.services.__file__,
            threat_intelligence.events.__file__,
            threat_intelligence.validation.__file__,
            threat_intelligence.query.__file__,
            threat_intelligence.lifecycle.__file__,
            threat_intelligence.confidence.__file__,
            threat_intelligence.reporting.__file__,
            threat_intelligence.evidence.__file__,
            threat_intelligence.attribution.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_connector_imports(self):
        """Test no connector imports."""
        import threat_intelligence.models
        import threat_intelligence.services
        
        source_files = [
            threat_intelligence.models.__file__,
            threat_intelligence.services.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_external_feed_imports(self):
        """Test no external feed imports."""
        import threat_intelligence.models
        import threat_intelligence.services
        
        source_files = [
            threat_intelligence.models.__file__,
            threat_intelligence.services.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "misp" not in content.lower()
            assert "taxii" not in content.lower()
