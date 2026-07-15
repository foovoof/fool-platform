"""
platform/kernel/kernel_config.py

Kernel configuration model.
"""
from dataclasses import dataclass, field
from enum import Enum

from .kernel_state import KernelState


class Environment(str, Enum):
    """Kernel environment profiles."""
    LOCAL = "local"
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass(frozen=True)
class KernelConfig:
    """
    Immutable kernel configuration.
    
    Contains all configuration needed to bootstrap and run the kernel.
    """
    environment: Environment
    version: str
    kernel_id: str | None = None
    startup_timeout_seconds: float = 30.0
    shutdown_timeout_seconds: float = 30.0
    enable_health_checks: bool = True
    enable_event_bus: bool = True
    service_discovery_enabled: bool = True
    registry_paths: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    
    @classmethod
    def for_local(cls) -> "KernelConfig":
        """Create a configuration for local development."""
        return cls(
            environment=Environment.LOCAL,
            version="1.0.0",
            startup_timeout_seconds=60.0,
            shutdown_timeout_seconds=60.0,
            enable_health_checks=True,
            enable_event_bus=True,
            registry_paths={
                "agents": "fool_platform/agents/registry/agents.yaml",
                "capabilities": "fool_platform/agents/registry/capabilities.yaml",
                "workflows": "workflows/",
                "contracts": "contracts/",
                "concepts": "standards/concepts/",
            },
        )
    
    @classmethod
    def for_development(cls) -> "KernelConfig":
        """Create a configuration for development."""
        return cls(
            environment=Environment.DEVELOPMENT,
            version="1.0.0",
            startup_timeout_seconds=30.0,
            shutdown_timeout_seconds=30.0,
            enable_health_checks=True,
            enable_event_bus=True,
            registry_paths={
                "agents": "fool_platform/agents/registry/agents.yaml",
                "capabilities": "fool_platform/agents/registry/capabilities.yaml",
                "workflows": "workflows/",
                "contracts": "contracts/",
                "concepts": "standards/concepts/",
            },
        )
    
    @classmethod
    def for_testing(cls) -> "KernelConfig":
        """Create a configuration for testing."""
        return cls(
            environment=Environment.TESTING,
            version="1.0.0",
            startup_timeout_seconds=10.0,
            shutdown_timeout_seconds=10.0,
            enable_health_checks=True,
            enable_event_bus=True,
            registry_paths={},
        )
    
    @classmethod
    def for_production(cls) -> "KernelConfig":
        """Create a configuration for production."""
        return cls(
            environment=Environment.PRODUCTION,
            version="1.0.0",
            startup_timeout_seconds=60.0,
            shutdown_timeout_seconds=60.0,
            enable_health_checks=True,
            enable_event_bus=True,
            service_discovery_enabled=True,
            registry_paths={
                "agents": "fool_platform/agents/registry/agents.yaml",
                "capabilities": "fool_platform/agents/registry/capabilities.yaml",
                "workflows": "workflows/",
                "contracts": "contracts/",
                "concepts": "standards/concepts/",
            },
        )
    
    def is_production(self) -> bool:
        """Returns True if running in production."""
        return self.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Returns True if running in development."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_testing(self) -> bool:
        """Returns True if running in testing."""
        return self.environment == Environment.TESTING


__all__ = [
    "Environment",
    "KernelConfig",
]
