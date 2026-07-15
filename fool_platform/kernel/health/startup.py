"""
platform/kernel/health/startup.py

Startup validation checks.
"""
from typing import Any

from .checks import LambdaHealthCheck
from .status import HealthCheckResult, HealthCheckType, HealthStatus
from ..kernel_interfaces import HealthCheck


class StartupCheck(LambdaHealthCheck):
    """
    Startup check to verify initialization completed.
    
    Startup checks are run during kernel initialization to ensure
    all required components are properly set up.
    """
    
    def __init__(
        self,
        name: str,
        check_fn: callable,
    ) -> None:
        super().__init__(name, check_fn, HealthCheckType.STARTUP)


class BootstrapCompleteCheck(HealthCheck):
    """
    Check that kernel bootstrap completed successfully.
    """
    
    def __init__(self) -> None:
        self._completed = False
        self._errors: list[str] = []
    
    @property
    def name(self) -> str:
        return "bootstrap.completed"
    
    def check(self) -> bool:
        return self._completed and len(self._errors) == 0
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.STARTUP.value,
            "completed": self._completed,
            "errors": self._errors,
        }
    
    def set_completed(self, completed: bool, errors: list[str] | None = None) -> None:
        """Mark bootstrap as completed with optional errors."""
        self._completed = completed
        if errors:
            self._errors = errors


class ConfigValidCheck(HealthCheck):
    """
    Check that configuration is valid.
    """
    
    def __init__(self, config_valid: bool = True) -> None:
        self._config_valid = config_valid
    
    @property
    def name(self) -> str:
        return "config.valid"
    
    def check(self) -> bool:
        return self._config_valid
    
    def details(self) -> dict[str, Any]:
        return {
            "check_type": HealthCheckType.STARTUP.value,
            "valid": self._config_valid,
        }


__all__ = [
    "BootstrapCompleteCheck",
    "ConfigValidCheck",
    "StartupCheck",
]
