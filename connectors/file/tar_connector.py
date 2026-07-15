"""
connectors/file/tar_connector.py

TAR Connector.

Reads TAR archive contents.
"""
from __future__ import annotations

import tarfile
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


class TarConnector(BaseConnector):
    """
    TAR archive connector.
    
    Only extracts file data from TAR.
    No processing, no parsing.
    """
    
    connector_type = ConnectorType.TAR
    name = "TAR Connector"
    description = "Extracts files from TAR archives"
    
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
        """Execute TAR extraction."""
        source = request.source
        member_name = request.parameters.get("member")
        list_only = request.parameters.get("list_only", False)
        
        try:
            path = Path(source)
            
            if not path.exists():
                result.add_error(f"TAR file not found: {source}")
                return result
            
            if not tarfile.is_tarfile(path):
                result.add_error(f"Not a valid TAR file: {source}")
                return result
            
            with tarfile.open(path, "r:*") as tf:
                if list_only or member_name is None:
                    names = tf.getnames()
                    
                    artifact = ConnectorArtifact(
                        artifact_type="tar_listing",
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
                    member = tf.extractfile(member_name)
                    if member is None:
                        result.add_error(f"Member not found: {member_name}")
                        return result
                    
                    data = member.read()
                    
                    artifact = ConnectorArtifact(
                        artifact_type="tar_member",
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
        
        except tarfile.TarError:
            result.add_error(f"Invalid TAR file: {source}")
        except KeyError:
            result.add_error(f"Member not found: {member_name}")
        except Exception as e:
            result.add_error(f"Failed to read TAR: {e}")
        
        return result
