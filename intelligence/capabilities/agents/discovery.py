"""
intelligence/capabilities/agents/discovery.py

Discovery Agent.

Reference agent for discovery capability.
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


class DiscoveryAgent(BaseAgent):
    """
    Discovery capability agent.
    
    Demonstrates runtime integration for discovery tasks.
    """
    
    agent_type: str = "discovery"
    name: str = "Discovery Agent"
    description: str = "Generic discovery capability agent"
    capability_type = CapabilityType.DISCOVERY
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        """Generate deterministic discovery outputs."""
        criteria = task.inputs.get("criteria", {})
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "criteria": criteria,
            "executed": True,
            "output_type": "discovery_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """Execute discovery task."""
        result = super().execute(task)
        
        criteria = task.inputs.get("criteria", {})
        
        finding = self.create_finding(
            title="Discovery completed",
            description=f"Discovery capability executed with criteria: {criteria}",
            finding_type=FindingType.OBSERVATION,
            confidence=0.7,
        )
        result.add_finding(finding)
        
        result.outputs["entities_found"] = 0
        result.outputs["discovery_type"] = "generic"
        
        return result
