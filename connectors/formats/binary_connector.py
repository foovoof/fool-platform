"""
connectors/formats/binary_connector.py

Binary Connector.

Reads binary files.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

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


class BinaryConnector(BaseConnector):
    """
    Binary file connector.
    
    Only reads binary files.
    No processing.
    """
    
    connector_type = ConnectorType.BINARY
    name = "Binary Connector"
    description = "Reads binary files"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute binary read."""
        source = request.source
        offset = request.parameters.get("offset", 0)
        size = request.parameters.get("size")
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"File not found: {source}")
                return result
            
            if size is not None:
                with open(path, "rb") as f:
                    f.seek(offset)
                    content = f.read(size)
            else:
                with open(path, "rb") as f:
                    content = f.read()
            
            artifact = ConnectorArtifact(
                artifact_type="binary",
                name=path.name,
                content=content,
                content_type="application/octet-stream",
                size=len(content),
                metadata={
                    "path": str(path),
                    "offset": offset,
                    "size": len(content),
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except Exception as e:
            result.add_error(f"Failed to read binary: {e}")
        
        return result
