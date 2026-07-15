"""
platform/kernel/health/checks.py

Health check implementations.
"""
from __future__ import annotations

from typing import Any

from .status import HealthCheckResult, HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck


class LambdaHealthCheck(HealthCheck):
    """
    Health check that wraps a simple callable.
    
    Useful for quick health check definitions without creating a class.
    """
    
    def __init__(
        self,
        name: str,
        check_fn: callable,
        check_type: HealthCheckType = HealthCheckType.LIVENESS,
    ) -> None:
        self._name = name
        self._check_fn = check_fn
        self._check_type = check_type
    
    @property
    def name(self) -> str:
        return self._name
    
    def check(self) -> bool:
        return self._check_fn()
    
    def details(self) -> dict[str, Any]:
        try:
            result = self._check_fn()
            return {
                "check_type": self._check_type.value,
                "result": result,
            }
        except Exception as e:
            return {
                "check_type": self._check_type.value,
                "error": str(e),
            }


class CompositeHealthCheck(HealthCheck):
    """
    Health check that combines multiple checks.
    """
    
    def __init__(
        self,
        name: str,
        checks: list[HealthCheck],
        strategy: str = "all",
    ) -> None:
        self._name = name
        self._checks = checks
        self._strategy = strategy  # "all" or "any"
    
    @property
    def name(self) -> str:
        return self._name
    
    def check(self) -> bool:
        if self._strategy == "all":
            return all(c.check() for c in self._checks)
        else:  # "any"
            return any(c.check() for c in self._checks)
    
    def details(self) -> dict[str, Any]:
        results = {}
        all_healthy = True
        for check in self._checks:
            try:
                healthy = check.check()
                results[check.name] = healthy
                if not healthy:
                    all_healthy = False
            except Exception as e:
                results[check.name] = {"error": str(e)}
                all_healthy = False
        
        return {
            "strategy": self._strategy,
            "checks": results,
            "overall": all_healthy,
        }


def create_lambda_check(
    name: str,
    check_fn: callable,
    check_type: HealthCheckType = HealthCheckType.LIVENESS,
) -> LambdaHealthCheck:
    """Factory to create a lambda health check."""
    return LambdaHealthCheck(name, check_fn, check_type)


__all__ = [
    "CompositeHealthCheck",
    "LambdaHealthCheck",
    "create_lambda_check",
]
