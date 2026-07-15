"""
platform/kernel/config/typed_config.py

Typed configuration objects.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic

from .environment import EnvironmentProfile

T = TypeVar("T")


@dataclass(frozen=True)
class TypedConfig(Generic[T]):
    """
    Base class for typed configuration objects.
    
    Provides type-safe access to configuration values.
    """
    
    raw: dict
    profile: EnvironmentProfile = EnvironmentProfile.LOCAL
    
    def get(self, key: str, default: T | None = None) -> T | None:
        """
        Get a configuration value by key.
        
        Args:
            key: Dot-separated path to configuration value
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value: Any = self.raw
        
        for k in keys:
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        
        return value
    
    def get_required(self, key: str) -> T:
        """
        Get a required configuration value.
        
        Args:
            key: Dot-separated path to configuration value
            
        Returns:
            Configuration value
            
        Raises:
            KeyError: If key not found
        """
        value = self.get(key)
        if value is None:
            raise KeyError(f"Required configuration key not found: {key}")
        return value
    
    def get_typed(self, key: str, expected_type: type[T]) -> T:
        """
        Get a configuration value with type checking.
        
        Args:
            key: Dot-separated path to configuration value
            expected_type: Expected type of the value
            
        Returns:
            Configuration value
            
        Raises:
            TypeError: If value is not of expected type
        """
        value = self.get(key)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(
                f"Configuration value for {key} has type {type(value).__name__}, "
                f"expected {expected_type.__name__}"
            )
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access."""
        return self.get(key)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return self.get(key) is not None


@dataclass(frozen=True)
class KernelTypedConfig(TypedConfig):
    """
    Typed configuration for kernel settings.
    """
    raw: dict = field(default_factory=dict)
    
    @property
    def environment(self) -> EnvironmentProfile:
        """Environment profile."""
        return self.get_typed("kernel.environment", str)
    
    @property
    def version(self) -> str:
        """Kernel version."""
        return self.get("kernel.version", "1.0.0")
    
    @property
    def startup_timeout(self) -> float:
        """Startup timeout in seconds."""
        return self.get("kernel.startup_timeout", 30.0)
    
    @property
    def shutdown_timeout(self) -> float:
        """Shutdown timeout in seconds."""
        return self.get("kernel.shutdown_timeout", 30.0)


@dataclass(frozen=True)
class RegistryTypedConfig(TypedConfig):
    """
    Typed configuration for registry paths.
    """
    raw: dict = field(default_factory=dict)
    
    @property
    def agents_path(self) -> str | None:
        """Path to agents registry."""
        return self.get("registry.agents")
    
    @property
    def capabilities_path(self) -> str | None:
        """Path to capabilities registry."""
        return self.get("registry.capabilities")
    
    @property
    def workflows_path(self) -> str | None:
        """Path to workflows directory."""
        return self.get("registry.workflows")
    
    @property
    def contracts_path(self) -> str | None:
        """Path to contracts directory."""
        return self.get("registry.contracts")
    
    @property
    def concepts_path(self) -> str | None:
        """Path to concepts directory."""
        return self.get("registry.concepts")


def create_typed_config(
    config: dict,
    profile: EnvironmentProfile | None = None,
) -> TypedConfig:
    """
    Factory function to create a typed configuration.
    
    Args:
        config: Raw configuration dictionary
        profile: Environment profile
        
    Returns:
        TypedConfig instance
    """
    return TypedConfig(
        raw=config,
        profile=profile or EnvironmentProfile.LOCAL,
    )


__all__ = [
    "KernelTypedConfig",
    "RegistryTypedConfig",
    "TypedConfig",
    "create_typed_config",
]
