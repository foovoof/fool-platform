"""
intelligence/capabilities/agents/research.py

Research Agent.

Reference agent for research capability.
"""
from __future__ import annotations

from typing import Any

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityFinding,
    CapabilityArtifact,
    CapabilityType,
    FindingType,
)


class ResearchAgent(BaseAgent):
    """
    Research capability agent.
    
    Demonstrates runtime integration for research tasks.
    Outputs are deterministic and in-memory.
    """
    
    agent_type: str = "research"
    name: str = "Research Agent"
    description: str = "Generic research capability agent"
    capability_type = CapabilityType.RESEARCH
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        """Generate deterministic research outputs."""
        topic = task.inputs.get("topic", task.objective)
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "topic": topic,
            "executed": True,
            "phase": "completed",
            "output_type": "research_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """Execute research task."""
        result = super().execute(task)
        
        topic = task.inputs.get("topic", task.objective)
        
        finding = self.create_finding(
            title=f"Research completed for: {topic}",
            description=f"Research capability executed successfully for topic '{topic}'",
            finding_type=FindingType.CONCLUSION,
            confidence=0.8,
        )
        result.add_finding(finding)
        
        artifact = self.create_artifact(
            artifact_type="research_data",
            name=f"Research Data - {topic}",
            content={
                "topic": topic,
                "status": "completed",
                "timestamp": task.created_at,
            },
        )
        result.artifacts.append(artifact)
        
        result.outputs["findings_count"] = len(result.findings)
        result.outputs["artifacts_count"] = len(result.artifacts)
        
        return result
