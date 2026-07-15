"""
fool_platform/agents/base/lifecycle.py

Agent Lifecycle Management for FOOL Platform.

Provides lifecycle state machine for agents.
"""
from datetime import datetime, timezone

from fool_platform.agents.base.agent_exceptions import AgentLifecycleError
from fool_platform.agents.base.models import AgentStatus


VALID_TRANSITIONS: dict[AgentStatus, set[AgentStatus]] = {
    AgentStatus.CREATED: {AgentStatus.INITIALIZED},
    AgentStatus.INITIALIZED: {AgentStatus.RUNNING, AgentStatus.STOPPED},
    AgentStatus.RUNNING: {
        AgentStatus.STOPPED,
        AgentStatus.FAILED,
        AgentStatus.INITIALIZED,
    },
    AgentStatus.STOPPED: {AgentStatus.INITIALIZED},
    AgentStatus.FAILED: {AgentStatus.INITIALIZED},
}


class AgentLifecycleManager:
    """
    Manages agent lifecycle state transitions.
    
    Validates state transitions before applying them.
    """

    @staticmethod
    def validate_transition(
        current: AgentStatus, target: AgentStatus
    ) -> None:
        """
        Validate a state transition.
        
        Args:
            current: Current status
            target: Target status
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        if target not in VALID_TRANSITIONS.get(current, set()):
            raise AgentLifecycleError(
                f"Invalid transition from {current.value} to {target.value}",
                current_status=current.value,
                target_status=target.value,
            )

    @staticmethod
    def initialize_agent(agent: "BaseAgent") -> None:
        """
        Initialize an agent.
        
        Args:
            agent: The agent to initialize
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.INITIALIZED
        )

    @staticmethod
    def start_agent(agent: "BaseAgent") -> None:
        """
        Start an agent.
        
        Args:
            agent: The agent to start
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        if agent.status == AgentStatus.CREATED:
            AgentLifecycleManager.initialize_agent(agent)
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.RUNNING
        )

    @staticmethod
    def stop_agent(agent: "BaseAgent") -> None:
        """
        Stop an agent.
        
        Args:
            agent: The agent to stop
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.STOPPED
        )

    @staticmethod
    def mark_running(agent: "BaseAgent") -> None:
        """
        Mark an agent as running.
        
        Args:
            agent: The agent
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.RUNNING
        )

    @staticmethod
    def mark_succeeded(agent: "BaseAgent") -> None:
        """
        Mark an agent as succeeded (returns to initialized).
        
        Args:
            agent: The agent
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.INITIALIZED
        )

    @staticmethod
    def mark_failed(agent: "BaseAgent") -> None:
        """
        Mark an agent as failed.
        
        Args:
            agent: The agent
            
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        AgentLifecycleManager.validate_transition(
            agent.status, AgentStatus.FAILED
        )
