"""
intelligence/capabilities/tests/test_capabilities.py

Tests for Intelligence Capabilities Foundation.
"""
from __future__ import annotations

import pytest
from pathlib import Path

from intelligence.capabilities.models import (
    CapabilityDefinition,
    CapabilityTask,
    CapabilityResult,
    CapabilityArtifact,
    CapabilityFinding,
    CapabilityExecutionRecord,
    CapabilityType,
    CapabilityStatus,
    FindingType,
)
from intelligence.capabilities.registry import (
    CapabilityRegistry,
    create_default_registry,
)
from intelligence.capabilities.agents import (
    BaseAgent,
    ResearchAgent,
    DiscoveryAgent,
    AgentFactory,
)
from intelligence.capabilities.execution import (
    CapabilityExecutor,
    CapabilityDispatcher,
    CapabilityResolver,
    ExecutionManager,
)
from intelligence.capabilities.pipelines import (
    CapabilityPipeline,
    PipelineStep,
    PipelineExecutor,
    create_default_pipeline,
)
from intelligence.capabilities.validation import (
    CapabilityValidator,
    TaskValidator,
    ResultValidator,
    PipelineValidator,
)
from intelligence.capabilities.events import (
    CapabilityEventEmitter,
    CapabilityEventType,
)
from intelligence.capabilities.services import (
    CapabilityService,
    ResearchService,
)


class TestCapabilityModels:
    """Test capability models."""
    
    def test_capability_definition_creation(self):
        """Test capability definition creation."""
        capability = CapabilityDefinition(
            name="Test Capability",
            description="A test capability",
            capability_type=CapabilityType.RESEARCH,
        )
        assert capability.capability_id
        assert capability.name == "Test Capability"
        assert capability.capability_type == CapabilityType.RESEARCH
    
    def test_capability_definition_to_dict(self):
        """Test capability serialization."""
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.DISCOVERY,
        )
        data = capability.to_dict()
        assert data["name"] == "Test"
        assert data["capability_type"] == "discovery"
    
    def test_capability_task_creation(self):
        """Test task creation."""
        task = CapabilityTask(
            capability_id="test-capability",
            capability_type=CapabilityType.RESEARCH,
            objective="Test objective",
        )
        assert task.task_id
        assert task.objective == "Test objective"
        assert task.status == CapabilityStatus.PENDING
    
    def test_capability_task_to_dict(self):
        """Test task serialization."""
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.EXTRACTION,
            objective="Extract data",
        )
        data = task.to_dict()
        assert data["capability_id"] == "test-cap"
        assert data["objective"] == "Extract data"
    
    def test_capability_result_creation(self):
        """Test result creation."""
        result = CapabilityResult(
            task_id="test-task",
            capability_id="test-capability",
            capability_type=CapabilityType.CORRELATION,
        )
        assert result.result_id
        assert result.status == CapabilityStatus.COMPLETED
    
    def test_capability_result_successful(self):
        """Test result success check."""
        result = CapabilityResult(
            task_id="test-task",
            capability_id="test-cap",
            status=CapabilityStatus.COMPLETED,
        )
        assert result.is_successful()
        
        failed_result = CapabilityResult(
            task_id="test-task",
            capability_id="test-cap",
            status=CapabilityStatus.FAILED,
            errors=["Test error"],
        )
        assert not failed_result.is_successful()
    
    def test_capability_result_findings_and_artifacts(self):
        """Test adding findings and artifacts."""
        result = CapabilityResult(task_id="test-task", capability_id="test-cap")
        
        finding = CapabilityFinding(
            title="Test Finding",
            finding_type=FindingType.OBSERVATION,
            confidence=0.8,
        )
        result.add_finding(finding)
        
        artifact = CapabilityArtifact(
            artifact_type="data",
            name="Test Artifact",
            content={"key": "value"},
        )
        result.add_artifact(artifact)
        
        assert len(result.findings) == 1
        assert len(result.artifacts) == 1
    
    def test_capability_finding_creation(self):
        """Test finding creation."""
        finding = CapabilityFinding(
            title="Important Finding",
            description="Test description",
            finding_type=FindingType.PATTERN,
            confidence=0.9,
        )
        assert finding.finding_id
        assert finding.title == "Important Finding"
        assert finding.confidence == 0.9
    
    def test_capability_artifact_creation(self):
        """Test artifact creation."""
        artifact = CapabilityArtifact(
            artifact_type="report",
            name="Test Report",
            content="# Test Report\nContent",
        )
        assert artifact.artifact_id
        assert artifact.artifact_type == "report"
    
    def test_capability_execution_record(self):
        """Test execution record."""
        record = CapabilityExecutionRecord(
            task_id="test-task",
            capability_id="test-cap",
            capability_type=CapabilityType.INVESTIGATION,
        )
        assert record.record_id
        assert record.status == CapabilityStatus.PENDING


class TestCapabilityRegistry:
    """Test capability registry."""
    
    def test_registry_creation(self):
        """Test registry creation."""
        registry = CapabilityRegistry()
        assert registry.count() == 0
    
    def test_register_capability(self):
        """Test capability registration."""
        registry = CapabilityRegistry()
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.RESEARCH,
        )
        success = registry.register(capability)
        assert success
        assert registry.count() == 1
    
    def test_get_capability(self):
        """Test getting capability."""
        registry = CapabilityRegistry()
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.DISCOVERY,
        )
        registry.register(capability)
        
        retrieved = registry.get(capability.capability_id)
        assert retrieved is not None
        assert retrieved.name == "Test"
    
    def test_get_by_type(self):
        """Test getting capability by type."""
        registry = CapabilityRegistry()
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.EXTRACTION,
        )
        registry.register(capability)
        
        retrieved = registry.get_by_type(CapabilityType.EXTRACTION)
        assert retrieved is not None
    
    def test_unregister_capability(self):
        """Test capability unregistration."""
        registry = CapabilityRegistry()
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.CORRELATION,
        )
        registry.register(capability)
        
        success = registry.unregister(capability.capability_id)
        assert success
        assert registry.count() == 0
    
    def test_search_capabilities(self):
        """Test capability search."""
        registry = CapabilityRegistry()
        capability = CapabilityDefinition(
            name="Research Capability",
            description="For research tasks",
            capability_type=CapabilityType.RESEARCH,
        )
        registry.register(capability)
        
        results = registry.search("research")
        assert len(results) >= 1
    
    def test_create_default_registry(self):
        """Test default registry creation."""
        registry = create_default_registry()
        assert registry.count() >= 9


class TestCapabilityAgents:
    """Test capability agents."""
    
    def test_base_agent_creation(self):
        """Test base agent creation."""
        agent = BaseAgent()
        assert agent.agent_id
        assert agent.agent_type == "base"
    
    def test_research_agent_execution(self):
        """Test research agent execution."""
        agent = ResearchAgent()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Research topic",
            inputs={"topic": "test"},
        )
        
        result = agent.execute(task)
        assert result.status == CapabilityStatus.COMPLETED
        assert len(result.findings) >= 1
    
    def test_discovery_agent_execution(self):
        """Test discovery agent execution."""
        agent = DiscoveryAgent()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.DISCOVERY,
            objective="Discover entities",
            inputs={"criteria": {}},
        )
        
        result = agent.execute(task)
        assert result.status == CapabilityStatus.COMPLETED
    
    def test_agent_factory(self):
        """Test agent factory."""
        agent = AgentFactory.create("research")
        assert agent is not None
        assert isinstance(agent, ResearchAgent)
        
        agent = AgentFactory.create("unknown")
        assert agent is None
    
    def test_agent_factory_list_types(self):
        """Test agent factory type listing."""
        types = AgentFactory.list_types()
        assert "research" in types
        assert "discovery" in types


class TestCapabilityExecution:
    """Test capability execution."""
    
    def test_executor_creation(self):
        """Test executor creation."""
        executor = CapabilityExecutor()
        assert executor is not None
    
    def test_executor_execution(self):
        """Test task execution."""
        executor = CapabilityExecutor()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test",
        )
        
        result = executor.execute(task)
        assert result is not None
        assert result.task_id == task.task_id
    
    def test_dispatcher_creation(self):
        """Test dispatcher creation."""
        dispatcher = CapabilityDispatcher()
        assert dispatcher is not None
    
    def test_dispatcher_dispatch(self):
        """Test task dispatch."""
        dispatcher = CapabilityDispatcher()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test",
        )
        
        result = dispatcher.dispatch(task)
        assert result is not None
    
    def test_resolver_creation(self):
        """Test resolver creation."""
        resolver = CapabilityResolver()
        assert resolver is not None
    
    def test_execution_manager(self):
        """Test execution manager."""
        manager = ExecutionManager()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test",
        )
        
        record = manager.create_record(task)
        assert record.record_id
        assert record.task_id == task.task_id


class TestCapabilityPipelines:
    """Test capability pipelines."""
    
    def test_pipeline_creation(self):
        """Test pipeline creation."""
        pipeline = CapabilityPipeline(
            name="Test Pipeline",
            capability_type=CapabilityType.RESEARCH,
        )
        assert pipeline.pipeline_id
        assert pipeline.name == "Test Pipeline"
    
    def test_pipeline_add_step(self):
        """Test adding step to pipeline."""
        pipeline = CapabilityPipeline(
            name="Test",
            capability_type=CapabilityType.DISCOVERY,
        )
        step = PipelineStep(name="Step 1", step_type="test")
        pipeline.add_step(step)
        assert len(pipeline.steps) == 1
        assert step.order == 0
    
    def test_pipeline_validation(self):
        """Test pipeline validation."""
        pipeline = CapabilityPipeline()
        is_valid, errors = pipeline.validate()
        assert not is_valid
        
        pipeline.name = "Test"
        is_valid, errors = pipeline.validate()
        assert not is_valid
        
        pipeline.add_step(PipelineStep(name="Step 1"))
        is_valid, errors = pipeline.validate()
        assert is_valid
    
    def test_pipeline_execution(self):
        """Test pipeline execution."""
        pipeline = CapabilityPipeline(
            name="Test",
            capability_type=CapabilityType.EXTRACTION,
        )
        pipeline.add_step(PipelineStep(
            name="Validate",
            step_type="validation",
            handler=lambda ctx: {"status": "passed"},
        ))
        
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.EXTRACTION,
            objective="Test",
        )
        
        result = pipeline.execute(task)
        assert result is not None
    
    def test_create_default_pipeline(self):
        """Test default pipeline creation."""
        pipeline = create_default_pipeline(CapabilityType.RESEARCH)
        assert pipeline.capability_type == CapabilityType.RESEARCH
        assert len(pipeline.steps) >= 1
    
    def test_pipeline_executor(self):
        """Test pipeline executor."""
        executor = PipelineExecutor()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test",
        )
        
        result = executor.execute(CapabilityType.RESEARCH, task)
        assert result is not None


class TestCapabilityValidators:
    """Test capability validators."""
    
    def test_capability_validator(self):
        """Test capability validation."""
        validator = CapabilityValidator()
        
        valid_capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.RESEARCH,
        )
        result = validator.validate(valid_capability)
        assert result.is_valid
        
        invalid_capability = CapabilityDefinition()
        result = validator.validate(invalid_capability)
        assert not result.is_valid
    
    def test_task_validator(self):
        """Test task validation."""
        validator = TaskValidator()
        
        valid_task = CapabilityTask(
            task_id="test-task",
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test",
        )
        result = validator.validate(valid_task)
        assert result.is_valid
        
        invalid_task = CapabilityTask()
        result = validator.validate(invalid_task)
        assert not result.is_valid
    
    def test_result_validator(self):
        """Test result validation."""
        validator = ResultValidator()
        
        result = CapabilityResult(
            task_id="test-task",
            capability_id="test-cap",
        )
        validation_result = validator.validate(result)
        assert validation_result.is_valid
    
    def test_pipeline_validator(self):
        """Test pipeline validation."""
        validator = PipelineValidator()
        
        pipeline = CapabilityPipeline(name="Test")
        pipeline.add_step(PipelineStep(name="Step 1"))
        result = validator.validate(pipeline)
        assert result.is_valid


class TestCapabilityEvents:
    """Test capability events."""
    
    def test_event_emitter_creation(self):
        """Test event emitter creation."""
        emitter = CapabilityEventEmitter()
        assert emitter is not None
    
    def test_emit_event(self):
        """Test event emission."""
        emitter = CapabilityEventEmitter()
        result = emitter.emit(
            CapabilityEventType.STARTED,
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            task_id="test-task",
        )
        assert result
    
    def test_emit_started(self):
        """Test started event."""
        emitter = CapabilityEventEmitter()
        result = emitter.emit_started(
            "test-cap",
            CapabilityType.RESEARCH,
            "test-task",
        )
        assert result
    
    def test_emit_completed(self):
        """Test completed event."""
        emitter = CapabilityEventEmitter()
        result = emitter.emit_completed(
            "test-cap",
            CapabilityType.RESEARCH,
            "test-task",
            "test-result",
        )
        assert result
    
    def test_get_events(self):
        """Test getting events."""
        emitter = CapabilityEventEmitter()
        emitter.emit_started("cap1", CapabilityType.RESEARCH, "task1")
        emitter.emit_completed("cap1", CapabilityType.RESEARCH, "task1", "result1")
        
        events = emitter.get_events()
        assert len(events) == 2


class TestCapabilityServices:
    """Test capability services."""
    
    def test_capability_service_creation(self):
        """Test capability service creation."""
        service = CapabilityService()
        assert service is not None
    
    def test_capability_service_register(self):
        """Test capability registration."""
        service = CapabilityService()
        capability = CapabilityDefinition(
            name="Test",
            capability_type=CapabilityType.RESEARCH,
        )
        success = service.register_capability(capability)
        assert success
    
    def test_capability_service_execute(self):
        """Test task execution."""
        service = CapabilityService()
        task = CapabilityTask(
            capability_id="test-cap",
            capability_type=CapabilityType.RESEARCH,
            objective="Test objective",
            inputs={"topic": "test"},
        )
        
        result = service.execute_task(task)
        assert result is not None
    
    def test_research_service(self):
        """Test research service."""
        service = ResearchService()
        result = service.execute("test topic")
        assert "task_id" in result


class TestArchitectureConstraints:
    """Test architecture constraints."""
    
    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        capabilities_dir = Path(__file__).parent.parent.parent
        for py_file in capabilities_dir.rglob("*.py"):
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
        
        capabilities_dir = Path(__file__).parent.parent.parent
        for py_file in capabilities_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_no_application_imports(self):
        """Verify no application imports."""
        from pathlib import Path
        
        capabilities_dir = Path(__file__).parent.parent.parent
        for py_file in capabilities_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from applications" not in content
            assert "import applications" not in content
    
    def test_no_cyber_imports(self):
        """Verify no cyber intelligence imports."""
        from pathlib import Path
        
        capabilities_dir = Path(__file__).parent.parent.parent
        for py_file in capabilities_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            # Check for actual imports, not documentation
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                if 'import' in line or 'from' in line:
                    assert "from cyber" not in line
                    assert "import cyber" not in line
                    assert "threat_intelligence" not in line.lower()
