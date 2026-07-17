"""
executive_portal/tests/test_executive_portal.py

Tests for Executive Intelligence Portal Module.
"""
import pytest

from executive_portal.models import (
    ExecutiveWorkspace,
    ExecutiveDashboard,
    StrategicBriefing,
    ExecutiveCollection,
    ExecutiveWidget,
    ExecutiveBookmark,
    PublicationFeed,
    ExecutivePreference,
    ExecutiveSession,
    AuditEntry,
    SavedSearch,
    DashboardSection,
    WidgetReference,
    BriefingSection,
    CollectionReference,
)

from executive_portal.runtime import (
    WorkspaceManager,
    DashboardManager,
    BriefingManager,
    CollectionManager,
    FeedManager,
    BookmarkManager,
    SearchManager,
    SessionManager,
    AuditManager,
)

from executive_portal.events import (
    PortalEventEmitter,
    PortalEventType,
)


class TestExecutiveWorkspaceModel:
    """Test ExecutiveWorkspace model."""
    
    def test_create_workspace(self):
        """Test creating workspace."""
        workspace = ExecutiveWorkspace(
            name="Executive Dashboard",
            description="Main executive workspace",
            owner="exec-1",
        )
        
        assert workspace.name == "Executive Dashboard"
        assert workspace.owner == "exec-1"
        assert workspace.id is not None


class TestExecutiveDashboardModel:
    """Test ExecutiveDashboard model."""
    
    def test_create_dashboard(self):
        """Test creating dashboard."""
        dashboard = ExecutiveDashboard(
            name="Threat Overview",
            description="Threat intelligence overview",
            owner="exec-1",
            status="active",
        )
        
        assert dashboard.name == "Threat Overview"
        assert dashboard.status == "active"


class TestStrategicBriefingModel:
    """Test StrategicBriefing model."""
    
    def test_create_briefing(self):
        """Test creating briefing."""
        briefing = StrategicBriefing(
            title="Weekly Threat Update",
            description="Weekly executive briefing",
            owner="analyst-1",
            status="draft",
        )
        
        assert briefing.title == "Weekly Threat Update"
        assert briefing.status == "draft"


class TestExecutiveCollectionModel:
    """Test ExecutiveCollection model."""
    
    def test_create_collection(self):
        """Test creating collection."""
        collection = ExecutiveCollection(
            name="APT Reports",
            description="APT-related reports",
            owner="exec-1",
        )
        
        assert collection.name == "APT Reports"
        assert collection.status == "active"


class TestExecutiveWidgetModel:
    """Test ExecutiveWidget model."""
    
    def test_create_widget(self):
        """Test creating widget."""
        widget = ExecutiveWidget(
            widget_type="metric",
            name="Threat Count",
            title="Threat Count Widget",
        )
        
        assert widget.widget_type == "metric"
        assert widget.name == "Threat Count"


class TestExecutiveBookmarkModel:
    """Test ExecutiveBookmark model."""
    
    def test_create_bookmark(self):
        """Test creating bookmark."""
        bookmark = ExecutiveBookmark(
            user_id="user-1",
            name="APT29 Report",
            ref_id="report-123",
            ref_type="report",
            ref_source="reporting",
        )
        
        assert bookmark.name == "APT29 Report"
        assert bookmark.ref_type == "report"


class TestPublicationFeedModel:
    """Test PublicationFeed model."""
    
    def test_create_feed(self):
        """Test creating feed."""
        feed = PublicationFeed(
            name="Daily Intelligence Feed",
            description="Daily threat intelligence",
            feed_type="standard",
        )
        
        assert feed.name == "Daily Intelligence Feed"


class TestExecutiveSessionModel:
    """Test ExecutiveSession model."""
    
    def test_create_session(self):
        """Test creating session."""
        session = ExecutiveSession(
            user_id="user-1",
            workspace_id="workspace-1",
            status="active",
        )
        
        assert session.user_id == "user-1"
        assert session.status == "active"


class TestAuditEntryModel:
    """Test AuditEntry model."""
    
    def test_create_audit_entry(self):
        """Test creating audit entry."""
        entry = AuditEntry(
            session_id="session-1",
            user_id="user-1",
            action="viewed",
            entity_type="dashboard",
            entity_id="dashboard-1",
        )
        
        assert entry.action == "viewed"
        assert entry.entity_type == "dashboard"


class TestWorkspaceManager:
    """Test WorkspaceManager."""
    
    def test_create_workspace(self):
        """Test creating workspace."""
        manager = WorkspaceManager()
        
        workspace = manager.create(
            name="Test Workspace",
            owner="exec-1",
        )
        
        assert workspace.name == "Test Workspace"
    
    def test_get_workspace(self):
        """Test getting workspace."""
        manager = WorkspaceManager()
        
        created = manager.create(name="Test", owner="exec")
        retrieved = manager.get(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id


class TestDashboardManager:
    """Test DashboardManager."""
    
    def test_create_dashboard(self):
        """Test creating dashboard."""
        manager = DashboardManager()
        
        dashboard = manager.create(
            name="Test Dashboard",
            owner="exec-1",
        )
        
        assert dashboard.name == "Test Dashboard"
    
    def test_add_widget(self):
        """Test adding widget reference."""
        manager = DashboardManager()
        
        dashboard = manager.create(name="Test", owner="exec")
        
        widget_ref = WidgetReference(
            widget_type="metric",
            title="Test Widget",
            position={"x": 0, "y": 0},
            size={"width": 1, "height": 1},
        )
        
        updated = manager.add_widget(dashboard.id, widget_ref)
        
        assert updated is not None
        assert len(updated.widgets) == 1


class TestBriefingManager:
    """Test BriefingManager."""
    
    def test_create_briefing(self):
        """Test creating briefing."""
        manager = BriefingManager()
        
        briefing = manager.create(
            title="Test Briefing",
            owner="analyst-1",
        )
        
        assert briefing.title == "Test Briefing"


class TestCollectionManager:
    """Test CollectionManager."""
    
    def test_create_collection(self):
        """Test creating collection."""
        manager = CollectionManager()
        
        collection = manager.create(
            name="Test Collection",
            owner="exec-1",
        )
        
        assert collection.name == "Test Collection"


class TestFeedManager:
    """Test FeedManager."""
    
    def test_create_feed(self):
        """Test creating feed."""
        manager = FeedManager()
        
        feed = manager.create(name="Test Feed")
        
        assert feed.name == "Test Feed"


class TestBookmarkManager:
    """Test BookmarkManager."""
    
    def test_create_bookmark(self):
        """Test creating bookmark."""
        manager = BookmarkManager()
        
        bookmark = manager.create(
            user_id="user-1",
            name="Test Bookmark",
            ref_id="ref-1",
            ref_type="publication",
            ref_source="reporting",
        )
        
        assert bookmark.name == "Test Bookmark"


class TestSearchManager:
    """Test SearchManager."""
    
    def test_create_search(self):
        """Test creating saved search."""
        manager = SearchManager()
        
        search = manager.create(
            user_id="user-1",
            name="Test Search",
            query="APT29",
        )
        
        assert search.name == "Test Search"


class TestSessionManager:
    """Test SessionManager."""
    
    def test_create_session(self):
        """Test creating session."""
        manager = SessionManager()
        
        session = manager.create(
            user_id="user-1",
            workspace_id="workspace-1",
        )
        
        assert session.user_id == "user-1"
        assert session.status == "active"


class TestAuditManager:
    """Test AuditManager."""
    
    def test_record_audit(self):
        """Test recording audit entry."""
        manager = AuditManager()
        
        entry = manager.record(
            session_id="session-1",
            user_id="user-1",
            action="viewed",
            entity_type="dashboard",
            entity_id="dashboard-1",
        )
        
        assert entry.action == "viewed"


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = PortalEventEmitter()
        
        emitter.emit_workspace_created("workspace-1", "exec")
        emitter.emit_dashboard_created("dashboard-1")
        emitter.emit_briefing_created("briefing-1")
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_knowledge_mutation(self):
        """Test no knowledge mutation."""
        import executive_portal.models
        import executive_portal.runtime
        
        source_files = [
            executive_portal.models.__file__,
            executive_portal.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            # Portal should not create or modify knowledge
            assert "class.*Indicator.*Create" not in content
            assert "def.*create_indicator" not in content.lower()
    
    def test_no_cti_duplication(self):
        """Test no CTI duplication."""
        import executive_portal.models
        import executive_portal.runtime
        
        source_files = [
            executive_portal.models.__file__,
            executive_portal.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            # Portal should not duplicate CTI models
            assert "class ThreatActor" not in content
            assert "class Campaign" not in content
            assert "class Malware" not in content
            assert "class Indicator" not in content
    
    def test_reference_only_models(self):
        """Test that reference models exist."""
        from executive_portal.models import (
            PublicationReference,
            ReportReference,
            EvidenceReference,
        )
        
        ref = PublicationReference(
            widget_id="widget-1",
            title="Test Report",
            source="reporting",
        )
        # Reference models should exist
        assert ref.title == "Test Report"
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import executive_portal.models
        import executive_portal.runtime
        
        source_files = [
            executive_portal.models.__file__,
            executive_portal.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_detection_imports(self):
        """Test no detection imports."""
        import executive_portal.models
        import executive_portal.runtime
        
        source_files = [
            executive_portal.models.__file__,
            executive_portal.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "detection" not in content.lower()
    
    def test_no_soar_imports(self):
        """Test no SOAR imports."""
        import executive_portal.models
        import executive_portal.runtime
        
        source_files = [
            executive_portal.models.__file__,
            executive_portal.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "soar" not in content.lower()
            assert "automation" not in content.lower()
