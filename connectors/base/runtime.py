"""
connectors/base/runtime.py

Connector Runtime.

Runtime environment for connector execution.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from connectors.base.models import (
    ConnectorDefinition,
    ConnectorRequest,
    ConnectorResult,
    ConnectorArtifact,
    ConnectorStatus,
    ConnectorExecutionRecord,
    ConnectorType,
)
from connectors.base.events import ConnectorEventEmitter
from connectors.base.validation import RequestValidator

if TYPE_CHECKING:
    from connectors.base.connector import BaseConnector


class ConnectorRuntime:
    """
    Runtime environment for connectors.
    
    Responsibilities:
    - Register connectors
    - Manage connector instances
    - Execute requests
    - Maintain execution records
    - Emit events
    """
    
    def __init__(self) -> None:
        """Initialize runtime."""
        self._connectors: dict[str, BaseConnector] = {}
        self._definitions: dict[str, ConnectorDefinition] = {}
        self._records: list[ConnectorExecutionRecord] = []
        self._event_emitter = ConnectorEventEmitter()
        self._request_validator = RequestValidator()
    
    def register(self, connector: BaseConnector) -> bool:
        """
        Register a connector.
        
        Args:
            connector: Connector to register
            
        Returns:
            True if registered
        """
        if connector.connector_id in self._connectors:
            return False
        
        self._connectors[connector.connector_id] = connector
        
        definition = connector.get_definition()
        self._definitions[connector.connector_id] = definition
        
        return True
    
    def unregister(self, connector_id: str) -> bool:
        """
        Unregister a connector.
        
        Args:
            connector_id: ID of connector to unregister
            
        Returns:
            True if unregistered
        """
        if connector_id in self._connectors:
            del self._connectors[connector_id]
            del self._definitions[connector_id]
            return True
        return False
    
    def get(self, connector_id: str) -> BaseConnector | None:
        """Get connector by ID."""
        return self._connectors.get(connector_id)
    
    def list_connectors(self) -> list[ConnectorDefinition]:
        """List all registered connectors."""
        return list(self._definitions.values())
    
    def list_capabilities(self) -> dict[str, list[str]]:
        """List capabilities of all connectors."""
        return {
            cid: [c.value for c in conn.get_capabilities()]
            for cid, conn in self._connectors.items()
        }
    
    def health_check(self) -> dict[str, bool]:
        """Check health of all connectors."""
        return {
            cid: conn.health_check()
            for cid, conn in self._connectors.items()
        }
    
    def execute(self, request: ConnectorRequest) -> ConnectorResult:
        """
        Execute request through appropriate connector.
        
        Args:
            request: Request to execute
            
        Returns:
            Execution result
        """
        result = ConnectorResult(
            request_id=request.request_id,
            connector_id=request.connector_id,
            connector_type=request.connector_type,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        record = self._create_record(request)
        
        try:
            connector = self.get(request.connector_id)
            if not connector:
                result.add_error(f"Connector not found: {request.connector_id}")
                self._update_record(record, result)
                return result
            
            validation_result = self._request_validator.validate(request)
            if not validation_result.is_valid:
                result.add_error(
                    f"Request validation failed: {[i.message for i in validation_result.issues]}"
                )
                self._update_record(record, result)
                return result
            
            result = connector.execute(request)
        
        except Exception as e:
            result.add_error(str(e))
        
        finally:
            self._update_record(record, result)
        
        return result
    
    def _create_record(self, request: ConnectorRequest) -> ConnectorExecutionRecord:
        """Create execution record."""
        record = ConnectorExecutionRecord(
            request_id=request.request_id,
            connector_id=request.connector_id,
            connector_type=request.connector_type,
            operation=request.operation,
            inputs=request.inputs,
            parameters=request.parameters,
            status=ConnectorStatus.PENDING,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records.append(record)
        return record
    
    def _update_record(
        self,
        record: ConnectorExecutionRecord,
        result: ConnectorResult,
    ) -> None:
        """Update execution record."""
        record.result_id = result.result_id
        record.status = result.status
        record.completed_at = result.completed_at
        record.execution_time_ms = result.execution_time_ms
    
    def get_records(self) -> list[ConnectorExecutionRecord]:
        """Get execution records."""
        return self._records.copy()
    
    def get_record(self, record_id: str) -> ConnectorExecutionRecord | None:
        """Get record by ID."""
        for record in self._records:
            if record.record_id == record_id:
                return record
        return None
    
    def clear_records(self) -> None:
        """Clear execution records."""
        self._records.clear()


class ConnectorExecutor:
    """
    Executes connector requests.
    
    Responsibilities:
    - Prepare execution context
    - Execute connector
    - Collect results
    """
    
    def __init__(self, runtime: ConnectorRuntime) -> None:
        """Initialize executor."""
        self._runtime = runtime
    
    def execute(self, request: ConnectorRequest) -> ConnectorResult:
        """
        Execute request.
        
        Args:
            request: Request to execute
            
        Returns:
            Execution result
        """
        return self._runtime.execute(request)


class ConnectorDispatcher:
    """
    Dispatches requests to appropriate connectors.
    
    Responsibilities:
    - Resolve connector by ID or type
    - Route requests
    """
    
    def __init__(self, runtime: ConnectorRuntime) -> None:
        """Initialize dispatcher."""
        self._runtime = runtime
    
    def dispatch(self, request: ConnectorRequest) -> ConnectorResult:
        """
        Dispatch request.
        
        Args:
            request: Request to dispatch
            
        Returns:
            Execution result
        """
        connector = self._resolve_connector(request)
        
        if not connector:
            result = ConnectorResult(
                request_id=request.request_id,
                connector_id=request.connector_id,
                connector_type=request.connector_type,
            )
            result.add_error(
                f"No connector found for: {request.connector_id or request.connector_type.value}"
            )
            return result
        
        return connector.execute(request)
    
    def _resolve_connector(
        self,
        request: ConnectorRequest,
    ) -> BaseConnector | None:
        """Resolve connector for request."""
        if request.connector_id:
            return self._runtime.get(request.connector_id)
        
        for connector in self._runtime._connectors.values():
            if connector.connector_type == request.connector_type:
                return connector
        
        return None
