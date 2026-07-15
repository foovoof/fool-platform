"""
connectors/file/file_connector.py

File Connector.

Reads files from the filesystem.
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
from connectors.base.exceptions import ConnectorExecutionError

if TYPE_CHECKING:
    from connectors.base.runtime import ConnectorRuntime


class FileConnector(BaseConnector):
    """
    File system connector.
    
    Only retrieves file contents.
    No parsing, no processing.
    """
    
    connector_type = ConnectorType.FILE
    name = "File Connector"
    description = "Reads files from filesystem"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [
            ConnectorCapability.READ,
            ConnectorCapability.LIST,
        ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute file read."""
        source = request.source
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"File not found: {source}")
                return result
            
            if not path.is_file():
                result.add_error(f"Not a file: {source}")
                return result
            
            if path.stat().st_size > self.configuration.max_size:
                result.add_error(f"File too large: {path.stat().st_size} > {self.configuration.max_size}")
                return result
            
            with open(path, "rb") as f:
                content = f.read()
            
            artifact = ConnectorArtifact(
                artifact_type="file",
                name=path.name,
                content=content,
                content_type=self._guess_content_type(path),
                size=len(content),
                metadata={
                    "path": str(path),
                    "absolute_path": str(path.absolute()),
                    "file_size": path.stat().st_size,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except PermissionError:
            result.add_error(f"Permission denied: {source}")
        except Exception as e:
            result.add_error(f"Failed to read file: {e}")
        
        return result
    
    def _guess_content_type(self, path: Path) -> str:
        """Guess content type from extension."""
        ext = path.suffix.lower()
        content_types = {
            ".txt": "text/plain",
            ".json": "application/json",
            ".xml": "application/xml",
            ".csv": "text/csv",
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".py": "text/x-python",
            ".md": "text/markdown",
            ".yaml": "application/yaml",
            ".yml": "application/yaml",
        }
        return content_types.get(ext, "application/octet-stream")
