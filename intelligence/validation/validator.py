"""
intelligence/validation/validator.py

Runtime Validator.

Validates runtime components.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from intelligence.models import IntelligenceTask
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.pipeline import Pipeline


@dataclass
class ValidationIssue:
    """A validation issue."""
    issue_type: str
    severity: str
    message: str
    location: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool
    entity_id: str
    issues: list[ValidationIssue] = field(default_factory=list)
    entity_type: str = ""
    
    def add_issue(
        self,
        issue_type: str,
        severity: str,
        message: str,
        location: str = "",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add a validation issue."""
        self.issues.append(ValidationIssue(
            issue_type=issue_type,
            severity=severity,
            message=message,
            location=location,
            details=details or {},
        ))
        if severity == "error":
            self.is_valid = False
    
    def add_warning(
        self,
        issue_type: str,
        message: str,
        location: str = "",
    ) -> None:
        """Add a warning."""
        self.add_issue(issue_type, "warning", message, location)


class RuntimeValidator:
    """
    Validates runtime components.
    
    Validates:
    - Task structure
    - Pipeline consistency
    - Runtime consistency
    - Session consistency
    - Contract compatibility
    """
    
    def validate_task(self, task: IntelligenceTask) -> ValidationResult:
        """
        Validate an intelligence task.
        
        Args:
            task: Task to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult(
            is_valid=True,
            entity_id=task.task_id,
            entity_type="task",
        )
        
        if not task.task_id:
            result.add_issue(
                "missing_id",
                "error",
                "Task must have a task_id",
            )
        
        if not task.task_type:
            result.add_issue(
                "missing_type",
                "error",
                "Task must have a task_type",
            )
        
        if not task.objective:
            result.add_issue(
                "missing_objective",
                "error",
                "Task must have an objective",
            )
        
        return result
    
    def validate_context(
        self,
        context: IntelligenceContext,
    ) -> ValidationResult:
        """
        Validate an intelligence context.
        
        Args:
            context: Context to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult(
            is_valid=True,
            entity_id=context.context_id,
            entity_type="context",
        )
        
        if not context.context_id:
            result.add_issue(
                "missing_id",
                "error",
                "Context must have a context_id",
            )
        
        return result
    
    def validate_session(
        self,
        session: IntelligenceSession,
    ) -> ValidationResult:
        """
        Validate an intelligence session.
        
        Args:
            session: Session to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult(
            is_valid=True,
            entity_id=session.session_id,
            entity_type="session",
        )
        
        if not session.session_id:
            result.add_issue(
                "missing_id",
                "error",
                "Session must have a session_id",
            )
        
        if not session.started_at:
            result.add_warning(
                "missing_start_time",
                "Session should have a started_at timestamp",
            )
        
        return result
    
    def validate_pipeline(self, pipeline: Pipeline) -> ValidationResult:
        """
        Validate a pipeline.
        
        Args:
            pipeline: Pipeline to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult(
            is_valid=True,
            entity_id=pipeline.pipeline_id,
            entity_type="pipeline",
        )
        
        if not pipeline.pipeline_id:
            result.add_issue(
                "missing_id",
                "error",
                "Pipeline must have a pipeline_id",
            )
        
        if not pipeline.name:
            result.add_issue(
                "missing_name",
                "error",
                "Pipeline must have a name",
            )
        
        if not pipeline.steps:
            result.add_issue(
                "no_steps",
                "error",
                "Pipeline must have at least one step",
            )
        
        for i, step in enumerate(pipeline.steps):
            if not step.name:
                result.add_issue(
                    "missing_step_name",
                    "error",
                    f"Step {i} must have a name",
                    location=f"steps[{i}]",
                )
            
            if step.required and not step.handler:
                result.add_issue(
                    "missing_step_handler",
                    "error",
                    f"Required step '{step.name}' must have a handler",
                    location=f"steps[{i}]",
                )
        
        return result
    
    def validate_contract_compatibility(
        self,
        task: IntelligenceTask,
        contract: dict[str, Any] | None = None,
    ) -> ValidationResult:
        """
        Validate task against contract.
        
        Args:
            task: Task to validate
            contract: Optional contract
            
        Returns:
            Validation result
        """
        result = ValidationResult(
            is_valid=True,
            entity_id=task.task_id,
            entity_type="contract_compatibility",
        )
        
        if contract is None:
            result.add_warning(
                "no_contract",
                "No contract provided for validation",
            )
            return result
        
        required_fields = contract.get("required_fields", [])
        for field in required_fields:
            if field not in task.inputs:
                result.add_warning(
                    "missing_field",
                    f"Contract expects field '{field}' in inputs",
                )
        
        return result
