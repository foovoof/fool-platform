"""
threat_intelligence/campaigns/tests/test_campaigns.py

Tests for Campaign Intelligence Module.
"""
import pytest

from threat_intelligence.campaigns.models import (
    Campaign,
    CampaignAlias,
    CampaignMetadata,
    TimelineEvent,
    Milestone,
    ObservedActivity,
    CampaignTimeline,
    CampaignAssertion,
    CampaignEvidence,
    CampaignRelationship,
    CampaignRelationshipType,
    CampaignLifecycle,
    Approval,
    Review,
    AuditEntry,
    AuditTrail,
    CampaignVersion,
    CampaignHistory,
    RollbackMetadata,
)

from threat_intelligence.campaigns.models.enums import (
    CampaignStatus,
    CampaignSeverity,
    AssertionStatus,
    AssertionType,
)

from threat_intelligence.campaigns.repositories import (
    CampaignRepository,
    TimelineEventRepository,
    CampaignAssertionRepository,
    CampaignEvidenceRepository,
    CampaignRelationshipRepository,
)

from threat_intelligence.campaigns.services import (
    CampaignService,
    AssertionService,
    TimelineService,
    EvidenceService,
    RelationshipService,
    LifecycleService,
    GovernanceService,
    VersionService,
)

from threat_intelligence.campaigns.events import (
    CampaignEventEmitter,
    CampaignEventType,
)

from threat_intelligence.campaigns.validation import (
    CampaignValidator,
    ValidationResult,
)

from threat_intelligence.campaigns.queries import CampaignQueryService

from threat_intelligence.campaigns.registry import CampaignRegistry


class TestCampaignModel:
    """Test Campaign model."""
    
    def test_create_campaign(self):
        """Test creating a campaign."""
        campaign = Campaign(
            name="Operation Aurora",
            description="Cyber espionage operation",
            status=CampaignStatus.ACTIVE.value,
        )
        
        assert campaign.name == "Operation Aurora"
        assert campaign.status == "active"
        assert campaign.id is not None
    
    def test_campaign_to_dict(self):
        """Test campaign serialization."""
        campaign = Campaign(
            name="Test Campaign",
            description="Test description",
        )
        
        data = campaign.to_dict()
        assert data["name"] == "Test Campaign"
        assert data["description"] == "Test description"


class TestTimelineEventModel:
    """Test TimelineEvent model."""
    
    def test_create_timeline_event(self):
        """Test creating a timeline event."""
        event = TimelineEvent(
            campaign_id="campaign-1",
            event_type="attack",
            timestamp="2024-01-15T10:00:00Z",
            description="Attack detected",
        )
        
        assert event.campaign_id == "campaign-1"
        assert event.event_type == "attack"


class TestAssertionModel:
    """Test CampaignAssertion model."""
    
    def test_create_assertion(self):
        """Test creating an assertion."""
        assertion = CampaignAssertion(
            campaign_id="campaign-1",
            assertion_type=AssertionType.OBSERVATION.value,
            assertion="Attacker used spear phishing",
            status=AssertionStatus.PENDING.value,
        )
        
        assert assertion.campaign_id == "campaign-1"
        assert assertion.status == "pending"


class TestEvidenceModel:
    """Test CampaignEvidence model."""
    
    def test_create_evidence(self):
        """Test creating evidence."""
        evidence = CampaignEvidence(
            campaign_id="campaign-1",
            evidence_type="direct",
            title="Email Header",
            description="Phishing email header",
        )
        
        assert evidence.campaign_id == "campaign-1"
        assert evidence.evidence_type == "direct"


class TestRelationshipModel:
    """Test CampaignRelationship model."""
    
    def test_create_relationship(self):
        """Test creating a relationship."""
        relationship = CampaignRelationship(
            campaign_id="campaign-1",
            source_type="campaign",
            source_id="campaign-1",
            target_type="malware",
            target_id="malware-1",
            relationship_type=CampaignRelationshipType.USES,
        )
        
        assert relationship.campaign_id == "campaign-1"
        assert relationship.relationship_type == "uses"


class TestRepository:
    """Test repository functionality."""
    
    def test_campaign_repository(self):
        """Test campaign repository."""
        repo = CampaignRepository()
        
        campaign = Campaign(
            name="Test Campaign",
            description="Test",
        )
        
        created = repo.create(campaign)
        assert created.id == campaign.id
        
        retrieved = repo.get(campaign.id)
        assert retrieved is not None
        assert retrieved.name == "Test Campaign"
        
        all_campaigns = repo.list_all()
        assert len(all_campaigns) == 1
        
        assert repo.count() == 1
        assert repo.exists(campaign.id)
        
        deleted = repo.delete(campaign.id)
        assert deleted
        assert repo.count() == 0


class TestServices:
    """Test service functionality."""
    
    def test_campaign_service_create(self):
        """Test campaign service create."""
        service = CampaignService()
        
        campaign = service.create(
            name="Test Campaign",
            description="Test description",
            author="test",
        )
        
        assert campaign.name == "Test Campaign"
        assert campaign.author == "test"
    
    def test_campaign_service_get(self):
        """Test campaign service get."""
        service = CampaignService()
        
        created = service.create(
            name="Test",
            description="Test",
        )
        
        retrieved = service.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_campaign_service_search(self):
        """Test campaign service search."""
        service = CampaignService()
        
        service.create(
            name="Campaign 1",
            description="Test",
        )
        
        service.create(
            name="Campaign 2",
            description="Test",
        )
        
        results = service.search({})
        assert len(results) >= 2
    
    def test_assertion_service(self):
        """Test assertion service."""
        service = AssertionService()
        
        assertion = service.create(
            campaign_id="campaign-1",
            assertion_type="observation",
            assertion="Test assertion",
            author="test",
        )
        
        assert assertion.campaign_id == "campaign-1"
    
    def test_timeline_service(self):
        """Test timeline service."""
        service = TimelineService()
        
        event = service.create_event(
            campaign_id="campaign-1",
            event_type="attack",
            timestamp="2024-01-15T10:00:00Z",
            description="Attack event",
            author="test",
        )
        
        assert event.campaign_id == "campaign-1"
    
    def test_evidence_service(self):
        """Test evidence service."""
        service = EvidenceService()
        
        evidence = service.create(
            campaign_id="campaign-1",
            evidence_type="direct",
            title="Evidence 1",
            description="Test evidence",
            author="test",
        )
        
        assert evidence.campaign_id == "campaign-1"
    
    def test_relationship_service(self):
        """Test relationship service."""
        service = RelationshipService()
        
        relationship = service.create(
            campaign_id="campaign-1",
            source_type="campaign",
            source_id="campaign-1",
            target_type="malware",
            target_id="malware-1",
            relationship_type="uses",
            author="test",
        )
        
        assert relationship.relationship_type == "uses"


class TestLifecycleService:
    """Test lifecycle service."""
    
    def test_lifecycle_transitions(self):
        """Test lifecycle transitions."""
        service = LifecycleService()
        
        success, msg = service.transition(
            "campaign-1",
            "active",
            reason="Starting",
            transitioned_by="user",
        )
        
        assert success
        
        status = service.get_status("campaign-1")
        assert status == "active"
    
    def test_valid_transitions(self):
        """Test valid transitions."""
        service = LifecycleService()
        
        assert service.can_transition("planned", "active")
        assert service.can_transition("active", "completed")
        assert service.can_transition("completed", "archived")
        
        assert not service.can_transition("archived", "active")
        assert not service.can_transition("planned", "completed")


class TestGovernanceService:
    """Test governance service."""
    
    def test_approval_workflow(self):
        """Test approval workflow."""
        service = GovernanceService()
        
        approval = service.create_approval(
            campaign_id="campaign-1",
            approval_type="create",
            author="test",
        )
        
        assert approval.campaign_id == "campaign-1"
        
        approved = service.approve(
            approval.id,
            approver="admin",
            comments="Approved",
        )
        
        assert approved is not None
        assert approved.status == "approved"
    
    def test_reject_workflow(self):
        """Test reject workflow."""
        service = GovernanceService()
        
        approval = service.create_approval(
            campaign_id="campaign-1",
            approval_type="create",
            author="test",
        )
        
        rejected = service.reject(
            approval.id,
            approver="admin",
            rejection_reason="Insufficient data",
        )
        
        assert rejected is not None
        assert rejected.status == "rejected"


class TestVersionService:
    """Test version service."""
    
    def test_create_version(self):
        """Test version creation."""
        service = VersionService()
        
        version = service.create_version(
            campaign_id="campaign-1",
            changes="Initial version",
            changes_summary="Initial",
            changed_by="test",
            change_reason="Created",
        )
        
        assert version.campaign_id == "campaign-1"
        assert version.version_number == 1
    
    def test_get_history(self):
        """Test getting history."""
        service = VersionService()
        
        service.create_version(
            campaign_id="campaign-1",
            changes="Version 1",
            changes_summary="v1",
            changed_by="test",
        )
        
        history = service.get_history("campaign-1")
        assert history is not None
        assert history.total_revisions == 1


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = CampaignEventEmitter()
        
        emitter.emit_campaign_created("campaign-1")
        emitter.emit_campaign_updated("campaign-1")
        emitter.emit_assertion_created("campaign-1", "assertion-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestValidation:
    """Test validation functionality."""
    
    def test_campaign_validator_valid(self):
        """Test valid campaign."""
        campaign = Campaign(
            name="Test Campaign",
            description="Test",
        )
        
        result = CampaignValidator.validate(campaign)
        assert result.is_valid
    
    def test_campaign_validator_invalid(self):
        """Test invalid campaign."""
        campaign = Campaign(
            name="",
            description="Test",
        )
        
        result = CampaignValidator.validate(campaign)
        assert not result.is_valid
        assert len(result.issues) > 0


class TestQueryService:
    """Test query service."""
    
    def test_query_service(self):
        """Test query service."""
        service = CampaignQueryService()
        
        results = service.find_by_actor("actor-1")
        assert isinstance(results, list)
        
        results = service.find_by_status("active")
        assert isinstance(results, list)


class TestRegistry:
    """Test registry."""
    
    def test_get_relationship_types(self):
        """Test getting relationship types."""
        types = CampaignRegistry.get_relationship_types()
        assert "uses" in types
        assert "targets" in types
    
    def test_get_assertion_types(self):
        """Test getting assertion types."""
        types = CampaignRegistry.get_assertion_types()
        assert "observation" in types
        assert "inference" in types


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import threat_intelligence.campaigns.models
        import threat_intelligence.campaigns.services
        import threat_intelligence.campaigns.validation
        import threat_intelligence.campaigns.queries
        import threat_intelligence.campaigns.events
        import threat_intelligence.campaigns.registry
        
        source_files = [
            threat_intelligence.campaigns.models.__file__,
            threat_intelligence.campaigns.services.__file__,
            threat_intelligence.campaigns.validation.__file__,
            threat_intelligence.campaigns.queries.__file__,
            threat_intelligence.campaigns.events.__file__,
            threat_intelligence.campaigns.registry.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_connector_imports(self):
        """Test no connector imports."""
        import threat_intelligence.campaigns.models
        import threat_intelligence.campaigns.services
        
        source_files = [
            threat_intelligence.campaigns.models.__file__,
            threat_intelligence.campaigns.services.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_external_feed_imports(self):
        """Test no external feed imports."""
        import threat_intelligence.campaigns.models
        import threat_intelligence.campaigns.services
        
        source_files = [
            threat_intelligence.campaigns.models.__file__,
            threat_intelligence.campaigns.services.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "misp" not in content.lower()
            assert "taxii" not in content.lower()
