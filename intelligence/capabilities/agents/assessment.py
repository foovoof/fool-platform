"""
intelligence/capabilities/agents/assessment.py

Assessment Agent.

Reference agent for assessment capability.
"""
from __future__ import annotations

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class AssessmentAgent(BaseAgent):
    """Assessment capability agent."""
    
    agent_type: str = "assessment"
    name: str = "Assessment Agent"
    description: str = "Generic assessment capability agent"
    capability_type = CapabilityType.ASSESSMENT
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        subject = task.inputs.get("subject", "unknown")
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "subject": subject,
            "executed": True,
            "output_type": "assessment_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        result = super().execute(task)
        finding = self.create_finding(
            title="Assessment completed",
            description="Assessment capability executed",
            finding_type=FindingType.RECOMMENDATION,
            confidence=0.7,
        )
        result.add_finding(finding)
        result.outputs["evaluation"] = {"status": "completed"}
        return result
