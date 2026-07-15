"""
platform/kernel/health/shutdown.py

Shutdown validation checks.
"""
from typing import Any

from .checks import LambdaHealthCheck
from .status import HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck


class ShutdownCheck(LambdaHealthCheck):
    """
    Shutdown check to verify cleanup completed.
    
    Shutdown checks are run during kernel shutdown to ensure
    all resources are properly released.
    """
    
    def __init__(
        self,
        name: str,
        check_fn: callable,
    ) -> None:
        super().__init__(name, check_fn, HealthCheckType.SHUTDOWN)


class ServicesDisposedCheck(HealthCheck):
    """
    Check that all services were disposed properly.
    """
    
    def __init__(self) -> None:
        self._disposed = False
        self._pending_disposals: list[str] = []
    
    @property
    def name(self) -> str:
        return "services.disposed"
    
    def check(self) -> bool:
        return self._disposed and len(self._pending_disposals) == 0
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.SHUTDOWN.value,
            "disposed": self._disposed,
            "pending_disposals": self._pending_disposals,
        }
    
    def set_disposed(
        self,
        disposed: bool,
        pending: list[str] | None = None,
    ) -> None:
        """Mark disposal status."""
        self._disposed = disposed
        if pending:
            self._pending_disposals = pending


class ResourcesReleasedCheck(HealthCheck):
    """
    Check that all resources were released.
    """
    
    def __init__(self) -> None:
        self._released = False
        self._held_resources: list[str] = []
    
    @property
    def name(self) -> str:
        return "resources.released"
    
    def check(self) -> bool:
        return self._released and len(self._held_resources) == 0
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.SHUTDOWN.value,
            "released": self._released,
            "held_resources": self._held_resources,
        }


__all__ = [
    "ResourcesReleasedCheck",
    "ServicesDisposedCheck",
    "ShutdownCheck",
]
