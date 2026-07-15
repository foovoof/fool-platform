"""
fool_platform/orchestration/tests/test_orchestration.py

Comprehensive tests for the Orchestration layer.
"""
import pytest
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fool_platform.orchestration import (
    ExecutionContext,
    ExecutionSummary,
    OrchestrationDecision,
    OrchestrationError,
    StepStatus,
    WorkflowExecution,
    WorkflowExecutionStatus,
    WorkflowStepExecution,
    WorkflowNotFoundError,
    WorkflowPlanningError,
    WorkflowStateError,
    WorkflowTransitionError,
)
from fool_platform.orchestration.engine import (
    StepRunner,
    StepResult,
    TransitionEvaluator,
    WorkflowEngine,
    EngineConfig,
)
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
    AgentRegistryError,
    CapabilityRegistryError,
    CheckpointError,
    PolicyEvaluationError,
    WorkflowNotFoundError,
    WorkflowPlanningError,
    WorkflowStateError,
    WorkflowTransitionError,
    WorkflowValidationError,
)
from fool_platform.orchestration.planner import (
    AgentSelection,
    AgentSelector,
    WorkflowPlan,
    WorkflowPlanner,
)
from fool_platform.orchestration.policies import (
    FailureAction,
    FailureDecision,
    FailurePolicyEvaluator,
    RetryPolicyEvaluator,
    TerminationDecision,
    TerminationPolicyEvaluator,
    TimeoutPolicyEvaluator,
)
from fool_platform.orchestration.registry import (
    AgentDefinition,
    AgentRegistry,
    CapabilityDefinition,
    CapabilityRegistry,
    FailurePolicy,
    PolicyRegistry,
    RetryPolicy,
    StepDefinition,
    TerminationCondition,
    TimeoutPolicy,
    TransitionDefinition,
    WorkflowDefinition,
    WorkflowRegistry,
)
from fool_platform.orchestration.state import (
    Checkpoint,
    CheckpointStore,
    StateTransitions,
    WorkflowStateStore,
)


class TestOrchestrationModels:
    """Tests for orchestration data models."""

    def test_workflow_execution_status_enum(self):
        """Test workflow execution status enum values."""
        assert WorkflowExecutionStatus.CREATED.value == "created"
        assert WorkflowExecutionStatus.RUNNING.value == "running"
        assert WorkflowExecutionStatus.COMPLETED.value == "completed"
        assert WorkflowExecutionStatus.FAILED.value == "failed"

    def test_step_status_enum(self):
        """Test step status enum values."""
        assert StepStatus.PENDING.value == "pending"
        assert StepStatus.READY.value == "ready"
        assert StepStatus.RUNNING.value == "running"
        assert StepStatus.COMPLETED.value == "completed"
        assert StepStatus.FAILED.value == "failed"

    def test_workflow_execution_create(self):
        """Test workflow execution creation."""
        execution = WorkflowExecution.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        assert execution.workflow_id == "test.workflow"
        assert execution.workflow_version == "1.0.0"
        assert execution.status == WorkflowExecutionStatus.CREATED
        assert execution.execution_id is not None

    def test_workflow_step_execution_immutable(self):
        """Test workflow step execution immutability."""
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.PENDING,
        )
        
        updated = step.with_status(StepStatus.READY)
        assert step.status == StepStatus.PENDING
        assert updated.status == StepStatus.READY

    def test_execution_summary(self):
        """Test execution summary creation."""
        summary = ExecutionSummary(
            execution_id="exec1",
            workflow_id="wf1",
            status=WorkflowExecutionStatus.RUNNING,
            runnable_steps=["step1"],
            completed_steps=["step0"],
            failed_steps=[],
            blocked_steps=[],
            events_emitted=5,
            errors=[],
        )
        
        assert summary.execution_id == "exec1"
        assert summary.runnable_steps == ["step1"]
        assert summary.generated_at is not None


class TestExceptions:
    """Tests for orchestration exceptions."""

    def test_workflow_not_found_error(self):
        """Test WorkflowNotFoundError."""
        error = WorkflowNotFoundError("unknown.workflow")
        assert error.workflow_id == "unknown.workflow"
        assert "unknown.workflow" in str(error)

    def test_workflow_planning_error(self):
        """Test WorkflowPlanningError."""
        error = WorkflowPlanningError(
            workflow_id="test.workflow",
            reason="cyclic dependency",
            details=["step1 -> step2 -> step1"],
        )
        assert error.workflow_id == "test.workflow"
        assert error.reason == "cyclic dependency"

    def test_workflow_transition_error(self):
        """Test WorkflowTransitionError."""
        error = WorkflowTransitionError(
            execution_id="exec1",
            current_status="running",
            target_status="created",
        )
        assert error.current_status == "running"
        assert error.target_status == "created"


class TestExecutionContext:
    """Tests for execution context."""

    def test_create_execution_context(self):
        """Test execution context creation."""
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
            case_id="case1",
            initiated_by="user1",
            input_payload={"key": "value"},
        )
        
        assert context.workflow_id == "test.workflow"
        assert context.case_id == "case1"
        assert context.input_payload == {"key": "value"}
        assert context.trace_id is not None
        assert context.correlation_id is not None

    def test_create_child_context(self):
        """Test child context creation."""
        parent = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        child = parent.create_child_context("step1")
        
        assert child.execution_id == parent.execution_id
        assert child.metadata["step_id"] == "step1"
        assert child.metadata["parent_execution_id"] == parent.execution_id

    def test_attach_metadata(self):
        """Test metadata attachment."""
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        context.attach_metadata("key1", "value1")
        assert context.get_metadata("key1") == "value1"
        assert context.get_metadata("nonexistent", "default") == "default"


class TestWorkflowStateStore:
    """Tests for workflow state store."""

    def test_create_execution(self):
        """Test workflow execution creation in store."""
        store = WorkflowStateStore()
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        execution = store.create_execution("test.workflow", "1.0.0", context)
        
        assert execution.workflow_id == "test.workflow"
        assert execution.status == WorkflowExecutionStatus.CREATED

    def test_get_execution(self):
        """Test getting execution from store."""
        store = WorkflowStateStore()
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        created = store.create_execution("test.workflow", "1.0.0", context)
        retrieved = store.get_execution(created.execution_id)
        
        assert retrieved is not None
        assert retrieved.execution_id == created.execution_id

    def test_valid_workflow_transition(self):
        """Test valid workflow status transition."""
        store = WorkflowStateStore()
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        execution = store.create_execution("test.workflow", "1.0.0", context)
        updated = store.update_status(execution.execution_id, WorkflowExecutionStatus.INITIALIZED)
        
        assert updated.status == WorkflowExecutionStatus.INITIALIZED

    def test_invalid_workflow_transition(self):
        """Test invalid workflow status transition raises error."""
        store = WorkflowStateStore()
        context = ExecutionContext.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        execution = store.create_execution("test.workflow", "1.0.0", context)
        
        with pytest.raises(WorkflowTransitionError):
            store.update_status(execution.execution_id, WorkflowExecutionStatus.COMPLETED)


class TestCheckpointStore:
    """Tests for checkpoint store."""

    def test_create_checkpoint(self):
        """Test checkpoint creation."""
        store = CheckpointStore()
        execution = WorkflowExecution.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        checkpoint = store.create_checkpoint(execution)
        
        assert checkpoint.execution_id == execution.execution_id
        assert checkpoint.workflow_id == "test.workflow"
        assert checkpoint.checkpoint_id is not None

    def test_get_checkpoint(self):
        """Test getting checkpoint."""
        store = CheckpointStore()
        execution = WorkflowExecution.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        created = store.create_checkpoint(execution)
        retrieved = store.get_checkpoint(created.checkpoint_id)
        
        assert retrieved is not None
        assert retrieved.checkpoint_id == created.checkpoint_id

    def test_restore_checkpoint(self):
        """Test checkpoint restoration."""
        store = CheckpointStore()
        execution = WorkflowExecution.create(
            workflow_id="test.workflow",
            workflow_version="1.0.0",
        )
        
        checkpoint = store.create_checkpoint(execution)
        restored = store.restore_checkpoint(checkpoint.checkpoint_id)
        
        assert restored.execution_id == execution.execution_id


class TestStateTransitions:
    """Tests for state transitions."""

    def test_valid_workflow_transition(self):
        """Test valid workflow transition validation."""
        transitions = StateTransitions()
        
        result = transitions.validate_workflow_transition(
            WorkflowExecutionStatus.CREATED,
            WorkflowExecutionStatus.INITIALIZED,
        )
        
        assert result is True

    def test_invalid_workflow_transition(self):
        """Test invalid workflow transition raises error."""
        transitions = StateTransitions()
        
        with pytest.raises(WorkflowTransitionError):
            transitions.validate_workflow_transition(
                WorkflowExecutionStatus.COMPLETED,
                WorkflowExecutionStatus.RUNNING,
            )

    def test_valid_step_transition(self):
        """Test valid step transition validation."""
        transitions = StateTransitions()
        
        result = transitions.validate_step_transition(
            StepStatus.PENDING,
            StepStatus.READY,
        )
        
        assert result is True


class TestWorkflowPlanner:
    """Tests for workflow planner."""

    def test_create_plan_simple_workflow(self):
        """Test creating plan for simple workflow."""
        workflow = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="step1", name="Step 1"),
                StepDefinition(step_id="step2", name="Step 2", depends_on=["step1"]),
            ],
        )
        
        planner = WorkflowPlanner()
        plan = planner.create_plan(workflow)
        
        assert plan.workflow_id == "test.workflow"
        assert "step1" in plan.entry_steps
        assert "step2" in plan.terminal_steps

    def test_detect_cycles(self):
        """Test cycle detection."""
        workflow = WorkflowDefinition(
            workflow_id="cyclic.workflow",
            name="Cyclic Workflow",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="step1", name="Step 1", depends_on=["step2"]),
                StepDefinition(step_id="step2", name="Step 2", depends_on=["step1"]),
            ],
        )
        
        planner = WorkflowPlanner()
        has_cycle = planner.detect_cycles(workflow)
        
        assert has_cycle is True

    def test_topological_ordering(self):
        """Test topological step ordering."""
        workflow = WorkflowDefinition(
            workflow_id="ordered.workflow",
            name="Ordered Workflow",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="step1", name="Step 1"),
                StepDefinition(step_id="step2", name="Step 2", depends_on=["step1"]),
                StepDefinition(step_id="step3", name="Step 3", depends_on=["step2"]),
            ],
        )
        
        planner = WorkflowPlanner()
        order = planner.topologically_order_steps(workflow)
        
        assert order.index("step1") < order.index("step2")
        assert order.index("step2") < order.index("step3")

    def test_identify_entry_and_terminal_steps(self):
        """Test identifying entry and terminal steps."""
        workflow = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="start", name="Start"),
                StepDefinition(step_id="middle", name="Middle", depends_on=["start"]),
                StepDefinition(step_id="end", name="End", depends_on=["middle"]),
            ],
        )
        
        planner = WorkflowPlanner()
        entry = planner.identify_entry_steps(workflow)
        terminal = planner.identify_terminal_steps(workflow)
        
        assert "start" in entry
        assert "end" in terminal


class TestAgentSelector:
    """Tests for agent selector."""

    def test_select_explicit_agent(self):
        """Test selecting explicitly assigned agent."""
        agent_registry = AgentRegistry()
        agent_registry._agents["research"] = AgentDefinition(
            agent_type="research",
            version="1.0.0",
            capabilities=["research"],
        )
        
        capability_registry = CapabilityRegistry()
        capability_registry._capabilities["research"] = CapabilityDefinition(
            id="research",
            version="1.0.0",
        )
        
        step = StepDefinition(step_id="step1", name="Step 1", agent_type="research")
        
        selector = AgentSelector()
        selection = selector.select_agent_for_step(
            step, agent_registry, capability_registry
        )
        
        assert selection.agent_id == "research"
        assert selection.selected_by == "explicit"
        assert selection.is_valid is True

    def test_select_by_capability(self):
        """Test selecting agent by capability."""
        agent_registry = AgentRegistry()
        agent_def = AgentDefinition(
            agent_type="research",
            version="1.0.0",
            capabilities=["research"],
        )
        agent_registry._agents["research"] = agent_def
        agent_registry._capability_index["research"] = ["research"]
        
        capability_registry = CapabilityRegistry()
        capability_registry._capabilities["research"] = CapabilityDefinition(
            id="research",
            version="1.0.0",
        )
        
        step = StepDefinition(step_id="step1", name="Step 1", capability="research")
        
        selector = AgentSelector()
        selection = selector.select_agent_for_step(
            step, agent_registry, capability_registry
        )
        
        assert selection.agent_id == "research"
        assert selection.selected_by == "capability"


class TestRetryPolicyEvaluator:
    """Tests for retry policy evaluator."""

    def test_should_retry_under_max_attempts(self):
        """Test retry decision under max attempts."""
        evaluator = RetryPolicyEvaluator()
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.FAILED,
            attempts=1,
        )
        policy = RetryPolicy(max_attempts=3)
        
        assert evaluator.should_retry(step, policy) is True

    def test_should_not_retry_at_max_attempts(self):
        """Test no retry at max attempts."""
        evaluator = RetryPolicyEvaluator()
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.FAILED,
            attempts=3,
        )
        policy = RetryPolicy(max_attempts=3)
        
        assert evaluator.should_retry(step, policy) is False


class TestTimeoutPolicyEvaluator:
    """Tests for timeout policy evaluator."""

    def test_not_timed_out(self):
        """Test step not timed out."""
        evaluator = TimeoutPolicyEvaluator()
        started_at = datetime.now(timezone.utc).isoformat()
        policy = TimeoutPolicy(duration_seconds=300)
        
        assert evaluator.is_timed_out(started_at, policy) is False

    def test_remaining_time(self):
        """Test remaining time calculation."""
        evaluator = TimeoutPolicyEvaluator()
        started_at = datetime.now(timezone.utc).isoformat()
        policy = TimeoutPolicy(duration_seconds=300)
        
        remaining = evaluator.remaining_time(started_at, policy)
        
        assert remaining > 0
        assert remaining <= 300


class TestFailurePolicyEvaluator:
    """Tests for failure policy evaluator."""

    def test_evaluate_fail_action(self):
        """Test failure with fail action."""
        evaluator = FailurePolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.FAILED,
            error="test error",
        )
        policy = FailurePolicy(on_failure="fail")
        
        decision = evaluator.evaluate_failure(execution, step, policy)
        
        assert decision.action == FailureAction.FAIL

    def test_evaluate_continue_action(self):
        """Test failure with continue action."""
        evaluator = FailurePolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.FAILED,
            error="test error",
        )
        policy = FailurePolicy(on_failure="continue")
        
        decision = evaluator.evaluate_failure(execution, step, policy)
        
        assert decision.action == FailureAction.CONTINUE

    def test_evaluate_escalate_action(self):
        """Test failure with escalate action."""
        evaluator = FailurePolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.FAILED,
            error="test error",
        )
        policy = FailurePolicy(on_failure="escalate_to_human", escalation_target="manager")
        
        decision = evaluator.evaluate_failure(execution, step, policy)
        
        assert decision.action == FailureAction.ESCALATE
        assert decision.escalate_to == "manager"


class TestTerminationPolicyEvaluator:
    """Tests for termination policy evaluator."""

    def test_is_terminated_by_step_completed(self):
        """Test termination by step completion."""
        evaluator = TerminationPolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        execution.completed_steps = ["step1"]
        conditions = [
            TerminationCondition(condition_type="step_completed", step_id="step1"),
        ]
        
        assert evaluator.is_terminated(execution, conditions) is True

    def test_is_not_terminated_no_match(self):
        """Test no termination when conditions don't match."""
        evaluator = TerminationPolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        execution.completed_steps = ["step1"]
        conditions = [
            TerminationCondition(condition_type="step_completed", step_id="step2"),
        ]
        
        assert evaluator.is_terminated(execution, conditions) is False

    def test_explain_termination(self):
        """Test termination explanation."""
        evaluator = TerminationPolicyEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        execution.completed_steps = ["step1"]
        conditions = [
            TerminationCondition(condition_type="step_completed", step_id="step1"),
        ]
        
        decision = evaluator.explain_termination(execution, conditions)
        
        assert decision.is_terminated is True
        assert decision.condition_matched == "step_completed"


class TestTransitionEvaluator:
    """Tests for transition evaluator."""

    def test_evaluate_step_completed_condition(self):
        """Test step completed condition evaluation."""
        evaluator = TransitionEvaluator()
        transition = TransitionDefinition(
            from_step="step1",
            to_step="step2",
            condition_type="step_completed",
            condition_params={"step_id": "step1"},
        )
        execution = WorkflowExecution.create("wf1", "1.0.0")
        execution.completed_steps = ["step1"]
        
        result = evaluator.evaluate_condition(
            "step_completed",
            {"step_id": "step1"},
            execution,
        )
        
        assert result is True

    def test_evaluate_always_condition(self):
        """Test always condition evaluation."""
        evaluator = TransitionEvaluator()
        execution = WorkflowExecution.create("wf1", "1.0.0")
        
        result = evaluator.evaluate_condition("always", {}, execution)
        
        assert result is True

    def test_reject_unknown_condition(self):
        """Test rejection of unknown condition types."""
        evaluator = TransitionEvaluator()
        transition = TransitionDefinition(
            from_step="step1",
            to_step="step2",
            condition_type="unknown_condition",
        )
        execution = WorkflowExecution.create("wf1", "1.0.0")
        
        decision = evaluator.evaluate_transition(transition, execution)
        
        assert decision.should_take is False
        assert "Unknown condition type" in decision.rationale


class TestStepRunner:
    """Tests for step runner."""

    def test_prepare_step(self):
        """Test step preparation."""
        runner = StepRunner()
        step = StepDefinition(
            step_id="step1",
            name="Step 1",
            agent_type="agent1",
            capability="cap1",
            depends_on=["step0"],
        )
        context = ExecutionContext.create("wf1", "1.0.0")
        
        preparation = runner.prepare_step(step, context)
        
        assert preparation.step_execution.step_id == "step1"
        assert preparation.agent_id == "agent1"
        assert StepStatus.PENDING == preparation.step_execution.status

    def test_mark_step_completed(self):
        """Test marking step as completed."""
        runner = StepRunner()
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.RUNNING,
        )
        
        result = runner.mark_step_completed(step)
        
        assert result.success is True
        assert result.step_execution.status == StepStatus.COMPLETED

    def test_mark_step_failed(self):
        """Test marking step as failed."""
        runner = StepRunner()
        step = WorkflowStepExecution(
            step_id="step1",
            agent_id="agent1",
            capability_id="cap1",
            status=StepStatus.RUNNING,
        )
        
        result = runner.mark_step_failed(step, "test error")
        
        assert result.success is False
        assert result.step_execution.status == StepStatus.FAILED
        assert "test error" in result.message


class TestWorkflowEngine:
    """Tests for workflow engine."""

    def test_initialize_workflow_not_found(self):
        """Test workflow initialization with unknown workflow."""
        workflow_registry = WorkflowRegistry()
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        
        with pytest.raises(WorkflowNotFoundError):
            engine.initialize_workflow("unknown.workflow")

    def test_initialize_workflow(self):
        """Test workflow initialization."""
        workflow_registry = WorkflowRegistry()
        workflow_registry._workflows["test.workflow"] = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[],
        )
        
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        execution = engine.initialize_workflow("test.workflow")
        
        assert execution is not None
        assert execution.workflow_id == "test.workflow"
        assert execution.status == WorkflowExecutionStatus.INITIALIZED

    def test_get_runnable_steps(self):
        """Test getting runnable steps."""
        workflow_registry = WorkflowRegistry()
        workflow_registry._workflows["test.workflow"] = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="step1", name="Step 1"),
                StepDefinition(step_id="step2", name="Step 2", depends_on=["step1"]),
            ],
        )
        
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        execution = engine.initialize_workflow("test.workflow")
        execution = engine.plan_workflow(execution.execution_id)
        
        runnable = engine.get_runnable_steps(execution.execution_id)
        
        assert "step1" in runnable
        assert "step2" not in runnable

    def test_mark_step_completed(self):
        """Test marking step as completed via state store."""
        workflow_registry = WorkflowRegistry()
        workflow_registry._workflows["test.workflow"] = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[StepDefinition(step_id="step1", name="Step 1")],
        )
        
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        execution = engine.initialize_workflow("test.workflow")
        execution = engine.plan_workflow(execution.execution_id)
        
        engine.state_store.update_status(execution.execution_id, WorkflowExecutionStatus.RUNNING)
        
        exec1 = engine.state_store.get_execution(execution.execution_id)
        step1 = exec1.current_steps.get("step1")
        assert step1 is not None, f"Step not found. Steps: {list(exec1.current_steps.keys())}"
        initial_status = step1.status
        
        engine.state_store.update_step_status(execution.execution_id, "step1", StepStatus.READY)
        
        exec2 = engine.state_store.get_execution(execution.execution_id)
        step2 = exec2.current_steps.get("step1")
        assert step2.status == StepStatus.READY, f"Expected READY, got {step2.status}"
        
        engine.state_store.update_step_status(execution.execution_id, "step1", StepStatus.RUNNING)
        
        updated = engine.state_store.get_execution(execution.execution_id)
        assert "step1" in updated.current_steps
        
        engine.state_store.update_step_status(execution.execution_id, "step1", StepStatus.COMPLETED)
        
        updated = engine.state_store.get_execution(execution.execution_id)
        assert "step1" in updated.completed_steps

    def test_get_execution_summary(self):
        """Test getting execution summary."""
        workflow_registry = WorkflowRegistry()
        workflow_registry._workflows["test.workflow"] = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[],
        )
        
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        execution = engine.initialize_workflow("test.workflow")
        
        summary = engine.get_execution_summary(execution.execution_id)
        
        assert summary is not None
        assert summary.workflow_id == "test.workflow"
        assert summary.execution_id == execution.execution_id

    def test_cancel_workflow(self):
        """Test workflow cancellation."""
        workflow_registry = WorkflowRegistry()
        workflow_registry._workflows["test.workflow"] = WorkflowDefinition(
            workflow_id="test.workflow",
            name="Test Workflow",
            version="1.0.0",
            steps=[],
        )
        
        engine = WorkflowEngine(workflow_registry=workflow_registry)
        execution = engine.initialize_workflow("test.workflow")
        engine.state_store.update_status(execution.execution_id, WorkflowExecutionStatus.PLANNED)
        engine.state_store.update_status(execution.execution_id, WorkflowExecutionStatus.RUNNING)
        
        cancelled = engine.cancel_workflow(execution.execution_id, "user cancelled")
        
        assert cancelled.status == WorkflowExecutionStatus.CANCELLED


class TestWorkflowRegistry:
    """Tests for workflow registry."""

    def test_list_workflows(self):
        """Test listing workflows."""
        registry = WorkflowRegistry()
        registry._workflows["wf1"] = WorkflowDefinition("wf1", "WF1", "1.0.0")
        registry._workflows["wf2"] = WorkflowDefinition("wf2", "WF2", "1.0.0")
        
        workflows = registry.list_workflows()
        
        assert "wf1" in workflows
        assert "wf2" in workflows

    def test_validate_workflow_with_missing_agent(self):
        """Test validation rejects missing agent reference."""
        registry = WorkflowRegistry()
        workflow = WorkflowDefinition(
            workflow_id="wf1",
            name="WF1",
            version="1.0.0",
            required_agents=["unknown_agent"],
            steps=[],
        )
        agent_registry = AgentRegistry()
        
        errors = registry.validate_workflow(workflow, agent_registry=agent_registry)
        
        assert len(errors) > 0
        assert any("unknown_agent" in e for e in errors)

    def test_validate_step_dependencies(self):
        """Test step dependency validation."""
        registry = WorkflowRegistry()
        workflow = WorkflowDefinition(
            workflow_id="wf1",
            name="WF1",
            version="1.0.0",
            steps=[
                StepDefinition(step_id="step1", name="Step 1"),
            ],
        )
        
        errors = registry.validate_steps(workflow)
        
        assert len(errors) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
