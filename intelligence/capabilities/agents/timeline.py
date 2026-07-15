"""
intelligence/capabilities/agents/timeline.py

Timeline Agent.

Reference agent for timeline capability.
"""
from __future__ import annotations

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class TimelineAgent(BaseAgent):
    """Timeline capability agent."""
    
    agent_type: str = "timeline"
    name: str = "Timeline Agent"
    description: str = "Generic timeline capability agent"
    capability_type = CapabilityType.TIMELINE
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "executed": True,
            "output_type": "timeline",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        result = super().execute(task)
        finding = self.create_finding(
            title="Timeline generated",
            description="Timeline capability executed",
            finding_type=FindingType.PATTERN,
            confidence=0.7,
        )
        result.add_finding(finding)
        result.outputs["timeline_events"] = []
        return result
