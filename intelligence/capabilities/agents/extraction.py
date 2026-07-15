"""
intelligence/capabilities/agents/extraction.py

Extraction Agent.

Reference agent for extraction capability.
"""
from __future__ import annotations

from typing import Any

from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    FindingType,
)


class ExtractionAgent(BaseAgent):
    """Extraction capability agent."""
    
    agent_type: str = "extraction"
    name: str = "Extraction Agent"
    description: str = "Generic extraction capability agent"
    capability_type = CapabilityType.EXTRACTION
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        """Generate deterministic extraction outputs."""
        source = task.inputs.get("source", "unknown")
        pattern = task.inputs.get("pattern", "default")
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "source": source,
            "pattern": pattern,
            "executed": True,
            "output_type": "extraction_result",
        }
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """Execute extraction task."""
        result = super().execute(task)
        
        finding = self.create_finding(
            title="Extraction completed",
            description=f"Extraction capability executed for source",
            finding_type=FindingType.OBSERVATION,
            confidence=0.7,
        )
        result.add_finding(finding)
        
        result.outputs["data_extracted"] = {}
        result.outputs["extraction_type"] = "generic"
        
        return result
