"""
platform/kernel/health/status.py

Health status models.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class HealthStatus(str, Enum):
    """Health status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheckType(str, Enum):
    """Types of health checks."""
    LIVENESS = "liveness"
    READINESS = "readiness"
    STARTUP = "startup"
    SHUTDOWN = "shutdown"


@dataclass(frozen=True)
class HealthCheckResult:
    """
    Result of a single health check.
    """
    name: str
    status: HealthStatus
    check_type: HealthCheckType
    message: str | None = None
    details: dict = field(default_factory=dict)
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    @classmethod
    def healthy(
        cls,
        name: str,
        check_type: HealthCheckType,
        message: str | None = None,
        details: dict | None = None,
    ) -> "HealthCheckResult":
        """Create a healthy result."""
        return cls(
            name=name,
            status=HealthStatus.HEALTHY,
            check_type=check_type,
            message=message,
            details=details or {},
        )
    
    @classmethod
    def degraded(
        cls,
        name: str,
        check_type: HealthCheckType,
        message: str | None = None,
        details: dict | None = None,
    ) -> "HealthCheckResult":
        """Create a degraded result."""
        return cls(
            name=name,
            status=HealthStatus.DEGRADED,
            check_type=check_type,
            message=message,
            details=details or {},
        )
    
    @classmethod
    def unhealthy(
        cls,
        name: str,
        check_type: HealthCheckType,
        message: str | None = None,
        details: dict | None = None,
    ) -> "HealthCheckResult":
        """Create an unhealthy result."""
        return cls(
            name=name,
            status=HealthStatus.UNHEALTHY,
            check_type=check_type,
            message=message,
            details=details or {},
        )


@dataclass(frozen=True)
class OverallHealthStatus:
    """
    Overall health status of the kernel.
    """
    status: HealthStatus
    checks: tuple[HealthCheckResult, ...]
    message: str | None = None
    
    @property
    def is_healthy(self) -> bool:
        """Returns True if overall status is healthy."""
        return self.status == HealthStatus.HEALTHY
    
    @property
    def is_degraded(self) -> bool:
        """Returns True if overall status is degraded."""
        return self.status == HealthStatus.DEGRADED
    
    @property
    def is_unhealthy(self) -> bool:
        """Returns True if overall status is unhealthy."""
        return self.status == HealthStatus.UNHEALTHY
    
    def by_type(self, check_type: HealthCheckType) -> tuple[HealthCheckResult, ...]:
        """Get check results filtered by type."""
        return tuple(c for c in self.checks if c.check_type == check_type)


__all__ = [
    "HealthCheckResult",
    "HealthCheckType",
    "HealthStatus",
    "OverallHealthStatus",
]
