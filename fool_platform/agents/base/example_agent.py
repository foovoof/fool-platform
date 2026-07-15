"""
fool_platform/agents/base/example_agent.py

Example Agent for FOOL Platform.

Validates runtime integrity only.
No AI. No business logic. No external calls.
"""
from datetime import datetime, timezone
from typing import Any

from fool_platform.agents.base.agent import BaseAgent
from fool_platform.agents.base.context import AgentContext
from fool_platform.agents.base.models import AgentCapability, AgentResult, AgentTask


class ExampleAgent(BaseAgent):
    """
    Example agent that validates runtime behavior.
    
    Purpose: Validate that the Agent Runtime Framework works correctly.
    
    This agent:
    - Accepts AgentTask
    - Returns AgentResult
    - Echoes objective and inputs into outputs
    - No AI
    - No business logic
    - No external calls
    """

    CAPABILITY_ID = "example.echo"
    VERSION = "1.0.0"

    def __init__(
        self,
        agent_id: str = "example.echo.agent",
        name: str = "Example Echo Agent",
        description: str = "Validates runtime integrity by echoing task data",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the example agent.
        
        Args:
            agent_id: Unique agent identifier
            name: Human-readable name
            description: Agent description
            **kwargs: Additional arguments for BaseAgent
        """
        capability = AgentCapability(
            capability_id=self.CAPABILITY_ID,
            name="Echo",
            description="Echoes task objective and inputs as outputs",
            version=self.VERSION,
        )

        super().__init__(
            agent_id=agent_id,
            name=name,
            version=self.VERSION,
            description=description,
            capabilities=[capability],
            **kwargs,
        )

    def _execute(self, task: AgentTask, context: AgentContext) -> dict[str, Any]:
        """
        Execute the task by echoing the input.
        
        This method implements the agent's logic.
        It simply echoes the task data for validation.
        
        Args:
            task: The task to execute
            context: The execution context
            
        Returns:
            Task outputs containing echoed data
        """
        return {
            "echoed_objective": task.objective,
            "echoed_inputs": task.inputs,
            "echoed_task_id": task.task_id,
            "echoed_task_type": task.task_type,
            "context_id": context.context_id,
            "agent_id": self._agent_id,
            "execution_time": datetime.now(timezone.utc).isoformat(),
        }

    def can_handle(self, task: AgentTask) -> bool:
        """
        Check if this agent can handle the task.
        
        Args:
            task: The task to check
            
        Returns:
            True if task type matches capability
        """
        return task.task_type == self.CAPABILITY_ID or not task.task_type

    def validate_task(self, task: AgentTask) -> list[str]:
        """
        Validate the task.
        
        Args:
            task: The task to validate
            
        Returns:
            List of validation errors
        """
        errors = super().validate_task(task)
        if not task.objective:
            errors.append("ExampleAgent requires an objective")
        return errors


class EchoAgent(ExampleAgent):
    """
    Alias for ExampleAgent.
    
    Provides a simpler name for testing.
    """
    pass
