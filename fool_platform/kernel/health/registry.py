"""
platform/kernel/health/registry.py

Health check registry.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .status import HealthCheckResult, HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck

logger = logging.getLogger(__name__)


class HealthCheckRegistry:
    """
    Registry for health checks.
    
    Manages registration and execution of health checks
    across all check types (liveness, readiness, startup, shutdown).
    """
    
    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}
        self._by_type: dict[HealthCheckType, list[str]] = {
            t: [] for t in HealthCheckType
        }
    
    def register(self, check: HealthCheck) -> None:
        """
        Register a health check.
        
        Args:
            check: HealthCheck implementation
        """
        if check.name in self._checks:
            logger.warning(f"Overwriting existing health check: {check.name}")
        
        self._checks[check.name] = check
        logger.debug(f"Registered health check: {check.name}")
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a health check.
        
        Args:
            name: Name of the check to remove
            
        Returns:
            True if check was found and removed
        """
        if name in self._checks:
            check = self._checks[name]
            del self._checks[name]
            
            # Remove from type index
            for check_type_list in self._by_type.values():
                if name in check_type_list:
                    check_type_list.remove(name)
            
            logger.debug(f"Unregistered health check: {name}")
            return True
        return False
    
    def get(self, name: str) -> HealthCheck | None:
        """Get a health check by name."""
        return self._checks.get(name)
    
    def get_by_type(self, check_type: HealthCheckType) -> list[HealthCheck]:
        """Get all health checks of a specific type."""
        names = self._by_type.get(check_type, [])
        return [self._checks[n] for n in names if n in self._checks]
    
    def run_check(self, name: str) -> HealthCheckResult:
        """
        Run a specific health check.
        
        Args:
            name: Name of the check to run
            
        Returns:
            HealthCheckResult for the check
        """
        check = self._checks.get(name)
        if check is None:
            return HealthCheckResult.unhealthy(
                name=name,
                check_type=HealthCheckType.LIVENESS,
                message="Check not found",
            )
        
        try:
            healthy = check.check()
            details = check.details()
            
            if healthy:
                return HealthCheckResult.healthy(
                    name=name,
                    check_type=details.get("check_type", HealthCheckType.LIVENESS),
                    details=details,
                )
            else:
                return HealthCheckResult.unhealthy(
                    name=name,
                    check_type=details.get("check_type", HealthCheckType.LIVENESS),
                    message=details.get("message", "Check failed"),
                    details=details,
                )
        except Exception as e:
            return HealthCheckResult.unhealthy(
                name=name,
                check_type=HealthCheckType.LIVENESS,
                message=f"Check error: {e}",
                details={"error": str(e)},
            )
    
    def run_all(self) -> list[HealthCheckResult]:
        """Run all registered health checks."""
        results = []
        for name in self._checks:
            results.append(self.run_check(name))
        return results
    
    def run_by_type(self, check_type: HealthCheckType) -> list[HealthCheckResult]:
        """Run all health checks of a specific type."""
        results = []
        for name in self._by_type.get(check_type, []):
            results.append(self.run_check(name))
        return results
    
    @property
    def check_names(self) -> list[str]:
        """Get all registered check names."""
        return list(self._checks.keys())


__all__ = [
    "HealthCheckRegistry",
]
