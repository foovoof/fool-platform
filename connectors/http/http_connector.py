"""
connectors/http/http_connector.py

HTTP Connector.

Fetches data via HTTP/HTTPS.
"""
from __future__ import annotations

import urllib.request
import urllib.error
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


class HttpConnector(BaseConnector):
    """
    HTTP/HTTPS connector.
    
    Only fetches data from URLs.
    No processing, no parsing.
    """
    
    connector_type = ConnectorType.HTTP
    name = "HTTP Connector"
    description = "Fetches data via HTTP/HTTPS"
    
    def get_capabilities(self) -> list[ConnectorCapability]:
        return [ConnectorCapability.READ]
    
    def _execute(
        self,
        request: ConnectorRequest,
        result: ConnectorResult,
    ) -> ConnectorResult:
        """Execute HTTP fetch."""
        source = request.source
        method = request.parameters.get("method", "GET")
        headers = request.parameters.get("headers", {})
        timeout = request.parameters.get("timeout", self.configuration.timeout)
        
        if not source.startswith(("http://", "https://")):
            result.add_error(f"Invalid URL: {source}")
            return result
        
        try:
            req = urllib.request.Request(
                url=source,
                method=method,
                headers=headers,
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
                status_code = response.status
                response_headers = dict(response.headers)
            
            artifact = ConnectorArtifact(
                artifact_type="http_response",
                name=source,
                content=content,
                content_type=response_headers.get("Content-Type", "application/octet-stream"),
                size=len(content),
                metadata={
                    "url": source,
                    "method": method,
                    "status_code": status_code,
                    "headers": response_headers,
                },
            )
            
            result.add_artifact(artifact)
            result.status = ConnectorStatus.COMPLETED
        
        except urllib.error.HTTPError as e:
            result.add_error(f"HTTP error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            result.add_error(f"URL error: {e.reason}")
        except Exception as e:
            result.add_error(f"Failed to fetch: {e}")
        
        return result
