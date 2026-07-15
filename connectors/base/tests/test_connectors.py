"""
connectors/base/tests/test_connectors.py

Tests for Data Connectors Foundation.
"""
from __future__ import annotations

import pytest
from pathlib import Path
import tempfile
import json

from connectors.base.models import (
    ConnectorStatus,
    ConnectorType,
    ConnectorCapability,
    ConnectorConfiguration,
    ConnectorRequest,
    ConnectorResult,
    ConnectorArtifact,
    ConnectorDefinition,
    ConnectorExecutionRecord,
    PolicyAction,
)
from connectors.base.lifecycle import ConnectorLifecycleManager
from connectors.base.policies import (
    ConnectorPolicyEngine,
    PolicyRule,
    PolicyResult,
    PolicyType,
)
from connectors.base.events import (
    ConnectorEventEmitter,
    ConnectorEventType,
)
from connectors.base.validation import (
    ConfigurationValidator,
    RequestValidator,
    LifecycleValidator,
    CapabilityValidator,
    ArtifactValidator,
    ValidationResult,
)
from connectors.base.connector import BaseConnector
from connectors.base.runtime import (
    ConnectorRuntime,
    ConnectorExecutor,
    ConnectorDispatcher,
)
from connectors.file.file_connector import FileConnector
from connectors.file.directory_connector import DirectoryConnector
from connectors.file.zip_connector import ZipConnector
from connectors.file.tar_connector import TarConnector
from connectors.formats.json_connector import JsonConnector
from connectors.formats.csv_connector import CsvConnector
from connectors.formats.text_connector import TextConnector
from connectors.formats.binary_connector import BinaryConnector
from connectors.http.http_connector import HttpConnector
from connectors.http.rest_connector import RestConnector


class TestConnectorModels:
    """Test connector models."""
    
    def test_connector_configuration(self):
        """Test configuration creation."""
        config = ConnectorConfiguration(
            connector_id="test-connector",
            name="Test",
            connector_type=ConnectorType.FILE,
        )
        assert config.connector_id == "test-connector"
        assert config.timeout == 30
    
    def test_connector_request(self):
        """Test request creation."""
        request = ConnectorRequest(
            connector_id="test",
            source="/path/to/file",
        )
        assert request.request_id
        assert request.source == "/path/to/file"
    
    def test_connector_result(self):
        """Test result creation."""
        result = ConnectorResult(
            request_id="req-1",
            connector_id="test",
        )
        assert result.result_id
        assert not result.is_successful()
    
    def test_connector_artifact(self):
        """Test artifact creation."""
        artifact = ConnectorArtifact(
            artifact_type="file",
            name="test.txt",
            content=b"hello",
        )
        assert artifact.artifact_id
        assert artifact.size == 0  # Size is not auto-calculated
    
    def test_connector_definition(self):
        """Test definition creation."""
        definition = ConnectorDefinition(
            name="Test",
            connector_type=ConnectorType.FILE,
        )
        assert definition.connector_id
        assert definition.capabilities == []
    
    def test_result_add_artifact(self):
        """Test adding artifact to result."""
        result = ConnectorResult(request_id="req", connector_id="test")
        artifact = ConnectorArtifact(name="test", content=b"data")
        result.add_artifact(artifact)
        assert len(result.artifacts) == 1
    
    def test_result_is_successful(self):
        """Test success check."""
        result = ConnectorResult(
            request_id="req",
            connector_id="test",
            status=ConnectorStatus.COMPLETED,
        )
        assert result.is_successful()
    
    def test_execution_record(self):
        """Test execution record."""
        record = ConnectorExecutionRecord(
            request_id="req",
            connector_id="test",
        )
        assert record.record_id


class TestConnectorLifecycle:
    """Test connector lifecycle."""
    
    def test_lifecycle_initial_state(self):
        """Test initial lifecycle state."""
        config = ConnectorConfiguration(connector_id="test")
        connector = BaseConnector(configuration=config)
        assert connector.status == ConnectorStatus.PENDING
    
    def test_lifecycle_transitions(self):
        """Test lifecycle state transitions."""
        config = ConnectorConfiguration(connector_id="test")
        connector = BaseConnector(configuration=config)
        
        connector.initialize()
        assert connector.status == ConnectorStatus.INITIALIZED
        
        connector.start()
        assert connector.status == ConnectorStatus.RUNNING
        
        connector.stop()
        assert connector.status == ConnectorStatus.STOPPED


class TestConnectorPolicies:
    """Test connector policies."""
    
    def test_policy_engine_creation(self):
        """Test policy engine creation."""
        engine = ConnectorPolicyEngine()
        assert engine is not None
    
    def test_policy_allow(self):
        """Test allow policy."""
        engine = ConnectorPolicyEngine()
        policy = PolicyRule(
            rule_id="allow-all",
            name="Allow All",
            action=PolicyAction.ALLOW,
        )
        engine.add_policy(policy)
        
        request = ConnectorRequest(
            connector_id="test",
            source="/path",
        )
        result = engine.evaluate(request)
        assert result.is_allowed()
    
    def test_policy_deny(self):
        """Test deny policy."""
        engine = ConnectorPolicyEngine()
        policy = PolicyRule(
            rule_id="deny-test",
            name="Deny Test",
            action=PolicyAction.DENY,
            conditions={"source": "/blocked"},
        )
        engine.add_policy(policy)
        
        request = ConnectorRequest(
            connector_id="test",
            source="/blocked",
        )
        result = engine.evaluate(request)
        assert result.is_denied()
    
    def test_policy_warn(self):
        """Test warn policy."""
        engine = ConnectorPolicyEngine()
        policy = PolicyRule(
            rule_id="warn-test",
            name="Warn Test",
            action=PolicyAction.WARN,
            conditions={"source": "/warn"},
        )
        engine.add_policy(policy)
        
        request = ConnectorRequest(
            connector_id="test",
            source="/warn",
        )
        result = engine.evaluate(request)
        assert result.is_warn()
    
    def test_default_engine(self):
        """Test default engine creation."""
        engine = ConnectorPolicyEngine.create_default_engine()
        assert len(engine.get_policies()) >= 1


class TestConnectorEvents:
    """Test connector events."""
    
    def test_event_emitter_creation(self):
        """Test event emitter creation."""
        emitter = ConnectorEventEmitter()
        assert emitter is not None
    
    def test_emit_event(self):
        """Test event emission."""
        emitter = ConnectorEventEmitter()
        result = emitter.emit(
            ConnectorEventType.INITIALIZED,
            connector_id="test",
            connector_type=ConnectorType.FILE,
        )
        assert result
    
    def test_get_events(self):
        """Test getting events."""
        emitter = ConnectorEventEmitter()
        emitter.emit_initialized("test", ConnectorType.FILE)
        emitter.emit_started("test", ConnectorType.FILE, "req-1")
        
        events = emitter.get_events()
        assert len(events) == 2


class TestConnectorValidation:
    """Test connector validation."""
    
    def test_configuration_validator(self):
        """Test configuration validation."""
        validator = ConfigurationValidator()
        config = ConnectorConfiguration(timeout=30)
        result = validator.validate(config)
        assert result.is_valid
    
    def test_configuration_validator_invalid(self):
        """Test configuration validation with invalid config."""
        validator = ConfigurationValidator()
        config = ConnectorConfiguration(timeout=-1)
        result = validator.validate(config)
        assert not result.is_valid
    
    def test_request_validator(self):
        """Test request validation."""
        validator = RequestValidator()
        request = ConnectorRequest(
            request_id="req-1",
            connector_id="test",
            source="/path",
        )
        result = validator.validate(request)
        assert result.is_valid
    
    def test_lifecycle_validator(self):
        """Test lifecycle validation."""
        validator = LifecycleValidator()
        result = validator.validate_state_transition(
            ConnectorStatus.PENDING,
            ConnectorStatus.INITIALIZED,
        )
        assert result.is_valid
    
    def test_capability_validator(self):
        """Test capability validation."""
        validator = CapabilityValidator()
        definition = ConnectorDefinition(
            connector_id="test",
            name="Test",
        )
        result = validator.validate_definition(definition)
        assert result.is_valid
    
    def test_artifact_validator(self):
        """Test artifact validation."""
        validator = ArtifactValidator()
        artifact = ConnectorArtifact(
            artifact_id="art-1",
            name="test",
        )
        result = validator.validate(artifact)
        assert result.is_valid


class TestConnectorRuntime:
    """Test connector runtime."""
    
    def test_runtime_creation(self):
        """Test runtime creation."""
        runtime = ConnectorRuntime()
        assert runtime is not None
    
    def test_register_connector(self):
        """Test connector registration."""
        runtime = ConnectorRuntime()
        config = ConnectorConfiguration(connector_id="test")
        connector = BaseConnector(configuration=config)
        
        success = runtime.register(connector)
        assert success
    
    def test_list_connectors(self):
        """Test listing connectors."""
        runtime = ConnectorRuntime()
        config = ConnectorConfiguration(connector_id="test")
        connector = BaseConnector(configuration=config)
        runtime.register(connector)
        
        connectors = runtime.list_connectors()
        assert len(connectors) == 1
    
    def test_execute_request(self):
        """Test request execution."""
        runtime = ConnectorRuntime()
        config = ConnectorConfiguration(connector_id="test")
        connector = BaseConnector(configuration=config)
        connector.initialize()
        connector.start()
        runtime.register(connector)
        
        request = ConnectorRequest(
            connector_id="test",
            source="/test",
        )
        result = runtime.execute(request)
        assert result is not None
    
    def test_executor(self):
        """Test connector executor."""
        runtime = ConnectorRuntime()
        executor = ConnectorExecutor(runtime)
        assert executor is not None
    
    def test_dispatcher(self):
        """Test connector dispatcher."""
        runtime = ConnectorRuntime()
        dispatcher = ConnectorDispatcher(runtime)
        assert dispatcher is not None


class TestFileConnectors:
    """Test file connectors."""
    
    def test_file_connector_creation(self):
        """Test file connector creation."""
        connector = FileConnector()
        assert connector.connector_type == ConnectorType.FILE
    
    def test_directory_connector_creation(self):
        """Test directory connector creation."""
        connector = DirectoryConnector()
        assert connector.connector_type == ConnectorType.DIRECTORY
    
    def test_zip_connector_creation(self):
        """Test ZIP connector creation."""
        connector = ZipConnector()
        assert connector.connector_type == ConnectorType.ZIP
    
    def test_tar_connector_creation(self):
        """Test TAR connector creation."""
        connector = TarConnector()
        assert connector.connector_type == ConnectorType.TAR


class TestFormatConnectors:
    """Test format connectors."""
    
    def test_json_connector_creation(self):
        """Test JSON connector creation."""
        connector = JsonConnector()
        assert connector.connector_type == ConnectorType.JSON
    
    def test_csv_connector_creation(self):
        """Test CSV connector creation."""
        connector = CsvConnector()
        assert connector.connector_type == ConnectorType.CSV
    
    def test_text_connector_creation(self):
        """Test text connector creation."""
        connector = TextConnector()
        assert connector.connector_type == ConnectorType.TEXT
    
    def test_binary_connector_creation(self):
        """Test binary connector creation."""
        connector = BinaryConnector()
        assert connector.connector_type == ConnectorType.BINARY


class TestHttpConnectors:
    """Test HTTP connectors."""
    
    def test_http_connector_creation(self):
        """Test HTTP connector creation."""
        connector = HttpConnector()
        assert connector.connector_type == ConnectorType.HTTP
    
    def test_rest_connector_creation(self):
        """Test REST connector creation."""
        connector = RestConnector()
        assert connector.connector_type == ConnectorType.REST


class TestArchitectureConstraints:
    """Test architecture constraints."""
    
    def test_no_knowledge_imports(self):
        """Verify no knowledge imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "knowledge" not in line.lower()
                    assert "from knowledge" not in line
    
    def test_no_inference_imports(self):
        """Verify no inference imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "inference" not in line.lower()
                    assert "from inference" not in line
    
    def test_no_intelligence_imports(self):
        """Verify no intelligence imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "intelligence" not in line.lower()
                    assert "from intelligence" not in line
    
    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "openai" not in line.lower()
                    assert "anthropic" not in line.lower()
                    assert "langchain" not in line.lower()
    
    def test_no_cyber_imports(self):
        """Verify no cyber imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "cyber" not in line.lower()
                    assert "from cyber" not in line
    
    def test_no_application_imports(self):
        """Verify no application imports."""
        from pathlib import Path
        
        connectors_dir = Path(__file__).parent.parent.parent
        for py_file in connectors_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'import' in line or 'from' in line:
                    assert "applications" not in line.lower()
                    assert "from applications" not in line
