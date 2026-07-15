"""
intelligence/context.py

Intelligence Context.

Provides execution context for the Intelligence Runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class IntelligenceContext:
    """
    Provides context for intelligence execution.
    
    Context holds:
    - Workflow identifiers
    - Execution identifiers
    - Graph reference
    - Inference session reference
    - Agent execution context
    - Metadata
    """
    context_id: str = field(default_factory=lambda: str(uuid4()))
    workflow_id: str | None = None
    execution_id: str | None = None
    session_id: str | None = None
    graph_id: str | None = None
    inference_session_id: str | None = None
    agent_execution_id: str | None = None
    parent_context_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def create_child(
        self,
        workflow_id: str | None = None,
        execution_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> IntelligenceContext:
        """
        Create a child context.
        
        Args:
            workflow_id: Optional workflow ID
            execution_id: Optional execution ID
            metadata: Optional metadata
            
        Returns:
            New child context
        """
        return IntelligenceContext(
            workflow_id=workflow_id or self.workflow_id,
            execution_id=execution_id,
            session_id=self.session_id,
            graph_id=self.graph_id,
            inference_session_id=self.inference_session_id,
            agent_execution_id=self.agent_execution_id,
            parent_context_id=self.context_id,
            metadata=metadata or {},
        )
    
    def to_event_context(self) -> dict[str, Any]:
        """
        Convert to event context format.
        
        Returns:
            Dictionary suitable for event emission
        """
        return {
            "context_id": self.context_id,
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "session_id": self.session_id,
            "graph_id": self.graph_id,
            "inference_session_id": self.inference_session_id,
            "agent_execution_id": self.agent_execution_id,
            "parent_context_id": self.parent_context_id,
            "metadata": self.metadata,
        }
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "context_id": self.context_id,
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "session_id": self.session_id,
            "graph_id": self.graph_id,
            "inference_session_id": self.inference_session_id,
            "agent_execution_id": self.agent_execution_id,
            "parent_context_id": self.parent_context_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceContext:
        """Create from dictionary."""
        return cls(**data)
