"""
intelligence/capabilities/agents/evidence_analysis.py

Evidence Analysis Agent.

Reference agent for evidence analysis capability.
"""
from __future__ import annotations

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class EvidenceAnalysisAgent(BaseAgent):
    """Evidence Analysis capability agent."""
    
    agent_type: str = "evidence_analysis"
    name: str = "Evidence Analysis Agent"
    description: str = "Generic evidence analysis capability agent"
    capability_type = CapabilityType.EVIDENCE_ANALYSIS
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "executed": True,
            "output_type": "evidence_analysis",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        result = super().execute(task)
        finding = self.create_finding(
            title="Evidence analyzed",
            description="Evidence analysis capability executed",
            finding_type=FindingType.ANOMALY,
            confidence=0.6,
        )
        result.add_finding(finding)
        result.outputs["analysis_summary"] = {"status": "completed"}
        return result
