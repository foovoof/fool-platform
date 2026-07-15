"""
connectors/base/connector.py

Base Connector.

Foundation for all connectors.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from connectors.base.models import (
    ConnectorConfiguration,
    ConnectorRequest,
    ConnectorResult,
    ConnectorArtifact,
    ConnectorDefinition,
    ConnectorStatus,
    ConnectorType,
    ConnectorCapability,
    ConnectorExecutionRecord,
)
from connectors.base.lifecycle import ConnectorLifecycleManager
from connectors.base.policies import ConnectorPolicyEngine, PolicyResult
from connectors.base.events import ConnectorEventEmitter
from connectors.base.validation import (
    RequestValidator,
    LifecycleValidator,
)
from connectors.base.exceptions import (
    ConnectorInitializationError,
    ConnectorStartError,
    ConnectorStopError,
    ConnectorValidationError,
    ConnectorExecutionError,
)

if TYPE_CHECKING:
    from connectors.base.runtime import ConnectorRuntime


class BaseConnector:
    """
    Base connector implementation.
    
    Responsibilities:
    - Lifecycle management
    - Request validation
    - Policy evaluation
    - Event emission
    - Execution timing
    - Error handling
    - Result generation
    
    Subclasses implement:
    - _execute()
    """
    
    connector_type: ConnectorType = ConnectorType.GENERIC
    name: str = "Base Connector"
    description: str = "Generic base connector"
    
    def __init__(
        self,
        configuration: ConnectorConfiguration | None = None,
        runtime: ConnectorRuntime | None = None,
    ) -> None:
        """Initialize connector."""
        self.connector_id = configuration.connector_id if configuration else str(uuid4())
        self.configuration = configuration or ConnectorConfiguration(
            connector_id=self.connector_id,
            name=self.name,
            description=self.description,
            connector_type=self.connector_type,
        )
        self._runtime = runtime
        
        self._lifecycle = ConnectorLifecycleManager(self)
        self._policy_engine = ConnectorPolicyEngine.create_default_engine()
        self._event_emitter = ConnectorEventEmitter()
        self._request_validator = RequestValidator()
        self._lifecycle_validator = LifecycleValidator()
        self._initialized = False
        self._started = False
    
    @property
    def status(self) -> ConnectorStatus:
        """Get current status."""
        return self._lifecycle.status
    
    def initialize(self) -> None:
        """
        Initialize connector.
        
        Raises:
            ConnectorInitializationError: If initialization fails
        """
        try:
            self._lifecycle.initialize()
            self._initialized = True
            self._event_emitter.emit_initialized(
                self.connector_id,
                self.connector_type,
            )
        except Exception as e:
            self._lifecycle.fail(str(e))
            raise ConnectorInitializationError(f"Failed to initialize: {e}") from e
    
    def start(self) -> None:
        """
        Start connector.
        
        Raises:
            ConnectorStartError: If start fails
        """
        if not self._initialized:
            raise ConnectorStartError("Connector not initialized")
        
        try:
            self._lifecycle.start()
            self._started = True
            self._lifecycle.running()
        except Exception as e:
            self._lifecycle.fail(str(e))
            raise ConnectorStartError(f"Failed to start: {e}") from e
    
    def stop(self) -> None:
        """
        Stop connector.
        
        Raises:
            ConnectorStopError: If stop fails
        """
        try:
            self._lifecycle.stop()
            self._started = False
            self._lifecycle.stopped()
            self._event_emitter.emit_stopped(
                self.connector_id,
                self.connector_type,
            )
        except Exception as e:
            self._lifecycle.fail(str(e))
            raise ConnectorStopError(f"Failed to stop: {e}") from e
    
    def validate_request(self, request: ConnectorRequest) -> bool:
        """
        Validate request.
        
        Args:
            request: Request to validate
            
        Returns:
            True if valid
            
        Raises:
            ConnectorValidationError: If validation fails
        """
        result = self._request_validator.validate(request)
        
        self._event_emitter.emit_validated(
            self.connector_id,
            self.connector_type,
            request.request_id,
            result.is_valid,
        )
        
        if not result.is_valid:
            raise ConnectorValidationError(
                f"Request validation failed: {[i.message for i in result.issues]}"
            )
        
        return True
    
    def _evaluate_policies(self, request: ConnectorRequest) -> PolicyResult:
        """Evaluate policies for request."""
        return self._policy_engine.evaluate(request)
    
    def execute(self, request: ConnectorRequest) -> ConnectorResult:
        """
        Execute connector request.
        
        Args:
            request: Request to execute
            
        Returns:
            Execution result
        """
        result = ConnectorResult(
            request_id=request.request_id,
            connector_id=self.connector_id,
            connector_type=self.connector_type,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        start_time = time.time()
        
        try:
            self.validate_request(request)
            
            policy_result = self._evaluate_policies(request)
            if policy_result.is_denied():
                result.add_error(policy_result.denied_reason)
                return result
            
            if policy_result.is_warn():
                result.add_warning(
                    f"Policy warning: {', '.join(policy_result.matched_rules)}"
                )
            
            self._event_emitter.emit_started(
                self.connector_id,
                self.connector_type,
                request.request_id,
            )
            
            result = self._execute(request, result)
            
            if result.is_successful():
                result.status = ConnectorStatus.COMPLETED
                self._event_emitter.emit_completed(
                    self.connector_id,
                    self.connector_type,
                    request.request_id,
                    result.result_id,
                )
        
        except ConnectorValidationError as e:
            result.add_error(str(e))
            self._event_emitter.emit_failed(
                self.connector_id,
                self.connector_type,
                request.request_id,
                str(e),
            )
        
        except Exception as e:
            result.add_error(str(e))
            self._event_emitter.emit_failed(
                self.connector_id,
                self.connector_type,
                request.request_id,
                str(e),
            )
        
        finally:
            result.completed_at = datetime.now(timezone.utc).isoformat()
            result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """
        Execute connector-specific logic.
        
        Subclasses override this method.
        
        Args:
            request: Request to execute
            result: Result to populate
            
        Returns:
            Populated result
        """
        raise NotImplementedError("Subclasses must implement _execute()")
    
    def health_check(self) -> bool:
        """
        Perform health check.
        
        Returns:
            True if healthy
        """
        return self._initialized and self._started
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        """Get connector capabilities."""
        return [
            ConnectorCapability.READ,
            ConnectorCapability.LIST,
        ]
    
    def get_definition(self) -> ConnectorDefinition:
        """Get connector definition."""
        return ConnectorDefinition(
            connector_id=self.connector_id,
            name=self.name,
            description=self.description,
            connector_type=self.connector_type,
            capabilities=self.get_capabilities(),
            configuration=self.configuration,
        )
    
    def get_lifecycle_events(self) -> list[dict]:
        """Get lifecycle events."""
        return self._lifecycle.get_events()
    
    def get_events(self) -> list:
        """Get emitted events."""
        return self._event_emitter.get_events()
