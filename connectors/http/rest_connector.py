"""
connectors/http/rest_connector.py

REST Connector.

Fetches data from REST APIs.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
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


class RestConnector(BaseConnector):
    """
    REST API connector.
    
    Only fetches data from REST endpoints.
    No processing, no parsing beyond JSON.
    """
    
    connector_type = ConnectorType.REST
    name = "REST Connector"
    description = "Fetches data from REST APIs"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute REST API call."""
        source = request.source
        method = request.parameters.get("method", "GET")
        headers = request.parameters.get("headers", {})
        body = request.parameters.get("body")
        timeout = request.parameters.get("timeout", self.configuration.timeout)
        
        if not source.startswith(("http://", "https://")):
            result.add_error(f"Invalid URL: {source}")
            return result
        
        try:
            headers["Accept"] = headers.get("Accept", "application/json")
            
            req_data = None
            if body is not None:
                req_data = json.dumps(body).encode("utf-8")
                headers["Content-Type"] = headers.get("Content-Type", "application/json")
            
            req = urllib.request.Request(
                url=source,
                method=method,
                data=req_data,
                headers=headers,
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
                status_code = response.status
                content_type = response.headers.get("Content-Type", "")
            
            artifact = ConnectorArtifact(
                artifact_type="rest_response",
                name=source,
                content=content,
                content_type=content_type,
                size=len(content),
                metadata={
                    "url": source,
                    "method": method,
                    "status_code": status_code,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except urllib.error.HTTPError as e:
            result.add_error(f"HTTP error {e.code}: {e.reason}")
            error_content = e.read()
            result.add_warning(f"Error body: {error_content[:500]}")
        except urllib.error.URLError as e:
            result.add_error(f"URL error: {e.reason}")
        except Exception as e:
            result.add_error(f"Failed to call REST API: {e}")
        
        return result
