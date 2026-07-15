"""
fool_platform/agents/base/events.py

Agent Event Integration for FOOL Platform.

Provides event emission for agent lifecycle and task events.
Uses platform/events contracts.
"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

if TYPE_CHECKING:
    pass


class AgentEventEmitter:
    """
    Emits agent events through the Event Bus.
    
    Supports optional EventBus integration.
    Event failures do not fail task execution.
    """

    SUPPORTED_EVENTS = [
        "agent.initialized",
        "agent.started",
        "agent.stopped",
        "agent.task.started",
        "agent.task.completed",
        "agent.task.failed",
    ]

    def __init__(self, event_bus: Any = None) -> None:
        """
        Initialize the event emitter.
        
        Args:
            event_bus: Optional EventBus instance
        """
        self._event_bus = event_bus
        self._event_count = 0
        self._failed_events: list[dict[str, Any]] = []

    @property
    def event_bus(self) -> Any:
        """Get the event bus."""
        return self._event_bus

    @property
    def has_event_bus(self) -> bool:
        """Check if an event bus is configured."""
        return self._event_bus is not None

    def emit(self, event_type: str, data: dict[str, Any]) -> bool:
        """
        Emit an event.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if emitted successfully
        """
        self._event_count += 1

        if event_type not in self.SUPPORTED_EVENTS:
            self._failed_events.append({
                "event_type": event_type,
                "data": data,
                "error": f"Unsupported event type: {event_type}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return False

        event = self._create_event(event_type, data)

        if self._event_bus is None:
            return False

        try:
            if hasattr(self._event_bus, "publish"):
                self._event_bus.publish(event_type, event)
            elif hasattr(self._event_bus, "emit"):
                self._event_bus.emit(event)
            else:
                self._failed_events.append({
                    "event_type": event_type,
                    "data": data,
                    "error": "Event bus has no publish or emit method",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return False
            return True
        except Exception as e:
            self._failed_events.append({
                "event_type": event_type,
                "data": data,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return False

    def _create_event(self, event_type: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Create an event in the platform/events format.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            Formatted event dictionary
        """
        return {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "fool_platform.agents",
            "data": data,
        }

    def emit_agent_initialized(self, agent_id: str) -> bool:
        """
        Emit agent.initialized event.
        
        Args:
            agent_id: The agent ID
            
        Returns:
            True if emitted successfully
        """
        return self.emit("agent.initialized", {"agent_id": agent_id})

    def emit_agent_started(self, agent_id: str) -> bool:
        """
        Emit agent.started event.
        
        Args:
            agent_id: The agent ID
            
        Returns:
            True if emitted successfully
        """
        return self.emit("agent.started", {"agent_id": agent_id})

    def emit_agent_stopped(self, agent_id: str) -> bool:
        """
        Emit agent.stopped event.
        
        Args:
            agent_id: The agent ID
            
        Returns:
            True if emitted successfully
        """
        return self.emit("agent.stopped", {"agent_id": agent_id})

    def emit_task_started(
        self, task_id: str, agent_id: str, task_type: str = ""
    ) -> bool:
        """
        Emit agent.task.started event.
        
        Args:
            task_id: The task ID
            agent_id: The agent ID
            task_type: Optional task type
            
        Returns:
            True if emitted successfully
        """
        data = {"task_id": task_id, "agent_id": agent_id}
        if task_type:
            data["task_type"] = task_type
        return self.emit("agent.task.started", data)

    def emit_task_completed(
        self, task_id: str, agent_id: str, result_id: str = ""
    ) -> bool:
        """
        Emit agent.task.completed event.
        
        Args:
            task_id: The task ID
            agent_id: The agent ID
            result_id: Optional result ID
            
        Returns:
            True if emitted successfully
        """
        data = {"task_id": task_id, "agent_id": agent_id}
        if result_id:
            data["result_id"] = result_id
        return self.emit("agent.task.completed", data)

    def emit_task_failed(
        self, task_id: str, agent_id: str, error: str = ""
    ) -> bool:
        """
        Emit agent.task.failed event.
        
        Args:
            task_id: The task ID
            agent_id: The agent ID
            error: Optional error message
            
        Returns:
            True if emitted successfully
        """
        data = {"task_id": task_id, "agent_id": agent_id}
        if error:
            data["error"] = error
        return self.emit("agent.task.failed", data)

    def get_event_count(self) -> int:
        """
        Get the total number of events emitted.
        
        Returns:
            Event count
        """
        return self._event_count

    def get_failed_events(self) -> list[dict[str, Any]]:
        """
        Get list of failed events.
        
        Returns:
            List of failed event records
        """
        return self._failed_events.copy()

    def clear_failed_events(self) -> None:
        """Clear the failed events list."""
        self._failed_events.clear()
