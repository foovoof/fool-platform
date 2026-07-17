"""
analyst_workspace/runtime.py

Analyst Workspace Runtime.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from analyst_workspace.models import (
    Workspace,
    WorkspaceSession,
    WorkspaceState,
    WorkspaceLayout,
    WorkspaceContext,
    WorkspaceSelection,
    NavigationState,
    SessionSnapshot,
    OpenView,
    OpenPanel,
    CommandDefinition,
    CommandExecution,
    ViewDefinition,
    PanelDefinition,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._workspaces: dict[str, Workspace] = {}
        self._sessions: dict[str, WorkspaceSession] = {}
        self._states: dict[str, WorkspaceState] = {}
        self._contexts: dict[str, WorkspaceContext] = {}
        self._selections: dict[str, WorkspaceSelection] = {}
        self._navigation: dict[str, NavigationState] = {}
        self._snapshots: dict[str, SessionSnapshot] = {}
        self._open_views: dict[str, OpenView] = {}
        self._open_panels: dict[str, OpenPanel] = {}
        self._commands: dict[str, CommandDefinition] = {}
        self._view_defs: dict[str, ViewDefinition] = {}
        self._panel_defs: dict[str, PanelDefinition] = {}


_storage = InMemoryStorage()


class WorkspaceRuntime:
    """Main workspace runtime."""
    
    def create_workspace(
        self,
        name: str,
        owner_id: str,
        description: str = "",
    ) -> Workspace:
        """Create new workspace."""
        workspace = Workspace(
            id=str(uuid4()),
            name=name,
            description=description,
            owner_id=owner_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._workspaces[workspace.id] = workspace
        return workspace
    
    def get_workspace(self, workspace_id: str) -> Workspace | None:
        """Get workspace by ID."""
        return _storage._workspaces.get(workspace_id)
    
    def update_workspace(self, workspace: Workspace) -> Workspace:
        """Update workspace."""
        updated = Workspace(
            id=workspace.id,
            name=workspace.name,
            description=workspace.description,
            owner_id=workspace.owner_id,
            status=workspace.status,
            layouts=workspace.layouts,
            current_layout_id=workspace.current_layout_id,
            preferences=workspace.preferences,
            context=workspace.context,
            tags=workspace.tags,
            created_at=workspace.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=workspace.version + 1,
            metadata=workspace.metadata,
            author=workspace.author,
            reason=workspace.reason,
            revision_history=workspace.revision_history,
        )
        _storage._workspaces[updated.id] = updated
        return updated
    
    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete workspace."""
        if workspace_id in _storage._workspaces:
            del _storage._workspaces[workspace_id]
            return True
        return False
    
    def list_workspaces(self) -> list[Workspace]:
        """List all workspaces."""
        return list(_storage._workspaces.values())


class WorkspaceSessionManager:
    """Manages workspace sessions."""
    
    def create_session(
        self,
        workspace_id: str,
        user_id: str,
    ) -> WorkspaceSession:
        """Create new session."""
        session = WorkspaceSession(
            id=str(uuid4()),
            workspace_id=workspace_id,
            user_id=user_id,
            status="active",
            started_at=datetime.now(timezone.utc).isoformat(),
            last_activity=datetime.now(timezone.utc).isoformat(),
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._sessions[session.id] = session
        return session
    
    def get_session(self, session_id: str) -> WorkspaceSession | None:
        """Get session by ID."""
        return _storage._sessions.get(session_id)
    
    def end_session(self, session_id: str) -> WorkspaceSession | None:
        """End session."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        ended = WorkspaceSession(
            id=session.id,
            workspace_id=session.workspace_id,
            user_id=session.user_id,
            status="closed",
            started_at=session.started_at,
            ended_at=datetime.now(timezone.utc).isoformat(),
            last_activity=session.last_activity,
            idle_time=session.idle_time,
            snapshots=session.snapshots,
            current_snapshot_id=session.current_snapshot_id,
            is_recovery=session.is_recovery,
            parent_session_id=session.parent_session_id,
            created_at=session.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=session.version + 1,
            metadata=session.metadata,
            author=session.author,
            reason=session.reason,
        )
        _storage._sessions[ended.id] = ended
        return ended
    
    def list_sessions(self, workspace_id: str) -> list[WorkspaceSession]:
        """List sessions by workspace."""
        return [
            s for s in _storage._sessions.values()
            if s.workspace_id == workspace_id
        ]


class WorkspaceContextManager:
    """Manages workspace context."""
    
    def create_context(
        self,
        workspace_id: str,
        entity_id: str,
        entity_type: str,
        view_type: str,
    ) -> WorkspaceContext:
        """Create new context."""
        context = WorkspaceContext(
            id=str(uuid4()),
            workspace_id=workspace_id,
            entity_id=entity_id,
            entity_type=entity_type,
            view_type=view_type,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._contexts[context.id] = context
        return context
    
    def get_context(self, context_id: str) -> WorkspaceContext | None:
        """Get context by ID."""
        return _storage._contexts.get(context_id)
    
    def update_context(
        self,
        context: WorkspaceContext,
        **kwargs: Any,
    ) -> WorkspaceContext:
        """Update context."""
        updated = WorkspaceContext(
            id=context.id,
            workspace_id=context.workspace_id,
            entity_id=kwargs.get("entity_id", context.entity_id),
            entity_type=kwargs.get("entity_type", context.entity_type),
            view_type=kwargs.get("view_type", context.view_type),
            panel_ids=kwargs.get("panel_ids", context.panel_ids),
            parameters=kwargs.get("parameters", context.parameters),
            created_at=context.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=context.version + 1,
            metadata=context.metadata,
        )
        _storage._contexts[updated.id] = updated
        return updated


class WorkspaceNavigationManager:
    """Manages workspace navigation."""
    
    def create_navigation_state(
        self,
        workspace_id: str,
    ) -> NavigationState:
        """Create navigation state."""
        state = NavigationState(
            id=str(uuid4()),
            workspace_id=workspace_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._navigation[state.id] = state
        return state
    
    def get_navigation_state(
        self,
        workspace_id: str,
    ) -> NavigationState | None:
        """Get navigation state by workspace."""
        for state in _storage._navigation.values():
            if state.workspace_id == workspace_id:
                return state
        return None
    
    def navigate_to(
        self,
        workspace_id: str,
        node_id: str,
    ) -> NavigationState | None:
        """Navigate to node."""
        state = self.get_navigation_state(workspace_id)
        if not state:
            state = self.create_navigation_state(workspace_id)
        
        updated = NavigationState(
            id=state.id,
            workspace_id=workspace_id,
            current_node_id=node_id,
            breadcrumbs=state.breadcrumbs,
            expanded_nodes=state.expanded_nodes,
            selected_nodes=state.selected_nodes,
            created_at=state.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=state.version + 1,
            metadata=state.metadata,
        )
        _storage._navigation[updated.id] = updated
        return updated


class WorkspaceStateManager:
    """Manages workspace state."""
    
    def create_state(
        self,
        workspace_id: str,
    ) -> WorkspaceState:
        """Create state."""
        state = WorkspaceState(
            state_id=str(uuid4()),
            workspace_id=workspace_id,
            active_view="",
            active_panel="",
            selections=(),
            context={},
            scroll_positions={},
            expanded_nodes=(),
        )
        _storage._states[state.state_id] = state
        return state
    
    def get_state(self, workspace_id: str) -> WorkspaceState | None:
        """Get state by workspace."""
        for state in _storage._states.values():
            if state.workspace_id == workspace_id:
                return state
        return None
    
    def update_state(
        self,
        state: WorkspaceState,
        **kwargs: Any,
    ) -> WorkspaceState:
        """Update state."""
        updated = WorkspaceState(
            state_id=state.state_id,
            workspace_id=state.workspace_id,
            active_view=kwargs.get("active_view", state.active_view),
            active_panel=kwargs.get("active_panel", state.active_panel),
            selections=kwargs.get("selections", state.selections),
            context=kwargs.get("context", state.context),
            scroll_positions=kwargs.get("scroll_positions", state.scroll_positions),
            expanded_nodes=kwargs.get("expanded_nodes", state.expanded_nodes),
        )
        _storage._states[updated.state_id] = updated
        return updated


class WorkspaceCommandDispatcher:
    """Dispatches workspace commands."""
    
    def register_command(self, command: CommandDefinition) -> None:
        """Register command."""
        _storage._commands[command.id] = command
    
    def get_command(self, command_id: str) -> CommandDefinition | None:
        """Get command."""
        return _storage._commands.get(command_id)
    
    def dispatch(
        self,
        command_name: str,
        workspace_id: str,
        session_id: str,
        parameters: dict[str, Any] = None,
    ) -> CommandExecution:
        """Dispatch command."""
        execution = CommandExecution(
            workspace_id=workspace_id,
            session_id=session_id,
            command_name=command_name,
            parameters=parameters or {},
            result={},
            success=True,
            error="",
            duration_ms=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return execution
    
    def list_commands(self) -> list[CommandDefinition]:
        """List all commands."""
        return list(_storage._commands.values())


class WorkspaceLifecycleManager:
    """Manages workspace lifecycle."""
    
    def load_workspace(self, workspace_id: str) -> Workspace | None:
        """Load workspace."""
        return WorkspaceRuntime().get_workspace(workspace_id)
    
    def save_workspace(self, workspace: Workspace) -> Workspace:
        """Save workspace."""
        return WorkspaceRuntime().update_workspace(workspace)
    
    def close_workspace(self, workspace_id: str) -> bool:
        """Close workspace."""
        workspace = WorkspaceRuntime().get_workspace(workspace_id)
        if not workspace:
            return False
        
        updated = WorkspaceRuntime().update_workspace(
            Workspace(
                id=workspace.id,
                name=workspace.name,
                description=workspace.description,
                owner_id=workspace.owner_id,
                status="closed",
                layouts=workspace.layouts,
                current_layout_id=workspace.current_layout_id,
                preferences=workspace.preferences,
                context=workspace.context,
                tags=workspace.tags,
                created_at=workspace.created_at,
                modified_at=datetime.now(timezone.utc).isoformat(),
                version=workspace.version + 1,
                metadata=workspace.metadata,
                author=workspace.author,
                reason=workspace.reason,
                revision_history=workspace.revision_history,
            )
        )
        return updated is not None


class ViewRegistry:
    """Registry for view definitions."""
    
    def register(self, view: ViewDefinition) -> None:
        """Register view."""
        _storage._view_defs[view.id] = view
    
    def get(self, view_id: str) -> ViewDefinition | None:
        """Get view."""
        return _storage._view_defs.get(view_id)
    
    def list_by_type(self, view_type: str) -> list[ViewDefinition]:
        """List views by type."""
        return [
            v for v in _storage._view_defs.values()
            if v.view_type == view_type
        ]
    
    def list_all(self) -> list[ViewDefinition]:
        """List all views."""
        return list(_storage._view_defs.values())


class PanelRegistry:
    """Registry for panel definitions."""
    
    def register(self, panel: PanelDefinition) -> None:
        """Register panel."""
        _storage._panel_defs[panel.id] = panel
    
    def get(self, panel_id: str) -> PanelDefinition | None:
        """Get panel."""
        return _storage._panel_defs.get(panel_id)
    
    def list_by_type(self, panel_type: str) -> list[PanelDefinition]:
        """List panels by type."""
        return [
            p for p in _storage._panel_defs.values()
            if p.panel_type == panel_type
        ]
    
    def list_all(self) -> list[PanelDefinition]:
        """List all panels."""
        return list(_storage._panel_defs.values())
