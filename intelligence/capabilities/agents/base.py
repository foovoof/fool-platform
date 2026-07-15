"""
intelligence/capabilities/agents/base.py

Base Agent for Intelligence Capabilities.

Provides common functionality for reference agents.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityFinding,
    CapabilityArtifact,
    CapabilityType,
    CapabilityStatus,
    FindingType,
)


@dataclass
class BaseAgent:
    """
    Base class for intelligence capability agents.
    
    Reference agents demonstrate runtime integration only.
    Outputs are deterministic and in-memory.
    """
    agent_id: str = field(default_factory=lambda: str(uuid4()))
    agent_type: str = "base"
    name: str = "Base Agent"
    description: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """
        Execute the agent on a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        result = CapabilityResult(
            task_id=task.task_id,
            capability_id=task.capability_id,
            capability_type=task.capability_type,
        )
        
        result.status = CapabilityStatus.COMPLETED
        result.outputs = self._generate_outputs(task)
        
        return result
    
    def _generate_outputs(self, task: CapabilityTask) -> dict[str, Any]:
        """
        Generate deterministic outputs.
        
        Override in subclasses.
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "task_id": task.task_id,
            "executed": True,
        }
    
    def validate_task(self, task: CapabilityTask) -> tuple[bool, list[str]]:
        """
        Validate task before execution.
        
        Args:
            task: Task to validate
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        if not task.task_id:
            errors.append("Task must have a task_id")
        
        if not task.capability_id:
            errors.append("Task must have a capability_id")
        
        if not task.objective:
            errors.append("Task must have an objective")
        
        return len(errors) == 0, errors
    
    def create_finding(
        self,
        title: str,
        description: str,
        finding_type: FindingType = FindingType.OBSERVATION,
        confidence: float = 0.5,
    ) -> CapabilityFinding:
        """Create a finding."""
        return CapabilityFinding(
            finding_type=finding_type,
            title=title,
            description=description,
            confidence=confidence,
            task_id=self.agent_id,
        )
    
    def create_artifact(
        self,
        artifact_type: str,
        name: str,
        content: Any,
    ) -> CapabilityArtifact:
        """Create an artifact."""
        return CapabilityArtifact(
            artifact_type=artifact_type,
            name=name,
            content=content,
            capability_id=self.agent_id,
        )
