"""
platform/kernel/health/readiness.py

Readiness checks for the kernel.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from .checks import LambdaHealthCheck
from .status import HealthCheckResult, HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck


class ReadinessCheck(LambdaHealthCheck):
    """
    Liveness check to verify kernel is ready to receive traffic.
    
    Readiness checks verify that the kernel has completed startup
    and is ready to handle requests.
    """
    
    def __init__(
        self,
        name: str,
        check_fn: Callable[..., bool],
    ) -> None:
        super().__init__(name, check_fn, HealthCheckType.READINESS)


class KernelReadinessCheck(HealthCheck):
    """
    Built-in readiness check for kernel state.
    """
    
    def __init__(self, kernel_state_check: Optional[Callable[..., bool]] = None) -> None:
        self._kernel_state_check = kernel_state_check
        self._ready = False
    
    @property
    def name(self) -> str:
        return "kernel.readiness"
    
    def check(self) -> bool:
        if self._kernel_state_check:
            return self._kernel_state_check()
        return self._ready
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.READINESS.value,
            "ready": self._ready,
        }
    
    def set_ready(self, ready: bool) -> None:
        """Set the ready state."""
        self._ready = ready


class RegistryReadinessCheck(HealthCheck):
    """
    Readiness check for registry availability.
    """
    
    def __init__(self, registry_check: Optional[Callable[..., bool]] = None) -> None:
        self._registry_check = registry_check
    
    @property
    def name(self) -> str:
        return "registry.readiness"
    
    def check(self) -> bool:
        if self._registry_check:
            return self._registry_check()
        return True
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.READINESS.value,
        }


__all__ = [
    "KernelReadinessCheck",
    "ReadinessCheck",
    "RegistryReadinessCheck",
]
