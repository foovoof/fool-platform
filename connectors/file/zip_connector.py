"""
connectors/file/zip_connector.py

ZIP Connector.

Reads ZIP archive contents.
"""
from __future__ import annotations

import io
import zipfile
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


class ZipConnector(BaseConnector):
    """
    ZIP archive connector.
    
    Only extracts file data from ZIP.
    No processing, no parsing.
    """
    
    connector_type = ConnectorType.ZIP
    name = "ZIP Connector"
    description = "Extracts files from ZIP archives"
    
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
        """Execute ZIP extraction."""
        source = request.source
        member_name = request.parameters.get("member")
        list_only = request.parameters.get("list_only", False)
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"ZIP file not found: {source}")
                return result
            
            if not zipfile.is_zipfile(path):
                result.add_error(f"Not a valid ZIP file: {source}")
                return result
            
            with zipfile.ZipFile(path, "r") as zf:
                if list_only or member_name is None:
                    names = zf.namelist()
                    
                    artifact = ConnectorArtifact(
                        artifact_type="zip_listing",
                        name=path.name,
                        content={"members": names, "count": len(names)},
                        content_type="application/json",
                        size=len(str(names)),
                        metadata={
                            "source": str(path),
                            "member_count": len(names),
                        },
                    )
                    result.add_artifact(artifact)
                else:
                    data = zf.read(member_name)
                    
                    artifact = ConnectorArtifact(
                        artifact_type="zip_member",
                        name=member_name,
                        content=data,
                        content_type="application/octet-stream",
                        size=len(data),
                        metadata={
                            "source": str(path),
                            "member_name": member_name,
                        },
                    )
                    result.add_artifact(artifact)
            
            result.status = ConnectorStatus.COMPLETED
        
        except zipfile.BadZipFile:
            result.add_error(f"Invalid ZIP file: {source}")
        except KeyError:
            result.add_error(f"Member not found: {member_name}")
        except Exception as e:
            result.add_error(f"Failed to read ZIP: {e}")
        
        return result
