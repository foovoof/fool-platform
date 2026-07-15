"""
connectors/file/directory_connector.py

Directory Connector.

Lists directory contents.
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


class DirectoryConnector(BaseConnector):
    """
    Directory listing connector.
    
    Only lists directory contents.
    No file reading, no processing.
    """
    
    connector_type = ConnectorType.DIRECTORY
    name = "Directory Connector"
    description = "Lists directory contents"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [
            ConnectorCapability.LIST,
            ConnectorCapability.SEARCH,
        ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute directory listing."""
        source = request.source
        pattern = request.parameters.get("pattern", "*")
        recursive = request.parameters.get("recursive", False)
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"Directory not found: {source}")
                return result
            
            if not path.is_dir():
                result.add_error(f"Not a directory: {source}")
                return result
            
            entries = []
            
            if recursive:
                for item in path.rglob(pattern):
                    entries.append(self._entry_info(item))
            else:
                for item in path.glob(pattern):
                    entries.append(self._entry_info(item))
            
            artifact = ConnectorArtifact(
                artifact_type="directory_listing",
                name=path.name,
                content=entries,
                content_type="application/json",
                size=len(str(entries)),
                metadata={
                    "path": str(path),
                    "pattern": pattern,
                    "recursive": recursive,
                    "entry_count": len(entries),
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except PermissionError:
            result.add_error(f"Permission denied: {source}")
        except Exception as e:
            result.add_error(f"Failed to list directory: {e}")
        
        return result
    
    def _entry_info(self, path: Path) -> dict:
        """Get entry information."""
        try:
            stat = path.stat()
            return {
                "name": path.name,
                "path": str(path),
                "type": "directory" if path.is_dir() else "file",
                "size": stat.st_size if path.is_file() else 0,
            }
        except Exception:
            return {
                "name": path.name,
                "path": str(path),
                "type": "unknown",
                "size": 0,
            }
