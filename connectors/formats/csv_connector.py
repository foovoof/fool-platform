"""
connectors/formats/csv_connector.py

CSV Connector.

Reads CSV files.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import TYPE_CHECKING, Any, TextIO

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


class CsvConnector(BaseConnector):
    """
    CSV file connector.
    
    Only reads CSV files.
    No processing, no analysis.
    """
    
    connector_type = ConnectorType.CSV
    name = "CSV Connector"
    description = "Reads CSV files"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute CSV read."""
        source = request.source
        delimiter = request.parameters.get("delimiter", ",")
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"File not found: {source}")
                return result
            
            with open(path, "r", encoding="utf-8", newline="") as f:
                content = f.read()
            
            artifact = ConnectorArtifact(
                artifact_type="csv",
                name=path.name,
                content=content,
                content_type="text/csv",
                size=len(content),
                metadata={
                    "path": str(path),
                    "delimiter": delimiter,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except Exception as e:
            result.add_error(f"Failed to read CSV: {e}")
        
        return result
