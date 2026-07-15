"""
connectors/formats/text_connector.py

Text Connector.

Reads text files.
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


class TextConnector(BaseConnector):
    """
    Text file connector.
    
    Only reads text files.
    No encoding detection, no processing.
    """
    
    connector_type = ConnectorType.TEXT
    name = "Text Connector"
    description = "Reads text files"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute text read."""
        source = request.source
        encoding = request.parameters.get("encoding", "utf-8")
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"File not found: {source}")
                return result
            
            with open(path, "r", encoding=encoding) as f:
                content = f.read()
            
            artifact = ConnectorArtifact(
                artifact_type="text",
                name=path.name,
                content=content,
                content_type="text/plain",
                size=len(content),
                metadata={
                    "path": str(path),
                    "encoding": encoding,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except UnicodeDecodeError:
            result.add_error(f"Encoding error with {encoding}: {source}")
        except Exception as e:
            result.add_error(f"Failed to read text: {e}")
        
        return result
