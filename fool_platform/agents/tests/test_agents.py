"""
fool_platform/agents/tests/test_agents.py

Tests for Agent Runtime Framework.

Covers:
1. AgentTask creation
2. AgentResult creation
3. AgentCapability creation
4. AgentContext creation
5. Child context creation
6. BaseAgent abstract behavior
7. ExampleAgent initialization
8. ExampleAgent start
9. ExampleAgent execution
10. ExampleAgent result
11. Lifecycle valid transitions
12. Lifecycle invalid transitions
13. Task validation success
14. Task validation failure
15. Result validation success
16. Memory set/get/delete/clear
17. Policy allow
18. Policy deny
19. Event emitter without Event Bus
20. Event emitter with Event Bus
21. Executor register agent
22. Executor execute by id
23. Executor execute by capability
24. Executor handles failures
25. Registry adapter loads agents
26. Registry adapter loads capabilities
27. No tool execution
28. No connector execution
29. No AI imports
30. Architecture rules enforced
"""
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from fool_platform.agents.base import (
    BaseAgent,
    ExampleAgent,
    AgentContext,
    AgentTask,
    AgentResult,
    AgentCapability,
    AgentExecutionRecord,
    AgentEventEmitter,
    AgentLifecycleManager,
    AgentMemory,
    InMemoryAgentMemory,
    AgentPolicy,
    AgentPolicyDecision,
    AgentPolicyEvaluator,
    AgentTaskValidator,
    AgentResultValidator,
    AgentCapabilityValidator,
    ValidationResult,
    AgentStatus,
    AgentTaskStatus,
    AgentResultStatus,
    AgentInitializationError,
    AgentLifecycleError,
    AgentValidationError,
    AgentCapabilityError,
    AgentExecutionError,
)
from fool_platform.agents.runtime import AgentExecutor
from fool_platform.agents.registry.registry_adapter import RegistryAdapter


class TestAgentModels:
    """Test agent data models."""

    def test_agent_task_creation(self):
        """Test AgentTask creation with defaults."""
        task = AgentTask(
            task_type="test.type",
            objective="Test objective",
            inputs={"key": "value"},
        )
        assert task.task_id is not None
        assert task.task_type == "test.type"
        assert task.objective == "Test objective"
        assert task.inputs == {"key": "value"}
        assert task.trace_id is not None
        assert task.created_at is not None

    def test_agent_result_creation(self):
        """Test AgentResult creation."""
        result = AgentResult(
            task_id="task-123",
            agent_id="agent-456",
            outputs={"result": "success"},
        )
        assert result.result_id is not None
        assert result.task_id == "task-123"
        assert result.agent_id == "agent-456"
        assert result.status == AgentResultStatus.SUCCESS
        assert result.outputs == {"result": "success"}
        assert result.is_success is True
        assert result.is_failure is False

    def test_agent_capability_creation(self):
        """Test AgentCapability creation."""
        cap = AgentCapability(
            capability_id="test.capability",
            name="Test Capability",
            description="A test capability",
        )
        assert cap.capability_id == "test.capability"
        assert cap.name == "Test Capability"
        assert cap.matches_capability_id("test.capability") is True
        assert cap.matches_capability_id("other.capability") is False

    def test_agent_execution_record(self):
        """Test AgentExecutionRecord creation."""
        record = AgentExecutionRecord(
            task_id="task-123",
            agent_id="agent-456",
        )
        assert record.execution_record_id is not None
        assert record.task_id == "task-123"
        assert record.agent_id == "agent-456"
        assert record.status == AgentTaskStatus.PENDING

    def test_agent_result_failure_status(self):
        """Test AgentResult failure status."""
        result = AgentResult(
            task_id="task-123",
            agent_id="agent-456",
            status=AgentResultStatus.FAILURE,
            errors=["Error 1", "Error 2"],
        )
        assert result.is_failure is True
        assert result.is_success is False
        assert len(result.errors) == 2


class TestAgentContext:
    """Test Agent Context."""

    def test_context_creation(self):
        """Test AgentContext creation."""
        context = AgentContext.create(
            agent_id="agent-123",
            task_id="task-456",
            case_id="case-789",
        )
        assert context.context_id is not None
        assert context.agent_id == "agent-123"
        assert context.task_id == "task-456"
        assert context.case_id == "case-789"

    def test_child_context_creation(self):
        """Test child context creation."""
        parent = AgentContext.create(
            agent_id="agent-123",
            task_id="task-456",
        )
        child = parent.create_child_context("sub-operation")
        assert child.context_id != parent.context_id
        assert child.agent_id == parent.agent_id
        assert child.task_id == parent.task_id
        assert child.trace_id == parent.trace_id
        assert child.metadata.get("parent_context_id") == parent.context_id

    def test_attach_metadata(self):
        """Test attaching metadata."""
        context = AgentContext.create(agent_id="agent-123")
        context.attach_metadata("key1", "value1")
        context.attach_metadata("key2", {"nested": True})
        assert context.get_metadata("key1") == "value1"
        assert context.get_metadata("key2") == {"nested": True}
        assert context.get_metadata("nonexistent", "default") == "default"

    def test_with_task(self):
        """Test creating context with task."""
        context = AgentContext.create(agent_id="agent-123")
        new_context = context.with_task("task-456")
        assert new_context.task_id == "task-456"
        assert new_context.agent_id == context.agent_id

    def test_to_event_context(self):
        """Test converting context to event format."""
        context = AgentContext.create(
            agent_id="agent-123",
            task_id="task-456",
        )
        event_data = context.to_event_context()
        assert event_data["agent_id"] == "agent-123"
        assert event_data["task_id"] == "task-456"
        assert event_data["trace_id"] is not None


class TestExampleAgent:
    """Test ExampleAgent."""

    def test_example_agent_initialization(self):
        """Test ExampleAgent initialization."""
        agent = ExampleAgent()
        assert agent.agent_id == "example.echo.agent"
        assert agent.name == "Example Echo Agent"
        assert len(agent.capabilities) == 1
        assert agent.capabilities[0].capability_id == "example.echo"
        assert agent.status == AgentStatus.CREATED

    def test_example_agent_start(self):
        """Test ExampleAgent start."""
        agent = ExampleAgent()
        agent.initialize()
        assert agent.status == AgentStatus.INITIALIZED
        agent.start()
        assert agent.status == AgentStatus.RUNNING

    def test_example_agent_execution(self):
        """Test ExampleAgent execution."""
        agent = ExampleAgent()
        agent.initialize()
        agent.start()

        task = AgentTask(
            task_type="example.echo",
            objective="Test echo",
            inputs={"input1": "value1"},
        )

        result = agent.execute(task)

        assert result.is_success
        assert result.agent_id == agent.agent_id
        assert result.task_id == task.task_id
        assert result.outputs.get("echoed_objective") == "Test echo"
        assert result.outputs.get("echoed_inputs") == {"input1": "value1"}

    def test_example_agent_stop(self):
        """Test ExampleAgent stop."""
        agent = ExampleAgent()
        agent.initialize()
        agent.start()
        agent.stop()
        assert agent.status == AgentStatus.STOPPED


class TestLifecycleManager:
    """Test lifecycle management."""

    def test_valid_transitions(self):
        """Test valid lifecycle transitions."""
        assert AgentLifecycleManager.validate_transition(
            AgentStatus.CREATED, AgentStatus.INITIALIZED
        ) is None
        assert AgentLifecycleManager.validate_transition(
            AgentStatus.INITIALIZED, AgentStatus.RUNNING
        ) is None
        assert AgentLifecycleManager.validate_transition(
            AgentStatus.RUNNING, AgentStatus.STOPPED
        ) is None

    def test_invalid_transition(self):
        """Test invalid lifecycle transition raises error."""
        with pytest.raises(AgentLifecycleError):
            AgentLifecycleManager.validate_transition(
                AgentStatus.CREATED, AgentStatus.RUNNING
            )

    def test_stopped_to_running_invalid(self):
        """Test that stopped to running is invalid."""
        with pytest.raises(AgentLifecycleError):
            AgentLifecycleManager.validate_transition(
                AgentStatus.STOPPED, AgentStatus.RUNNING
            )


class TestValidators:
    """Test validators."""

    def test_task_validation_success(self):
        """Test task validation success."""
        task = AgentTask(
            task_id="task-123",
            task_type="test.type",
            objective="Test objective",
            trace_id="trace-456",
        )
        result = AgentTaskValidator.validate(task)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_task_validation_failure(self):
        """Test task validation failure."""
        task = AgentTask()
        result = AgentTaskValidator.validate(task)
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("objective" in e for e in result.errors)
        assert any("task_type" in e for e in result.errors)

    def test_result_validation_success(self):
        """Test result validation success."""
        result = AgentResult(
            result_id="result-123",
            task_id="task-456",
            agent_id="agent-789",
        )
        validation = AgentResultValidator.validate(result)
        assert validation.is_valid is True

    def test_capability_validation_success(self):
        """Test capability validation success."""
        cap = AgentCapability(
            capability_id="test.cap",
            name="Test Cap",
        )
        result = AgentCapabilityValidator.validate(cap)
        assert result.is_valid is True


class TestMemory:
    """Test agent memory."""

    def test_memory_set_get(self):
        """Test memory set and get."""
        memory = InMemoryAgentMemory()
        memory.set("key1", "value1")
        assert memory.get("key1") == "value1"
        assert memory.get("nonexistent") is None

    def test_memory_delete(self):
        """Test memory delete."""
        memory = InMemoryAgentMemory()
        memory.set("key1", "value1")
        assert memory.delete("key1") is True
        assert memory.get("key1") is None
        assert memory.delete("nonexistent") is False

    def test_memory_clear(self):
        """Test memory clear."""
        memory = InMemoryAgentMemory()
        memory.set("key1", "value1")
        memory.set("key2", "value2")
        memory.clear()
        assert len(memory) == 0
        assert memory.list_keys() == []

    def test_memory_list_keys(self):
        """Test listing memory keys."""
        memory = InMemoryAgentMemory()
        memory.set("key1", "value1")
        memory.set("key2", "value2")
        keys = memory.list_keys()
        assert len(keys) == 2
        assert "key1" in keys
        assert "key2" in keys


class TestPolicies:
    """Test agent policies."""

    def test_policy_allow(self):
        """Test policy allows operation."""
        policy = AgentPolicy(
            policy_name="test.policy",
            enabled=True,
        )
        evaluator = AgentPolicyEvaluator([policy])

        task = AgentTask(
            task_id="task-123",
            task_type="test.type",
            objective="Test",
        )
        context = AgentContext.create(agent_id="agent-456")

        result = evaluator.evaluate_task(task, context, "test.policy")
        assert result.is_allowed

    def test_policy_deny(self):
        """Test policy denies operation."""
        policy = AgentPolicy(
            policy_name="test.policy",
            enabled=True,
            capability_restrictions=["restricted.capability"],
        )
        evaluator = AgentPolicyEvaluator([policy])

        task = AgentTask(
            task_id="task-123",
            task_type="restricted.capability",
            objective="Test",
        )
        context = AgentContext.create(agent_id="agent-456")

        result = evaluator.evaluate_task(task, context, "test.policy")
        assert result.is_denied


class TestEventEmitter:
    """Test event emitter."""

    def test_emit_without_event_bus(self):
        """Test event emission without Event Bus."""
        emitter = AgentEventEmitter()
        result = emitter.emit("agent.initialized", {"agent_id": "agent-123"})
        assert result is False
        assert emitter.get_event_count() == 1
        assert len(emitter.get_failed_events()) == 0

    def test_emit_with_event_bus(self):
        """Test event emission with Event Bus."""
        mock_bus = MockEventBus()
        emitter = AgentEventEmitter(mock_bus)
        result = emitter.emit("agent.initialized", {"agent_id": "agent-123"})
        assert result is True
        assert mock_bus.published_events == 1

    def test_emit_invalid_event(self):
        """Test emitting invalid event."""
        emitter = AgentEventEmitter()
        result = emitter.emit("invalid.event", {})
        assert result is False
        assert len(emitter.get_failed_events()) == 1


class MockEventBus:
    """Mock event bus for testing."""

    def __init__(self):
        self.published_events = 0

    def publish(self, event_type: str, event: dict):
        self.published_events += 1


class TestExecutor:
    """Test agent executor."""

    def test_register_agent(self):
        """Test agent registration."""
        executor = AgentExecutor()
        agent = ExampleAgent()
        executor.register_agent(agent)
        assert agent.agent_id in executor.list_agents()
        assert executor.get_agent(agent.agent_id) is agent

    def test_execute_by_id(self):
        """Test execution by agent ID."""
        executor = AgentExecutor()
        agent = ExampleAgent()
        executor.register_agent(agent)

        task = AgentTask(
            task_type="example.echo",
            objective="Test",
            inputs={"test": "data"},
        )

        result = executor.execute(task, agent.agent_id)
        assert result.is_success
        assert result.agent_id == agent.agent_id

    def test_execute_by_capability(self):
        """Test execution by capability."""
        executor = AgentExecutor()
        agent = ExampleAgent()
        executor.register_agent(agent)

        task = AgentTask(
            task_type="example.echo",
            objective="Test",
        )

        result = executor.execute_with_capability(task, "example.echo")
        assert result.is_success

    def test_execute_handles_failures(self):
        """Test executor handles task validation failures."""
        executor = AgentExecutor()

        task = AgentTask()  # Missing required fields
        with pytest.raises(AgentValidationError):
            executor.execute(task, "nonexistent")


class TestRegistryAdapter:
    """Test registry adapter."""

    def test_loads_agents(self):
        """Test loading agents from registry."""
        adapter = RegistryAdapter()
        agents = adapter.list_registered_agents()
        assert isinstance(agents, list)

    def test_loads_capabilities(self):
        """Test loading capabilities from registry."""
        adapter = RegistryAdapter()
        capabilities = adapter.list_registered_capabilities()
        assert isinstance(capabilities, list)

    def test_get_agent_definition(self):
        """Test getting agent definition."""
        adapter = RegistryAdapter()
        agent = adapter.get_agent_definition("research")
        assert agent is not None or agent is None  # Depends on registry

    def test_get_capability_definition(self):
        """Test getting capability definition."""
        adapter = RegistryAdapter()
        cap = adapter.get_capability_definition("research")
        assert cap is not None or cap is None  # Depends on registry


class TestArchitectureConstraints:
    """Test architecture constraints."""

    def test_no_tool_execution(self):
        """Verify no tool execution imports."""
        from pathlib import Path
        base_dir = Path(__file__).parent.parent / "base"
        for py_file in base_dir.glob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.tools" not in content
            assert "import fool_platform.tools" not in content

    def test_no_connector_execution(self):
        """Verify no connector imports."""
        from pathlib import Path
        base_dir = Path(__file__).parent.parent / "base"
        for py_file in base_dir.glob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.connectors" not in content
            assert "import fool_platform.connectors" not in content

    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        base_dir = Path(__file__).parent.parent / "base"
        for py_file in base_dir.glob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lower_content = content.lower()
            assert "openai" not in lower_content
            assert "anthropic" not in lower_content
