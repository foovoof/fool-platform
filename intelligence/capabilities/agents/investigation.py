"""
intelligence/capabilities/agents/investigation.py

Investigation Agent.

Reference agent for investigation capability.
"""
from __future__ import annotations

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class InvestigationAgent(BaseAgent):
    """Investigation capability agent."""
    
    agent_type: str = "investigation"
    name: str = "Investigation Agent"
    description: str = "Generic investigation capability agent"
    capability_type = CapabilityType.INVESTIGATION
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        target = task.inputs.get("target", "unknown")
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "target": target,
            "executed": True,
            "output_type": "investigation_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        result = super().execute(task)
        finding = self.create_finding(
            title="Investigation completed",
            description="Investigation capability executed",
            finding_type=FindingType.CONCLUSION,
            confidence=0.8,
        )
        result.add_finding(finding)
        result.outputs["findings_count"] = 1
        return result
