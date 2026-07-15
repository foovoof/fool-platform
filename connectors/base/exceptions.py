"""
connectors/base/exceptions.py

Connector Exceptions.
"""


class ConnectorError(Exception):
    """Base connector exception."""
    pass


class ConnectorInitializationError(ConnectorError):
    """Connector initialization error."""
    pass


class ConnectorStartError(ConnectorError):
    """Connector start error."""
    pass


class ConnectorStopError(ConnectorError):
    """Connector stop error."""
    pass


class ConnectorValidationError(ConnectorError):
    """Connector validation error."""
    pass


class ConnectorExecutionError(ConnectorError):
    """Connector execution error."""
    pass


class ConnectorTimeoutError(ConnectorError):
    """Connector timeout error."""
    pass


class ConnectorNotFoundError(ConnectorError):
    """Connector not found error."""
    pass


class ConnectorConfigurationError(ConnectorError):
    """Connector configuration error."""
    pass


class ConnectorPolicyError(ConnectorError):
    """Connector policy violation error."""
    pass


class ConnectorHealthCheckError(ConnectorError):
    """Connector health check error."""
    pass


class ConnectorArtifactError(ConnectorError):
    """Connector artifact error."""
    pass
