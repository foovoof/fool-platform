"""
fool_platform/agents/base/validation.py

Agent Validation for FOOL Platform.

Provides validators for agent tasks, results, and capabilities.
"""
from dataclasses import dataclass, field
from typing import Any

from fool_platform.agents.base.models import (
    AgentCapability,
    AgentResult,
    AgentResultStatus,
    AgentTask,
    AgentTaskStatus,
)


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def success(cls) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True)

    @classmethod
    def failure(cls, errors: list[str]) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=errors)

    def add_error(self, error: str) -> "ValidationResult":
        """Add an error to the result."""
        self.errors.append(error)
        self.is_valid = False
        return self

    def add_warning(self, warning: str) -> "ValidationResult":
        """Add a warning to the result."""
        self.warnings.append(warning)
        return self


class AgentTaskValidator:
    """
    Validates agent tasks.
    """

    @staticmethod
    def validate(task: AgentTask) -> ValidationResult:
        """
        Validate an agent task.
        
        Args:
            task: The task to validate
            
        Returns:
            ValidationResult with errors if any
        """
        result = ValidationResult.success()

        if not task.task_id:
            result.add_error("Task must have a task_id")

        if not task.task_type:
            result.add_error("Task must have a task_type")

        if not task.objective:
            result.add_error("Task must have an objective")

        if not task.trace_id:
            result.add_error("Task must have a trace_id")

        if not isinstance(task.inputs, dict):
            result.add_error("Task inputs must be a dictionary")

        if not isinstance(task.metadata, dict):
            result.add_error("Task metadata must be a dictionary")

        if task.created_at:
            if not AgentTaskValidator._is_valid_iso_timestamp(task.created_at):
                result.add_error("Task created_at must be a valid ISO timestamp")

        return result

    @staticmethod
    def _is_valid_iso_timestamp(value: str) -> bool:
        """Check if a string is a valid ISO timestamp."""
        try:
            from datetime import datetime
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except (ValueError, AttributeError):
            return False


class AgentResultValidator:
    """
    Validates agent results.
    """

    @staticmethod
    def validate(result: AgentResult) -> ValidationResult:
        """
        Validate an agent result.
        
        Args:
            result: The result to validate
            
        Returns:
            ValidationResult with errors if any
        """
        validation = ValidationResult.success()

        if not result.result_id:
            validation.add_error("Result must have a result_id")

        if not result.task_id:
            validation.add_error("Result must have a task_id")

        if not result.agent_id:
            validation.add_error("Result must have an agent_id")

        if not isinstance(result.status, AgentResultStatus):
            validation.add_error("Result must have a valid status")

        if not isinstance(result.outputs, dict):
            validation.add_error("Result outputs must be a dictionary")

        if not isinstance(result.errors, list):
            validation.add_error("Result errors must be a list")

        if not isinstance(result.warnings, list):
            validation.add_error("Result warnings must be a list")

        if result.confidence is not None:
            if not isinstance(result.confidence, (int, float)):
                validation.add_error("Result confidence must be a number")
            elif not (0.0 <= result.confidence <= 1.0):
                validation.add_error("Result confidence must be between 0.0 and 1.0")

        return validation

    @staticmethod
    def validate_task_result_relationship(
        task: AgentTask, result: AgentResult
    ) -> ValidationResult:
        """
        Validate the relationship between task and result.
        
        Args:
            task: The original task
            result: The result to validate
            
        Returns:
            ValidationResult with errors if any
        """
        validation = ValidationResult.success()

        if result.task_id != task.task_id:
            validation.add_error(
                f"Result task_id {result.task_id} does not match task task_id {task.task_id}"
            )

        if not result.started_at:
            validation.add_error("Result must have a started_at timestamp")

        if not result.completed_at:
            validation.add_error("Result must have a completed_at timestamp")

        if result.started_at and result.completed_at:
            if result.started_at > result.completed_at:
                validation.add_error("Result started_at must be before completed_at")

        return validation


class AgentCapabilityValidator:
    """
    Validates agent capabilities.
    """

    @staticmethod
    def validate(capability: AgentCapability) -> ValidationResult:
        """
        Validate an agent capability.
        
        Args:
            capability: The capability to validate
            
        Returns:
            ValidationResult with errors if any
        """
        result = ValidationResult.success()

        if not capability.capability_id:
            result.add_error("Capability must have a capability_id")

        if not capability.name:
            result.add_error("Capability must have a name")

        if not capability.version:
            result.add_warning("Capability should have a version")

        if not isinstance(capability.inputs, dict):
            result.add_error("Capability inputs must be a dictionary")

        if not isinstance(capability.outputs, dict):
            result.add_error("Capability outputs must be a dictionary")

        if not isinstance(capability.metadata, dict):
            result.add_error("Capability metadata must be a dictionary")

        return result

    @staticmethod
    def validate_manifest(
        capabilities: list[AgentCapability]
    ) -> ValidationResult:
        """
        Validate a capability manifest.
        
        Args:
            capabilities: List of capabilities to validate
            
        Returns:
            ValidationResult with errors if any
        """
        result = ValidationResult.success()

        if not capabilities:
            result.add_warning("Capability manifest is empty")

        capability_ids: set[str] = set()
        for cap in capabilities:
            cap_result = AgentCapabilityValidator.validate(cap)
            if not cap_result.is_valid:
                result.errors.extend(cap_result.errors)
                result.is_valid = False

            if cap.capability_id in capability_ids:
                result.add_error(
                    f"Duplicate capability_id: {cap.capability_id}"
                )
            capability_ids.add(cap.capability_id)

        return result
