"""
analyst_workspace/tests/test_analyst_workspace.py

Tests for Analyst Workspace Module.
"""
import pytest

from analyst_workspace.models import (
    Workspace,
    WorkspaceSession,
    WorkspaceLayout,
    WorkspaceState,
    WorkspacePreference,
    WorkspaceContext,
    WorkspaceSelection,
    NavigationNode,
    Breadcrumb,
    NavigationState,
    WorkspaceBookmark,
    WorkspaceFavorite,
    CommandDefinition,
    WorkspaceCommand,
    WorkspaceNotification,
    ViewDefinition,
    PanelDefinition,
    OpenView,
    OpenPanel,
)

from analyst_workspace.models.enums import (
    WorkspaceStatus,
    SessionStatus,
    ViewType,
    PanelType,
    CommandScope,
    NotificationLevel,
)

from analyst_workspace.runtime import (
    WorkspaceRuntime,
    WorkspaceSessionManager,
    WorkspaceContextManager,
    WorkspaceNavigationManager,
    WorkspaceStateManager,
    WorkspaceCommandDispatcher,
    ViewRegistry,
    PanelRegistry,
)

from analyst_workspace.events import (
    WorkspaceEventEmitter,
    WorkspaceEventType,
)


class TestWorkspaceModel:
    """Test Workspace model."""
    
    def test_create_workspace(self):
        """Test creating workspace."""
        workspace = Workspace(
            name="Analyst Workspace",
            description="Main workspace",
            owner_id="user-1",
        )
        
        assert workspace.name == "Analyst Workspace"
        assert workspace.owner_id == "user-1"
        assert workspace.id is not None
        assert workspace.status == "active"
    
    def test_workspace_to_dict(self):
        """Test workspace serialization."""
        workspace = Workspace(
            name="Test Workspace",
            description="Test description",
            owner_id="user-1",
        )
        
        data = workspace.to_dict()
        assert data["name"] == "Test Workspace"
        assert data["owner_id"] == "user-1"


class TestWorkspaceLayout:
    """Test WorkspaceLayout model."""
    
    def test_create_layout(self):
        """Test creating layout."""
        layout = WorkspaceLayout(
            layout_id="layout-1",
            name="Default Layout",
            description="Default layout configuration",
        )
        
        assert layout.layout_id == "layout-1"
        assert layout.name == "Default Layout"


class TestWorkspaceState:
    """Test WorkspaceState model."""
    
    def test_create_state(self):
        """Test creating state."""
        state = WorkspaceState(
            state_id="state-1",
            workspace_id="workspace-1",
            active_view="entity_view",
        )
        
        assert state.state_id == "state-1"
        assert state.active_view == "entity_view"


class TestWorkspaceSession:
    """Test WorkspaceSession model."""
    
    def test_create_session(self):
        """Test creating session."""
        session = WorkspaceSession(
            workspace_id="workspace-1",
            user_id="user-1",
            status="active",
        )
        
        assert session.workspace_id == "workspace-1"
        assert session.user_id == "user-1"
        assert session.status == "active"


class TestNavigationModels:
    """Test navigation models."""
    
    def test_create_navigation_node(self):
        """Test creating navigation node."""
        node = NavigationNode(
            workspace_id="workspace-1",
            label="Indicators",
            node_type="folder",
        )
        
        assert node.label == "Indicators"
        assert node.workspace_id == "workspace-1"
    
    def test_create_breadcrumb(self):
        """Test creating breadcrumb."""
        breadcrumb = Breadcrumb(
            workspace_id="workspace-1",
            label="Home",
            entity_type="root",
            entity_id="root",
            position=0,
        )
        
        assert breadcrumb.label == "Home"
        assert breadcrumb.position == 0
    
    def test_create_navigation_state(self):
        """Test creating navigation state."""
        state = NavigationState(
            workspace_id="workspace-1",
            current_node_id="node-1",
        )
        
        assert state.workspace_id == "workspace-1"
        assert state.current_node_id == "node-1"


class TestBookmarkModels:
    """Test bookmark models."""
    
    def test_create_bookmark(self):
        """Test creating bookmark."""
        bookmark = WorkspaceBookmark(
            workspace_id="workspace-1",
            user_id="user-1",
            name="APT29 Indicators",
            entity_type="indicator",
            entity_id="ioc-1",
        )
        
        assert bookmark.name == "APT29 Indicators"
        assert bookmark.entity_type == "indicator"
    
    def test_create_favorite(self):
        """Test creating favorite."""
        favorite = WorkspaceFavorite(
            workspace_id="workspace-1",
            user_id="user-1",
            entity_type="actor",
            entity_id="actor-1",
            label="APT29",
        )
        
        assert favorite.label == "APT29"


class TestCommandModels:
    """Test command models."""
    
    def test_create_command_definition(self):
        """Test creating command definition."""
        command = CommandDefinition(
            name="open_entity",
            description="Open entity view",
            scope="global",
            shortcut="Ctrl+O",
        )
        
        assert command.name == "open_entity"
        assert command.scope == "global"
    
    def test_create_workspace_command(self):
        """Test creating workspace command."""
        command = WorkspaceCommand(
            workspace_id="workspace-1",
            name="open",
            command_type="navigation",
        )
        
        assert command.name == "open"


class TestViewModels:
    """Test view models."""
    
    def test_create_view_definition(self):
        """Test creating view definition."""
        view = ViewDefinition(
            name="Entity View",
            view_type="entity",
            description="View for entity details",
        )
        
        assert view.name == "Entity View"
        assert view.view_type == "entity"
    
    def test_create_open_view(self):
        """Test creating open view."""
        view = OpenView(
            workspace_id="workspace-1",
            view_id="view-1",
            view_type="entity",
            entity_id="entity-1",
            entity_type="indicator",
        )
        
        assert view.workspace_id == "workspace-1"
        assert view.entity_id == "entity-1"


class TestPanelModels:
    """Test panel models."""
    
    def test_create_panel_definition(self):
        """Test creating panel definition."""
        panel = PanelDefinition(
            name="Entity Details",
            panel_type="entity_details",
            description="Entity details panel",
        )
        
        assert panel.name == "Entity Details"
        assert panel.panel_type == "entity_details"
    
    def test_create_open_panel(self):
        """Test creating open panel."""
        panel = OpenPanel(
            workspace_id="workspace-1",
            panel_id="panel-1",
            panel_type="entity_details",
        )
        
        assert panel.workspace_id == "workspace-1"


class TestNotificationModel:
    """Test notification model."""
    
    def test_create_notification(self):
        """Test creating notification."""
        notification = WorkspaceNotification(
            workspace_id="workspace-1",
            title="New Indicator",
            message="A new indicator was added",
            level="info",
        )
        
        assert notification.title == "New Indicator"
        assert notification.level == "info"


class TestWorkspaceRuntime:
    """Test WorkspaceRuntime."""
    
    def test_create_workspace(self):
        """Test creating workspace."""
        runtime = WorkspaceRuntime()
        
        workspace = runtime.create_workspace(
            name="Test Workspace",
            owner_id="user-1",
            description="Test description",
        )
        
        assert workspace.name == "Test Workspace"
        assert workspace.owner_id == "user-1"
    
    def test_get_workspace(self):
        """Test getting workspace."""
        runtime = WorkspaceRuntime()
        
        created = runtime.create_workspace(
            name="Test",
            owner_id="user-1",
        )
        
        retrieved = runtime.get_workspace(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_update_workspace(self):
        """Test updating workspace."""
        runtime = WorkspaceRuntime()
        
        workspace = runtime.create_workspace(
            name="Test",
            owner_id="user-1",
        )
        
        updated = runtime.update_workspace(
            Workspace(
                id=workspace.id,
                name="Updated",
                description=workspace.description,
                owner_id=workspace.owner_id,
                status=workspace.status,
                layouts=workspace.layouts,
                current_layout_id=workspace.current_layout_id,
                preferences=workspace.preferences,
                context=workspace.context,
                tags=workspace.tags,
                created_at=workspace.created_at,
                modified_at=workspace.modified_at,
                version=workspace.version,
                metadata=workspace.metadata,
                author=workspace.author,
                reason=workspace.reason,
                revision_history=workspace.revision_history,
            )
        )
        
        assert updated.name == "Updated"
    
    def test_list_workspaces(self):
        """Test listing workspaces."""
        runtime = WorkspaceRuntime()
        
        runtime.create_workspace(name="Workspace 1", owner_id="user-1")
        runtime.create_workspace(name="Workspace 2", owner_id="user-1")
        
        workspaces = runtime.list_workspaces()
        assert len(workspaces) >= 2


class TestSessionManager:
    """Test WorkspaceSessionManager."""
    
    def test_create_session(self):
        """Test creating session."""
        manager = WorkspaceSessionManager()
        
        session = manager.create_session(
            workspace_id="workspace-1",
            user_id="user-1",
        )
        
        assert session.workspace_id == "workspace-1"
        assert session.user_id == "user-1"
    
    def test_get_session(self):
        """Test getting session."""
        manager = WorkspaceSessionManager()
        
        created = manager.create_session(
            workspace_id="workspace-1",
            user_id="user-1",
        )
        
        retrieved = manager.get_session(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id


class TestNavigationManager:
    """Test WorkspaceNavigationManager."""
    
    def test_create_navigation_state(self):
        """Test creating navigation state."""
        manager = WorkspaceNavigationManager()
        
        state = manager.create_navigation_state("workspace-1")
        
        assert state.workspace_id == "workspace-1"
    
    def test_navigate_to(self):
        """Test navigating to node."""
        manager = WorkspaceNavigationManager()
        
        state = manager.navigate_to("workspace-1", "node-1")
        
        assert state is not None
        assert state.current_node_id == "node-1"


class TestCommandDispatcher:
    """Test WorkspaceCommandDispatcher."""
    
    def test_register_command(self):
        """Test registering command."""
        dispatcher = WorkspaceCommandDispatcher()
        
        command = CommandDefinition(
            name="test_command",
            description="Test command",
        )
        
        dispatcher.register_command(command)
        
        retrieved = dispatcher.get_command(command.id)
        assert retrieved is not None
        assert retrieved.name == "test_command"
    
    def test_dispatch(self):
        """Test dispatching command."""
        dispatcher = WorkspaceCommandDispatcher()
        
        execution = dispatcher.dispatch(
            "test_command",
            "workspace-1",
            "session-1",
            {"param": "value"},
        )
        
        assert execution.command_name == "test_command"
        assert execution.success


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = WorkspaceEventEmitter()
        
        emitter.emit_workspace_created("workspace-1", "user-1")
        emitter.emit_view_opened("workspace-1", "view-1", "entity")
        emitter.emit_selection_changed("workspace-1", ["entity-1"])
        
        events = emitter.get_events()
        assert len(events) == 3
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestRegistries:
    """Test registries."""
    
    def test_view_registry(self):
        """Test view registry."""
        registry = ViewRegistry()
        
        view = ViewDefinition(
            name="Test View",
            view_type="test",
        )
        
        registry.register(view)
        
        retrieved = registry.get(view.id)
        assert retrieved is not None
        assert retrieved.name == "Test View"
    
    def test_panel_registry(self):
        """Test panel registry."""
        registry = PanelRegistry()
        
        panel = PanelDefinition(
            name="Test Panel",
            panel_type="test",
        )
        
        registry.register(panel)
        
        retrieved = registry.get(panel.id)
        assert retrieved is not None
        assert retrieved.name == "Test Panel"


class TestArchitectureBoundaries:
    """Test architecture boundaries."""
    
    def test_no_ai_imports(self):
        """Test no AI imports."""
        import analyst_workspace.models
        import analyst_workspace.runtime
        import analyst_workspace.events
        
        source_files = [
            analyst_workspace.models.__file__,
            analyst_workspace.runtime.__file__,
            analyst_workspace.events.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from openai" not in content
            assert "import openai" not in content
            assert "from anthropic" not in content
            assert "import anthropic" not in content
    
    def test_no_detection_imports(self):
        """Test no detection imports."""
        import analyst_workspace.models
        import analyst_workspace.runtime
        
        source_files = [
            analyst_workspace.models.__file__,
            analyst_workspace.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "detection" not in content.lower()
            assert "correlation" not in content.lower()
    
    def test_no_inference_imports(self):
        """Test no inference imports."""
        import analyst_workspace.models
        import analyst_workspace.runtime
        
        source_files = [
            analyst_workspace.models.__file__,
            analyst_workspace.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "inference" not in content.lower()
    
    def test_no_external_imports(self):
        """Test no external imports."""
        import analyst_workspace.models
        import analyst_workspace.runtime
        
        source_files = [
            analyst_workspace.models.__file__,
            analyst_workspace.runtime.__file__,
        ]
        
        for source_file in source_files:
            content = open(source_file).read()
            assert "from connectors" not in content
            assert "import connectors" not in content
            assert "from exchange" not in content
            assert "import exchange" not in content
