"""
connectors/formats/json_connector.py

JSON Connector.

Reads JSON files.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from connectors.base.connector import BaseConnector
from connectors.base.models import (
    ConnectorArtifact,
    ConnectorRequest,
    ConnectorResult,
    ConnectorStatus,
    ConnectorType,
    ConnectorCapability,
)

if TYPE_CHECKING:
    from connectors.base.runtime import ConnectorRuntime


class JsonConnector(BaseConnector):
    """
    JSON file connector.
    
    Only reads JSON files.
    No validation, no parsing beyond JSON parse.
    """
    
    connector_type = ConnectorType.JSON
    name = "JSON Connector"
    description = "Reads JSON files"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute JSON read."""
        source = request.source
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"File not found: {source}")
                return result
            
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
            
            content_str = json.dumps(content)
            
            artifact = ConnectorArtifact(
                artifact_type="json",
                name=path.name,
                content=content_str,
                content_type="application/json",
                size=len(content_str),
                metadata={
                    "path": str(path),
                    "parsed": True,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON: {e}")
        except Exception as e:
            result.add_error(f"Failed to read JSON: {e}")
        
        return result
