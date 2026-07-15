"""
intelligence/capabilities/validation/__init__.py

Capability Validators.

Validates capability structures, tasks, results, and compatibility.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from intelligence.capabilities.models import (
    CapabilityDefinition,
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    CapabilityStatus,
)
from intelligence.capabilities.agents import BaseAgent


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str = "error"
    code: str = ""
    message: str = ""
    path: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, code: str, message: str, path: str = "") -> None:
        """Add an error."""
        self.is_valid = False
        self.issues.append(ValidationIssue(
            severity="error",
            code=code,
            message=message,
            path=path,
        ))
    
    def add_warning(self, code: str, message: str, path: str = "") -> None:
        """Add a warning."""
        self.issues.append(ValidationIssue(
            severity="warning",
            code=code,
            message=message,
            path=path,
        ))
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [i.to_dict() for i in self.issues],
            "metadata": self.metadata,
        }


class CapabilityValidator:
    """Validates capability definitions."""
    
    def validate(self, capability: CapabilityDefinition) -> ValidationResult:
        """
        Validate a capability definition.
        
        Args:
            capability: Capability to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not capability.capability_id:
            result.add_error(
                "MISSING_ID",
                "Capability must have an ID",
                "capability_id",
            )
        
        if not capability.name:
            result.add_error(
                "MISSING_NAME",
                "Capability must have a name",
                "name",
            )
        
        if not capability.description:
            result.add_warning(
                "MISSING_DESCRIPTION",
                "Capability should have a description",
                "description",
            )
        
        if not capability.capability_type:
            result.add_error(
                "MISSING_TYPE",
                "Capability must have a type",
                "capability_type",
            )
        
        return result


class TaskValidator:
    """Validates capability tasks."""
    
    def validate(self, task: CapabilityTask) -> ValidationResult:
        """
        Validate a capability task.
        
        Args:
            task: Task to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not task.task_id:
            result.add_error(
                "MISSING_TASK_ID",
                "Task must have a task_id",
                "task_id",
            )
        
        if not task.capability_id:
            result.add_error(
                "MISSING_CAPABILITY_ID",
                "Task must have a capability_id",
                "capability_id",
            )
        
        if not task.capability_type:
            result.add_error(
                "MISSING_TYPE",
                "Task must have a capability_type",
                "capability_type",
            )
        
        if not task.objective:
            result.add_warning(
                "MISSING_OBJECTIVE",
                "Task should have an objective",
                "objective",
            )
        
        return result


class ResultValidator:
    """Validates capability results."""
    
    def validate(self, result: CapabilityResult) -> ValidationResult:
        """
        Validate a capability result.
        
        Args:
            result: Result to validate
            
        Returns:
            Validation result
        """
        result_validation = ValidationResult()
        
        if not result.result_id:
            result_validation.add_error(
                "MISSING_RESULT_ID",
                "Result must have a result_id",
                "result_id",
            )
        
        if not result.task_id:
            result_validation.add_error(
                "MISSING_TASK_ID",
                "Result must have a task_id",
                "task_id",
            )
        
        if result.status == CapabilityStatus.FAILED and not result.errors:
            result_validation.add_warning(
                "NO_ERRORS",
                "Failed result should have error messages",
                "errors",
            )
        
        for i, finding in enumerate(result.findings):
            if not finding.title:
                result_validation.add_warning(
                    "MISSING_TITLE",
                    f"Finding {i} should have a title",
                    f"findings[{i}].title",
                )
            
            if finding.confidence < 0 or finding.confidence > 1:
                result_validation.add_error(
                    "INVALID_CONFIDENCE",
                    f"Finding {i} confidence must be between 0 and 1",
                    f"findings[{i}].confidence",
                )
        
        return result_validation


class PipelineValidator:
    """Validates capability pipelines."""
    
    def validate(self, pipeline) -> ValidationResult:
        """
        Validate a capability pipeline.
        
        Args:
            pipeline: Pipeline to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not pipeline.name:
            result.add_error(
                "MISSING_NAME",
                "Pipeline must have a name",
                "name",
            )
        
        if not pipeline.steps:
            result.add_error(
                "NO_STEPS",
                "Pipeline must have at least one step",
                "steps",
            )
        
        for i, step in enumerate(pipeline.steps):
            if not step.name:
                result.add_error(
                    "MISSING_STEP_NAME",
                    f"Step {i} must have a name",
                    f"steps[{i}].name",
                )
        
        return result


class AgentValidator:
    """Validates agent compatibility."""
    
    def validate(
        self,
        agent: BaseAgent,
        capability_type: CapabilityType,
    ) -> ValidationResult:
        """
        Validate agent is compatible with capability type.
        
        Args:
            agent: Agent to validate
            capability_type: Expected capability type
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not agent.agent_id:
            result.add_error(
                "MISSING_AGENT_ID",
                "Agent must have an agent_id",
                "agent_id",
            )
        
        if agent.capability_type != capability_type:
            result.add_warning(
                "TYPE_MISMATCH",
                f"Agent type {agent.capability_type} does not match {capability_type}",
                "capability_type",
            )
        
        return result


class CompatibilityValidator:
    """Validates capability compatibility."""
    
    def validate(
        self,
        capability: CapabilityDefinition,
        task: CapabilityTask,
    ) -> ValidationResult:
        """
        Validate capability and task are compatible.
        
        Args:
            capability: Capability definition
            task: Task to execute
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if capability.capability_type != task.capability_type:
            result.add_error(
                "TYPE_MISMATCH",
                f"Capability type {capability.capability_type} does not match task type {task.capability_type}",
                "capability_type",
            )
        
        for required_input in capability.inputs.keys():
            if required_input not in task.inputs:
                result.add_warning(
                    "MISSING_INPUT",
                    f"Task missing required input: {required_input}",
                    f"inputs.{required_input}",
                )
        
        return result
