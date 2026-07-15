"""
platform/kernel/health_manager.py

Health management for the kernel.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .kernel_events import KernelEventType
from .kernel_interfaces import HealthCheck

if TYPE_CHECKING:
    from .runtime import Kernel

logger = logging.getLogger(__name__)


class HealthManager:
    """
    Manages health checks for the kernel and its components.
    
    Coordinates health check registration, execution, and reporting.
    """
    
    def __init__(self) -> None:
        self._initialized = False
        self._disposed = False
        self._checks: dict[str, HealthCheck] = {}
    
    def initialize(self) -> None:
        """Initialize the health manager."""
        if self._initialized:
            logger.warning("HealthManager already initialized")
            return
        
        logger.debug("HealthManager initializing")
        
        # Register built-in health checks
        self._register_builtin_checks()
        
        self._initialized = True
        logger.info("HealthManager initialized")
    
    def dispose(self) -> None:
        """Dispose the health manager."""
        if self._disposed:
            return
        
        self._checks.clear()
        self._disposed = True
        logger.info("HealthManager disposed")
    
    def register_check(self, check: HealthCheck) -> None:
        """
        Register a health check.
        
        Args:
            check: HealthCheck implementation to register
        """
        if check.name in self._checks:
            logger.warning(f"Overwriting existing health check: {check.name}")
        self._checks[check.name] = check
        logger.debug(f"Registered health check: {check.name}")
    
    def unregister_check(self, name: str) -> bool:
        """
        Unregister a health check.
        
        Args:
            name: Name of the health check to remove
            
        Returns:
            True if check was found and removed, False otherwise
        """
        if name in self._checks:
            del self._checks[name]
            logger.debug(f"Unregistered health check: {name}")
            return True
        return False
    
    def run_all_checks(self) -> dict[str, Any]:
        """
        Run all registered health checks.
        
        Returns:
            Dictionary mapping check names to their results
        """
        results = {}
        for name, check in self._checks.items():
            try:
                results[name] = {
                    "healthy": check.check(),
                    "details": check.details(),
                }
            except Exception as e:
                results[name] = {
                    "healthy": False,
                    "error": str(e),
                }
        return results
    
    def get_liveness_status(self) -> dict[str, Any]:
        """
        Get overall liveness status.
        
        Returns:
            Liveness status with results of liveness checks
        """
        checks = {name: check for name, check in self._checks.items()}
        liveness_checks = {k: v for k, v in checks.items() if "liveness" in k}
        
        if not liveness_checks:
            return {"alive": True, "checks": {}}
        
        results = {}
        all_healthy = True
        for name, check in liveness_checks.items():
            try:
                healthy = check.check()
                results[name] = {"healthy": healthy}
                if not healthy:
                    all_healthy = False
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                all_healthy = False
        
        return {"alive": all_healthy, "checks": results}
    
    def get_readiness_status(self) -> dict[str, Any]:
        """
        Get overall readiness status.
        
        Returns:
            Readiness status with results of readiness checks
        """
        checks = {name: check for name, check in self._checks.items()}
        readiness_checks = {k: v for k, v in checks.items() if "readiness" in k}
        
        if not readiness_checks:
            return {"ready": True, "checks": {}}
        
        results = {}
        all_ready = True
        for name, check in readiness_checks.items():
            try:
                healthy = check.check()
                results[name] = {"healthy": healthy}
                if not healthy:
                    all_ready = False
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                all_ready = False
        
        return {"ready": all_ready, "checks": results}
    
    def _register_builtin_checks(self) -> None:
        """Register built-in health checks."""
        # KernelStateCheck would be registered here
        # Implementation omitted for simplicity
        pass


__all__ = [
    "HealthManager",
]
