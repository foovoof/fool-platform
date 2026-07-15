"""
intelligence/tests/test_intelligence.py

Tests for Intelligence Runtime Foundation.
"""
from __future__ import annotations

import pytest
from pathlib import Path

from intelligence.models import (
    IntelligenceTask,
    IntelligenceResult,
    IntelligenceFinding,
    IntelligenceArtifact,
    TaskStatus,
    FindingType,
    ArtifactType,
    ResultStatus,
)
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.runtime import (
    IntelligenceRuntime,
    RuntimeExecutor,
    RuntimeDispatcher,
    RuntimeScheduler,
)
from intelligence.pipeline import (
    Pipeline,
    PipelineStep,
    PipelineExecutor,
    PipelineRegistry,
    StepStatus,
)
from intelligence.validation import RuntimeValidator, ValidationResult
from intelligence.events import (
    IntelligenceEventEmitter,
    IntelligenceEventType,
)
from intelligence.services import (
    IntelligenceRuntimeService,
    PipelineService,
    SessionService,
    FindingService,
    ArtifactService,
    ExecutionService,
)
from intelligence.registry import RegistryIntegration


class TestIntelligenceModels:
    """Test intelligence models."""

    def test_task_creation(self):
        """Test task creation."""
        task = IntelligenceTask(
            task_type="test",
            objective="Test objective",
            inputs={"key": "value"},
        )
        assert task.task_id
        assert task.task_type == "test"
        assert task.objective == "Test objective"
        assert task.inputs["key"] == "value"
        assert task.status == TaskStatus.PENDING

    def test_task_is_valid(self):
        """Test task validation."""
        task = IntelligenceTask(task_type="test", objective="Test")
        assert task.is_valid()

        empty_task = IntelligenceTask()
        assert not empty_task.is_valid()

    def test_task_to_dict(self):
        """Test task serialization."""
        task = IntelligenceTask(
            task_type="test",
            objective="Test",
        )
        data = task.to_dict()
        assert data["task_type"] == "test"
        assert data["objective"] == "Test"
        assert "task_id" in data

    def test_result_creation(self):
        """Test result creation."""
        result = IntelligenceResult(
            task_id="test-task",
            status=ResultStatus.SUCCESS,
        )
        assert result.result_id
        assert result.task_id == "test-task"
        assert result.status == ResultStatus.SUCCESS

    def test_result_findings_and_artifacts(self):
        """Test adding findings and artifacts."""
        result = IntelligenceResult(task_id="test-task")
        
        finding = IntelligenceFinding(
            title="Test Finding",
            finding_type=FindingType.OBSERVATION,
            confidence=0.8,
        )
        result.add_finding(finding)
        assert len(result.findings) == 1

        artifact = IntelligenceArtifact(
            artifact_type=ArtifactType.DATA,
            content={"key": "value"},
        )
        result.add_artifact(artifact)
        assert len(result.artifacts) == 1

    def test_result_recommendations(self):
        """Test adding recommendations."""
        result = IntelligenceResult(task_id="test-task")
        result.add_recommendation(
            recommendation_type="action",
            action="Test action",
            rationale="Test rationale",
        )
        assert len(result.recommendations) == 1

    def test_finding_creation(self):
        """Test finding creation."""
        finding = IntelligenceFinding(
            title="Test Finding",
            description="Test description",
            confidence=0.75,
            finding_type=FindingType.PATTERN,
        )
        assert finding.finding_id
        assert finding.confidence == 0.75
        assert finding.finding_type == FindingType.PATTERN

    def test_finding_validation(self):
        """Test finding validation."""
        valid_finding = IntelligenceFinding(
            title="Valid",
            confidence=0.5,
        )
        assert valid_finding.is_valid()

        invalid_finding = IntelligenceFinding(
            title="",
            confidence=1.5,
        )
        assert not invalid_finding.is_valid()


class TestIntelligenceContext:
    """Test intelligence context."""

    def test_context_creation(self):
        """Test context creation."""
        context = IntelligenceContext(
            workflow_id="wf-1",
            execution_id="exec-1",
        )
        assert context.context_id
        assert context.workflow_id == "wf-1"
        assert context.execution_id == "exec-1"

    def test_child_context(self):
        """Test child context creation."""
        parent = IntelligenceContext(
            workflow_id="wf-1",
            session_id="session-1",
        )
        child = parent.create_child(
            workflow_id="wf-2",
            execution_id="exec-2",
        )
        assert child.parent_context_id == parent.context_id
        assert child.workflow_id == "wf-2"
        assert child.session_id == parent.session_id

    def test_event_context_conversion(self):
        """Test event context conversion."""
        context = IntelligenceContext(
            workflow_id="wf-1",
            session_id="session-1",
        )
        event_ctx = context.to_event_context()
        assert event_ctx["workflow_id"] == "wf-1"
        assert event_ctx["session_id"] == "session-1"


class TestIntelligenceSession:
    """Test intelligence session."""

    def test_session_creation(self):
        """Test session creation."""
        session = IntelligenceSession()
        assert session.session_id
        assert session.status == "active"
        assert len(session.tasks) == 0

    def test_session_add_task(self):
        """Test adding task to session."""
        session = IntelligenceSession()
        task = IntelligenceTask(task_type="test", objective="Test")
        session.add_task(task)
        assert len(session.tasks) == 1

    def test_session_add_result(self):
        """Test adding result to session."""
        session = IntelligenceSession()
        task = IntelligenceTask(task_type="test", objective="Test")
        session.add_task(task)

        result = IntelligenceResult(task_id=task.task_id)
        result.add_finding(IntelligenceFinding(title="Finding"))
        session.add_result(result)

        assert len(session.results) == 1
        assert len(session.findings) == 1

    def test_session_mark_completed(self):
        """Test marking session completed."""
        session = IntelligenceSession()
        session.mark_completed()
        assert session.status == "completed"
        assert session.completed_at is not None

    def test_session_get_summary(self):
        """Test session summary."""
        session = IntelligenceSession()
        task = IntelligenceTask(task_type="test", objective="Test")
        session.add_task(task)
        
        summary = session.get_summary()
        assert summary["task_count"] == 1
        assert summary["status"] == "active"


class TestRuntimeExecutor:
    """Test runtime executor."""

    def test_executor_creation(self):
        """Test executor creation."""
        executor = RuntimeExecutor()
        assert executor is not None

    def test_execute_step(self):
        """Test step execution."""
        executor = RuntimeExecutor()
        step = PipelineStep(
            name="Test Step",
            step_type="test",
        )
        result = executor.execute_step(step, IntelligenceTask())
        assert result["step_name"] == "Test Step"


class TestRuntimeDispatcher:
    """Test runtime dispatcher."""

    def test_dispatcher_creation(self):
        """Test dispatcher creation."""
        dispatcher = RuntimeDispatcher()
        assert dispatcher is not None

    def test_register_handler(self):
        """Test handler registration."""
        dispatcher = RuntimeDispatcher()
        
        def handler(task, context):
            return {"handled": True}
        
        dispatcher.register_handler("test", handler)
        assert dispatcher.get_handler("test") is handler

    def test_dispatch(self):
        """Test task dispatch."""
        dispatcher = RuntimeDispatcher()
        
        def handler(task, context):
            return {"result": task.task_type}
        
        dispatcher.register_handler("test", handler)
        
        task = IntelligenceTask(task_type="test", objective="Test")
        result = dispatcher.dispatch(task)
        
        assert result["result"] == "test"


class TestRuntimeScheduler:
    """Test runtime scheduler."""

    def test_scheduler_creation(self):
        """Test scheduler creation."""
        scheduler = RuntimeScheduler()
        assert scheduler.queue_size() == 0

    def test_submit_task(self):
        """Test task submission."""
        scheduler = RuntimeScheduler()
        task = IntelligenceTask(task_type="test", objective="Test")
        schedule_id = scheduler.submit(task)
        assert schedule_id
        assert scheduler.queue_size() == 1

    def test_get_next(self):
        """Test getting next task."""
        scheduler = RuntimeScheduler()
        task = IntelligenceTask(task_type="test", objective="Test")
        scheduler.submit(task)
        
        next_task = scheduler.get_next()
        assert next_task is not None
        assert next_task.task_type == "test"
        assert scheduler.queue_size() == 0


class TestPipeline:
    """Test pipeline."""

    def test_pipeline_creation(self):
        """Test pipeline creation."""
        pipeline = Pipeline(
            name="Test Pipeline",
            task_type="test",
        )
        assert pipeline.pipeline_id
        assert pipeline.name == "Test Pipeline"
        assert len(pipeline.steps) == 0

    def test_add_step(self):
        """Test adding step to pipeline."""
        pipeline = Pipeline(name="Test")
        step = PipelineStep(name="Step 1")
        pipeline.add_step(step)
        assert len(pipeline.steps) == 1
        assert step.order == 0

    def test_pipeline_validation(self):
        """Test pipeline validation."""
        pipeline = Pipeline(name="Test")
        is_valid, errors = pipeline.validate()
        assert not is_valid
        assert "no steps" in errors[0]


class TestPipelineExecutor:
    """Test pipeline executor."""

    def test_executor_creation(self):
        """Test executor creation."""
        executor = PipelineExecutor()
        assert executor is not None

    def test_execute_pipeline(self):
        """Test pipeline execution."""
        executor = PipelineExecutor()
        
        step = PipelineStep(
            name="Test Step",
            step_type="test",
        )
        pipeline = Pipeline(name="Test")
        pipeline.add_step(step)
        
        results = executor.execute(pipeline)
        assert len(results) == 1
        assert results[0]["name"] == "Test Step"


class TestPipelineRegistry:
    """Test pipeline registry."""

    def test_registry_creation(self):
        """Test registry creation."""
        registry = PipelineRegistry()
        assert registry is not None

    def test_register_pipeline(self):
        """Test pipeline registration."""
        registry = PipelineRegistry()
        pipeline = Pipeline(name="Test", task_type="test")
        step = PipelineStep(name="Step 1", step_type="test", required=False)
        pipeline.add_step(step)
        success = registry.register_pipeline(pipeline)
        assert success

        retrieved = registry.get_pipeline("test")
        assert retrieved is not None
        assert retrieved.name == "Test"


class TestRuntimeValidator:
    """Test runtime validator."""

    def test_validator_creation(self):
        """Test validator creation."""
        validator = RuntimeValidator()
        assert validator is not None

    def test_validate_task(self):
        """Test task validation."""
        validator = RuntimeValidator()
        
        valid_task = IntelligenceTask(
            task_type="test",
            objective="Test",
        )
        result = validator.validate_task(valid_task)
        assert result.is_valid

        invalid_task = IntelligenceTask()
        result = validator.validate_task(invalid_task)
        assert not result.is_valid

    def test_validate_context(self):
        """Test context validation."""
        validator = RuntimeValidator()
        context = IntelligenceContext()
        result = validator.validate_context(context)
        assert result.is_valid

    def test_validate_session(self):
        """Test session validation."""
        validator = RuntimeValidator()
        session = IntelligenceSession()
        result = validator.validate_session(session)
        assert result.is_valid

    def test_validate_pipeline(self):
        """Test pipeline validation."""
        validator = RuntimeValidator()
        
        pipeline = Pipeline(name="Test")
        result = validator.validate_pipeline(pipeline)
        assert not result.is_valid


class TestIntelligenceEventEmitter:
    """Test intelligence event emitter."""

    def test_emitter_creation(self):
        """Test emitter creation."""
        emitter = IntelligenceEventEmitter()
        assert emitter is not None
        assert not emitter.has_event_bus

    def test_emit_without_bus(self):
        """Test emitting without event bus."""
        emitter = IntelligenceEventEmitter()
        result = emitter.emit("test.event", {})
        assert not result

    def test_emit_session_started(self):
        """Test emitting session started event."""
        emitter = IntelligenceEventEmitter()
        result = emitter.emit_session_started("session-1", "task-1")
        assert not result
        assert emitter.get_event_count() == 1


class TestIntelligenceRuntime:
    """Test intelligence runtime."""

    def test_runtime_creation(self):
        """Test runtime creation."""
        runtime = IntelligenceRuntime()
        assert runtime is not None

    def test_execute_task(self):
        """Test task execution."""
        runtime = IntelligenceRuntime()
        
        task = IntelligenceTask(
            task_type="test",
            objective="Test objective",
        )
        
        result = runtime.execute_task(task)
        assert result is not None
        assert result.task_id == task.task_id


class TestServices:
    """Test intelligence services."""

    def test_intelligence_runtime_service(self):
        """Test runtime service."""
        service = IntelligenceRuntimeService()
        task = IntelligenceTask(task_type="test", objective="Test")
        
        result = service.execute(task)
        assert "success" in result
        assert result["task_id"] == task.task_id

    def test_pipeline_service(self):
        """Test pipeline service."""
        service = PipelineService()
        
        pipeline_data = service.create_pipeline(
            name="Test",
            task_type="test",
        )
        assert pipeline_data["name"] == "Test"

    def test_session_service(self):
        """Test session service."""
        service = SessionService()
        
        session_data = service.create_session()
        assert "session_id" in session_data

    def test_finding_service(self):
        """Test finding service."""
        service = FindingService()
        
        finding_data = service.create_finding(
            finding_type="observation",
            title="Test Finding",
            description="Test description",
        )
        assert finding_data["title"] == "Test Finding"

    def test_artifact_service(self):
        """Test artifact service."""
        service = ArtifactService()
        
        artifact_data = service.create_artifact(
            artifact_type="data",
            content={"key": "value"},
        )
        assert artifact_data["artifact_type"] == "data"

    def test_execution_service(self):
        """Test execution service."""
        service = ExecutionService()
        task = IntelligenceTask(task_type="test", objective="Test")
        
        result = service.submit_task(task)
        assert "result_id" in result


class TestRegistryIntegration:
    """Test registry integration."""

    def test_integration_creation(self):
        """Test integration creation."""
        integration = RegistryIntegration()
        assert integration is not None

    def test_no_registry_configured(self):
        """Test without registries."""
        integration = RegistryIntegration()
        
        assert not integration.has_agent_registry
        assert not integration.has_capability_registry
        assert not integration.has_workflow_registry
        
        assert integration.get_agent("test") is None
        assert integration.list_agents() == []


class TestArchitectureConstraints:
    """Test architecture constraints."""

    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        intelligence_dir = Path(__file__).parent.parent.parent
        for py_file in intelligence_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('#'):
                    continue
                lower_line = line.lower()
                if 'import' in lower_line or 'from' in lower_line:
                    assert "openai" not in lower_line
                    assert "anthropic" not in lower_line
                    assert "langchain" not in lower_line

    def test_no_connector_imports(self):
        """Verify no connector imports."""
        from pathlib import Path
        
        intelligence_dir = Path(__file__).parent.parent.parent
        for py_file in intelligence_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content

    def test_no_application_imports(self):
        """Verify no application imports."""
        from pathlib import Path
        
        intelligence_dir = Path(__file__).parent.parent.parent
        for py_file in intelligence_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from applications" not in content
            assert "import applications" not in content

    def test_no_planning_imports(self):
        """Verify no planning imports."""
        from pathlib import Path
        
        intelligence_dir = Path(__file__).parent.parent.parent
        for py_file in intelligence_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from planning" not in content
            assert "import planning" not in content
