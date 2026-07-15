"""
intelligence/services/session_service.py

Session Service.

Manages intelligence sessions.
"""
from typing import Any

from intelligence.session import IntelligenceSession
from intelligence.models import IntelligenceTask, IntelligenceResult


class SessionService:
    """
    Service for session management.
    
    Coordinates:
    - Session creation
    - Session retrieval
    - Session updates
    """
    
    def __init__(self) -> None:
        """Initialize the service."""
        self._sessions: dict[str, IntelligenceSession] = {}
    
    def create_session(
        self,
        context_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new session.
        
        Args:
            context_id: Optional context ID
            metadata: Optional metadata
            
        Returns:
            Created session
        """
        session = IntelligenceSession(
            context_id=context_id,
            metadata=metadata or {},
        )
        
        self._sessions[session.session_id] = session
        
        return session.to_dict()
    
    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get session by ID."""
        session = self._sessions.get(session_id)
        if session:
            return session.to_dict()
        return None
    
    def add_task(self, session_id: str, task: IntelligenceTask) -> bool:
        """Add task to session."""
        session = self._sessions.get(session_id)
        if session:
            session.add_task(task)
            return True
        return False
    
    def add_result(self, session_id: str, result: IntelligenceResult) -> bool:
        """Add result to session."""
        session = self._sessions.get(session_id)
        if session:
            session.add_result(result)
            return True
        return False
    
    def list_sessions(self) -> list[dict[str, Any]]:
        """List all sessions."""
        return [s.to_dict() for s in self._sessions.values()]
    
    def get_summary(self, session_id: str) -> dict[str, Any] | None:
        """Get session summary."""
        session = self._sessions.get(session_id)
        if session:
            return session.get_summary()
        return None
