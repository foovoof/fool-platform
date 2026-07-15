"""
fool_platform/orchestration/planner/agent_selector.py

Agent selection for workflow steps.
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from fool_platform.orchestration.orchestration_exceptions import WorkflowPlanningError
from fool_platform.orchestration.registry.agent_registry import AgentRegistry
from fool_platform.orchestration.registry.capability_registry import CapabilityRegistry
from fool_platform.orchestration.registry.workflow_registry import StepDefinition

if TYPE_CHECKING:
    from fool_platform.orchestration.registry.agent_registry import AgentDefinition


@dataclass
class AgentSelection:
    """Result of agent selection."""
    agent_id: str | None
    agent_definition: "AgentDefinition | None"
    rationale: str
    selected_by: str  # "explicit" or "capability"
    is_valid: bool


class AgentSelector:
    """
    Selects appropriate agents for workflow steps.
    
    Does not instantiate or execute agents.
    """

    def select_agent_for_step(
        self,
        step: StepDefinition,
        agent_registry: AgentRegistry,
        capability_registry: CapabilityRegistry,
    ) -> AgentSelection:
        """
        Select an agent for a step.
        
        Prefers explicitly assigned agent, otherwise selects by capability.
        
        Args:
            step: The step definition
            agent_registry: Agent registry
            capability_registry: Capability registry
            
        Returns:
            AgentSelection with selected agent and rationale
            
        Raises:
            WorkflowPlanningError: If no suitable agent found
        """
        if step.agent_type:
            return self._select_explicit_agent(
                step.agent_type,
                step,
                agent_registry,
            )
        
        if step.capability:
            return self._select_by_capability(
                step.capability,
                step,
                agent_registry,
                capability_registry,
            )
        
        return AgentSelection(
            agent_id=None,
            agent_definition=None,
            rationale="No agent type or capability specified",
            selected_by="none",
            is_valid=False,
        )

    def _select_explicit_agent(
        self,
        agent_type: str,
        step: StepDefinition,
        agent_registry: AgentRegistry,
    ) -> AgentSelection:
        """Select explicitly assigned agent."""
        if not agent_registry.has_agent(agent_type):
            raise WorkflowPlanningError(
                workflow_id="unknown",
                reason=f"Step {step.step_id} requires agent {agent_type} which is not registered",
            )
        
        agent_def = agent_registry.get_agent(agent_type)
        
        return AgentSelection(
            agent_id=agent_type,
            agent_definition=agent_def,
            rationale=f"Explicit agent assignment: {agent_type}",
            selected_by="explicit",
            is_valid=True,
        )

    def _select_by_capability(
        self,
        capability: str,
        step: StepDefinition,
        agent_registry: AgentRegistry,
        capability_registry: CapabilityRegistry,
    ) -> AgentSelection:
        """Select agent by capability."""
        if not capability_registry.has_capability(capability):
            raise WorkflowPlanningError(
                workflow_id="unknown",
                reason=f"Step {step.step_id} requires capability {capability} which is not registered",
            )
        
        agents_with_capability = agent_registry.list_agents_with_capability(capability)
        enabled_agents = agent_registry.list_enabled_agents()
        candidates = [a for a in agents_with_capability if a in enabled_agents]
        
        if not candidates:
            raise WorkflowPlanningError(
                workflow_id="unknown",
                reason=f"No enabled agent found with capability {capability} for step {step.step_id}",
            )
        
        selected_agent = candidates[0]
        agent_def = agent_registry.get_agent(selected_agent)
        
        return AgentSelection(
            agent_id=selected_agent,
            agent_definition=agent_def,
            rationale=f"Selected {selected_agent} with capability {capability}",
            selected_by="capability",
            is_valid=True,
        )
