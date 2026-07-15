"""
fool_platform/orchestration/engine/workflow_engine.py

Workflow engine skeleton for orchestration.

IMPORTANT: This does NOT execute real agents.
It coordinates workflow execution state and emits events.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from fool_platform.orchestration.engine.step_runner import (
    StepPreparation,
    StepResult,
    StepRunner,
)
from fool_platform.orchestration.engine.transition_evaluator import TransitionEvaluator
from fool_platform.orchestration.execution_context import ExecutionContext
from fool_platform.orchestration.models import (
    ExecutionSummary,
    OrchestrationDecision,
    StepStatus,
    WorkflowExecution,
    WorkflowExecutionStatus,
    WorkflowStepExecution,
)
from fool_platform.orchestration.orchestration_exceptions import (
    WorkflowNotFoundError,
    WorkflowPlanningError,
    WorkflowStateError,
)
from fool_platform.orchestration.planner.agent_selector import AgentSelector
from fool_platform.orchestration.planner.workflow_planner import WorkflowPlanner
from fool_platform.orchestration.policies.failure_policy import (
    FailureAction,
    FailurePolicyEvaluator,
)
from fool_platform.orchestration.registry.agent_registry import AgentRegistry
from fool_platform.orchestration.registry.capability_registry import CapabilityRegistry
from fool_platform.orchestration.registry.policy_registry import PolicyRegistry
from fool_platform.orchestration.registry.workflow_registry import (
    StepDefinition,
    WorkflowRegistry,
)
from fool_platform.orchestration.state.checkpoint import CheckpointStore
from fool_platform.orchestration.state.workflow_state_store import WorkflowStateStore

if TYPE_CHECKING:
    from fool_platform.events.bus import EventBus


@dataclass
class EngineConfig:
    """Configuration for the workflow engine."""
    enable_event_emission: bool = True
    enable_checkpoints: bool = False
    checkpoint_interval: int = 10


@dataclass
class WorkflowEngine:
    """
    Workflow engine skeleton.
    
    Coordinates workflow execution without executing real agents.
    Emits events through Event Bus when configured.
    """
    workflow_registry: WorkflowRegistry
    agent_registry: AgentRegistry | None = None
    capability_registry: CapabilityRegistry | None = None
    policy_registry: PolicyRegistry | None = None
    state_store: WorkflowStateStore = field(default_factory=WorkflowStateStore)
    checkpoint_store: CheckpointStore = field(default_factory=CheckpointStore)
    event_bus: "EventBus | None" = None
    config: EngineConfig = field(default_factory=EngineConfig)
    
    _planner: WorkflowPlanner = field(default_factory=WorkflowPlanner)
    _agent_selector: AgentSelector = field(default_factory=AgentSelector)
    _transition_evaluator: TransitionEvaluator = field(default_factory=TransitionEvaluator)
    _step_runner: StepRunner = field(default_factory=StepRunner)
    _failure_evaluator: FailurePolicyEvaluator = field(default_factory=FailurePolicyEvaluator)
    _events_emitted: int = 0

    def initialize_workflow(
        self,
        workflow_id: str,
        input_payload: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        case_id: str | None = None,
        initiated_by: str | None = None,
    ) -> WorkflowExecution:
        """
        Initialize a new workflow execution.
        
        Args:
            workflow_id: The workflow ID
            input_payload: Optional input data
            metadata: Optional metadata
            case_id: Optional case ID
            initiated_by: Who initiated the execution
            
        Returns:
            The created WorkflowExecution
            
        Raises:
            WorkflowNotFoundError: If workflow not found
        """
        if not self.workflow_registry.has_workflow(workflow_id):
            raise WorkflowNotFoundError(workflow_id)
        
        workflow = self.workflow_registry.get_workflow(workflow_id)
        
        context = ExecutionContext.create(
            workflow_id=workflow_id,
            workflow_version=workflow.version,
            case_id=case_id,
            initiated_by=initiated_by,
            input_payload=input_payload or {},
            metadata=metadata or {},
        )
        
        execution = self.state_store.create_execution(
            workflow_id=workflow_id,
            workflow_version=workflow.version,
            context=context,
        )
        
        self.state_store.update_status(execution.execution_id, WorkflowExecutionStatus.INITIALIZED)
        
        self._emit_event("workflow.initialized", {
            "execution_id": execution.execution_id,
            "workflow_id": workflow_id,
            "case_id": case_id,
            "initiated_by": initiated_by,
        })
        
        return self.state_store.get_execution(execution.execution_id)

    def plan_workflow(self, execution_id: str) -> WorkflowExecution:
        """
        Plan workflow steps for execution.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            Updated WorkflowExecution with planned steps
            
        Raises:
            WorkflowStateError: If execution not found
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            raise WorkflowStateError(execution_id, "Execution not found")
        
        workflow = self.workflow_registry.get_workflow(execution.workflow_id)
        if not workflow:
            raise WorkflowNotFoundError(execution.workflow_id)
        
        try:
            plan = self._planner.create_plan(workflow)
        except WorkflowPlanningError as e:
            self.state_store.update_status(execution_id, WorkflowExecutionStatus.FAILED)
            raise
        
        for step_def in workflow.steps:
            agent_id = step_def.agent_type
            capability_id = step_def.capability
            
            if self.agent_registry and self.capability_registry:
                selection = self._agent_selector.select_agent_for_step(
                    step_def,
                    self.agent_registry,
                    self.capability_registry,
                )
                if selection.is_valid:
                    agent_id = selection.agent_id
            
            retry_policy = self.policy_registry.get_retry_policy(
                execution.workflow_id, step_def.step_id
            ) if self.policy_registry else None
            max_attempts = retry_policy.max_attempts if retry_policy else 1
            
            context = ExecutionContext.create(
                workflow_id=execution.workflow_id,
                workflow_version=execution.workflow_version,
                case_id=None,
                input_payload={},
            )
            
            preparation = self._step_runner.prepare_step(
                step_def,
                context,
                agent_id=agent_id,
                capability_id=capability_id,
                max_attempts=max_attempts,
            )
            
            self.state_store.add_step(execution_id, preparation.step_execution)
        
        self.state_store.update_status(execution_id, WorkflowExecutionStatus.PLANNED)
        
        self._emit_event("workflow.planned", {
            "execution_id": execution_id,
            "workflow_id": execution.workflow_id,
            "step_count": len(workflow.steps),
        })
        
        return self.state_store.get_execution(execution_id)

    def get_runnable_steps(self, execution_id: str) -> list[str]:
        """
        Get steps that are ready to run.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            List of runnable step IDs
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            return []
        
        runnable: list[str] = []
        
        for step_id, step in execution.current_steps.items():
            if step.status != StepStatus.PENDING:
                continue
            
            deps_met = all(
                dep in execution.completed_steps
                for dep in step.depends_on
            )
            
            if deps_met:
                runnable.append(step_id)
        
        return runnable

    def mark_step_completed(
        self,
        execution_id: str,
        step_id: str,
        output: dict[str, Any] | None = None,
    ) -> WorkflowExecution:
        """
        Mark a step as completed.
        
        Args:
            execution_id: The execution ID
            step_id: The step ID
            output: Optional step output
            
        Returns:
            Updated WorkflowExecution
        """
        self.state_store.update_step_status(execution_id, step_id, StepStatus.READY)
        self.state_store.update_step_status(execution_id, step_id, StepStatus.RUNNING)
        execution = self.state_store.get_execution(execution_id)
        
        step = execution.current_steps.get(step_id) if execution else None
        
        self.state_store.update_step_status(execution_id, step_id, StepStatus.COMPLETED)
        
        self._emit_event("workflow.step.completed", {
            "execution_id": execution_id,
            "step_id": step_id,
        })
        
        execution = self.state_store.get_execution(execution_id)
        
        self._check_workflow_completion(execution)
        
        return execution

    def mark_step_failed(
        self,
        execution_id: str,
        step_id: str,
        error: str,
    ) -> WorkflowExecution:
        """
        Mark a step as failed.
        
        Args:
            execution_id: The execution ID
            step_id: The step ID
            error: The error message
            
        Returns:
            Updated WorkflowExecution
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            raise WorkflowStateError(execution_id, "Execution not found")
        
        step = execution.current_steps.get(step_id)
        if not step:
            raise WorkflowStateError(execution_id, f"Step {step_id} not found")
        
        failure_decision = FailureAction.FAIL
        if self.policy_registry:
            failure_policy = self.policy_registry.get_failure_policy(execution.workflow_id)
            failure_decision = self._failure_evaluator.evaluate_failure(
                execution, step, failure_policy
            ).action
        
        self.state_store.update_step_status(execution_id, step_id, StepStatus.FAILED)
        
        self._emit_event("workflow.step.failed", {
            "execution_id": execution_id,
            "step_id": step_id,
            "error": error,
            "action": failure_decision.value if hasattr(failure_decision, 'value') else failure_decision,
        })
        
        execution = self.state_store.get_execution(execution_id)
        
        if failure_decision == FailureAction.FAIL:
            self.state_store.update_status(execution_id, WorkflowExecutionStatus.FAILED)
            self._emit_event("workflow.failed", {
                "execution_id": execution_id,
                "reason": f"Step {step_id} failed: {error}",
            })
        
        return execution

    def evaluate_transitions(self, execution_id: str) -> list[OrchestrationDecision]:
        """
        Evaluate available transitions.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            List of orchestration decisions
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            return []
        
        workflow = self.workflow_registry.get_workflow(execution.workflow_id)
        if not workflow:
            return []
        
        evaluation = self._transition_evaluator.find_available_transitions(
            workflow, execution
        )
        
        decisions: list[OrchestrationDecision] = []
        
        for decision in evaluation.available_transitions:
            decisions.append(OrchestrationDecision(
                decision_id=str(uuid4()),
                execution_id=execution_id,
                decision_type="transition_evaluation",
                rationale=decision.rationale,
                inputs={"transition": decision.transition.__dict__},
                outputs={"should_take": decision.should_take},
            ))
        
        return decisions

    def get_execution_summary(self, execution_id: str) -> ExecutionSummary | None:
        """
        Get a summary of workflow execution.
        
        Args:
            execution_id: The execution ID
            
        Returns:
            ExecutionSummary or None if not found
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            return None
        
        runnable_steps = self.get_runnable_steps(execution_id)
        
        return ExecutionSummary(
            execution_id=execution_id,
            workflow_id=execution.workflow_id,
            status=execution.status,
            runnable_steps=runnable_steps,
            completed_steps=execution.completed_steps.copy(),
            failed_steps=execution.failed_steps.copy(),
            blocked_steps=execution.blocked_steps.copy(),
            events_emitted=self._events_emitted,
            errors=[],
        )

    def cancel_workflow(
        self,
        execution_id: str,
        reason: str,
    ) -> WorkflowExecution:
        """
        Cancel a workflow execution.
        
        Args:
            execution_id: The execution ID
            reason: Cancellation reason
            
        Returns:
            Updated WorkflowExecution
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            raise WorkflowStateError(execution_id, "Execution not found")
        
        self.state_store.update_status(execution_id, WorkflowExecutionStatus.CANCELLED)
        
        self._emit_event("workflow.cancelled", {
            "execution_id": execution_id,
            "reason": reason,
        })
        
        return self.state_store.get_execution(execution_id)

    def terminate_workflow(
        self,
        execution_id: str,
        reason: str,
    ) -> WorkflowExecution:
        """
        Terminate a workflow execution.
        
        Args:
            execution_id: The execution ID
            reason: Termination reason
            
        Returns:
            Updated WorkflowExecution
        """
        execution = self.state_store.get_execution(execution_id)
        if not execution:
            raise WorkflowStateError(execution_id, "Execution not found")
        
        self.state_store.update_status(execution_id, WorkflowExecutionStatus.TERMINATED)
        
        self._emit_event("workflow.terminated", {
            "execution_id": execution_id,
            "reason": reason,
        })
        
        return self.state_store.get_execution(execution_id)

    def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Emit an event through Event Bus if configured."""
        if not self.config.enable_event_emission or not self.event_bus:
            return
        
        try:
            from fool_platform.events.envelope import EventEnvelope
            
            event = EventEnvelope.create_with_metadata(
                event_type=event_type,
                event_version="1.0.0",
                payload=data,
            )
            
            self.event_bus.publish(event)
            self._events_emitted += 1
        except Exception:
            pass

    def _check_workflow_completion(self, execution: WorkflowExecution) -> None:
        """Check if workflow should complete."""
        if len(execution.current_steps) == 0:
            if len(execution.failed_steps) > 0:
                self.state_store.update_status(
                    execution.execution_id,
                    WorkflowExecutionStatus.FAILED,
                )
            else:
                self.state_store.update_status(
                    execution.execution_id,
                    WorkflowExecutionStatus.COMPLETED,
                )
                self._emit_event("workflow.completed", {
                    "execution_id": execution.execution_id,
                    "workflow_id": execution.workflow_id,
                })
