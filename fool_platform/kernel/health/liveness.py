"""
platform/kernel/health/liveness.py

Liveness checks for the kernel.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from .checks import LambdaHealthCheck
from .status import HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck


class LivenessCheck(LambdaHealthCheck):
    """
    Liveness check to verify kernel is alive.
    
    Liveness checks are lightweight probes that verify the kernel
    process is running and responsive.
    """
    
    def __init__(
        self,
        name: str,
        check_fn: Callable[..., bool],
    ) -> None:
        super().__init__(name, check_fn, HealthCheckType.LIVENESS)


class KernelLivenessCheck(HealthCheck):
    """
    Built-in liveness check for kernel state.
    """
    
    def __init__(self, kernel_state_check: Optional[Callable[..., bool]] = None) -> None:
        self._kernel_state_check = kernel_state_check
    
    @property
    def name(self) -> str:
        return "kernel.liveness"
    
    def check(self) -> bool:
        if self._kernel_state_check:
            return self._kernel_state_check()
        return True
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.LIVENESS.value,
            "alive": True,
        }


class DIContainerLivenessCheck(HealthCheck):
    """
    Liveness check for DI container.
    """
    
    def __init__(self, container_check: Optional[Callable[..., bool]] = None) -> None:
        self._container_check = container_check
    
    @property
    def name(self) -> str:
        return "di.container.liveness"
    
    def check(self) -> bool:
        if self._container_check:
            return self._container_check()
        return True
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.LIVENESS.value,
            "container_healthy": True,
        }


__all__ = [
    "DIContainerLivenessCheck",
    "KernelLivenessCheck",
    "LivenessCheck",
]
