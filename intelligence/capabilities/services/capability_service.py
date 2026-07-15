"""
intelligence/capabilities/services/capability_service.py

Capability Service.

Main service for capability execution coordination.
"""
from __future__ import annotations

from typing import Any

from intelligence.capabilities.models import (
    CapabilityDefinition,
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    CapabilityStatus,
)
from intelligence.capabilities.registry import CapabilityRegistry, create_default_registry
from intelligence.capabilities.execution import (
    CapabilityExecutor,
    CapabilityDispatcher,
    CapabilityResolver,
    ExecutionManager,
)
from intelligence.capabilities.events import CapabilityEventEmitter
from intelligence.capabilities.validation import (
    CapabilityValidator,
    TaskValidator,
)


class CapabilityService:
    """
    Main service for capability execution.
    
    Coordinates all capability operations.
    """
    
    def __init__(self) -> None:
        """Initialize service."""
        self._registry: CapabilityRegistry = create_default_registry()
        self._executor = CapabilityExecutor()
        self._dispatcher = CapabilityDispatcher(self._registry)
        self._resolver = CapabilityResolver(self._registry)
        self._manager = ExecutionManager()
        self._emitter = CapabilityEventEmitter()
        self._capability_validator = CapabilityValidator()
        self._task_validator = TaskValidator()
    
    def register_capability(
        self,
        capability: CapabilityDefinition,
    ) -> bool:
        """Register a capability."""
        result = self._capability_validator.validate(capability)
        if not result.is_valid:
            return False
        return self._registry.register(capability)
    
    def get_capability(
        self,
        capability_id: str,
    ) -> CapabilityDefinition | None:
        """Get capability by ID."""
        return self._registry.get(capability_id)
    
    def get_capability_by_type(
        self,
        capability_type: CapabilityType,
    ) -> CapabilityDefinition | None:
        """Get capability by type."""
        return self._registry.get_by_type(capability_type)
    
    def list_capabilities(self) -> list[CapabilityDefinition]:
        """List all capabilities."""
        return self._registry.list_all()
    
    def execute_task(
        self,
        task: CapabilityTask,
    ) -> CapabilityResult:
        """Execute a capability task."""
        task_result = self._task_validator.validate(task)
        if not task_result.is_valid:
            return CapabilityResult(
                task_id=task.task_id,
                capability_id=task.capability_id,
                capability_type=task.capability_type,
                status=CapabilityStatus.FAILED,
                errors=[str(e) for e in task_result.issues],
            )
        
        self._emitter.emit_started(
            task.capability_id,
            task.capability_type,
            task.task_id,
        )
        
        record = self._manager.create_record(task)
        
        result = self._dispatcher.dispatch(task)
        
        self._manager.update_record(
            record.record_id,
            result_id=result.result_id,
            status=result.status,
        )
        
        if result.is_successful():
            self._emitter.emit_completed(
                task.capability_id,
                task.capability_type,
                task.task_id,
                result.result_id,
            )
        else:
            self._emitter.emit_failed(
                task.capability_id,
                task.capability_type,
                task.task_id,
                "; ".join(result.errors),
            )
        
        for finding in result.findings:
            self._emitter.emit_finding_created(
                task.capability_id,
                task.capability_type,
                task.task_id,
                finding.finding_id,
            )
        
        for artifact in result.artifacts:
            self._emitter.emit_artifact_created(
                task.capability_id,
                task.capability_type,
                task.task_id,
                artifact.artifact_id,
            )
        
        return result
    
    def get_execution_records(self) -> list:
        """Get execution records."""
        return self._manager.get_records()
