"""
intelligence/capabilities/agents/correlation.py

Correlation Agent.

Reference agent for correlation capability.
"""
from __future__ import annotations

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class CorrelationAgent(BaseAgent):
    """Correlation capability agent."""
    
    agent_type: str = "correlation"
    name: str = "Correlation Agent"
    description: str = "Generic correlation capability agent"
    capability_type = CapabilityType.CORRELATION
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "executed": True,
            "output_type": "correlation_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        result = super().execute(task)
        finding = self.create_finding(
            title="Correlation completed",
            description="Correlation capability executed",
            finding_type=FindingType.CORRELATION,
            confidence=0.7,
        )
        result.add_finding(finding)
        result.outputs["relationships_found"] = 0
        return result
