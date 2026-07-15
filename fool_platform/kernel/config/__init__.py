"""
platform/kernel/config/__init__.py

Configuration management for the FOOL Platform kernel.
"""
from .environment import EnvironmentDetector, EnvironmentProfile
from .loader import ConfigLoadResult, ConfigLoader, ConfigSource
from .override import ConfigOverrideManager, ScopedOverride
from .registry import ConfigEntry, ConfigRegistry
from .secrets import SecretConfig, SecretProvider, SecretRef, SecretResolver
from .typed_config import (
    KernelTypedConfig,
    RegistryTypedConfig,
    TypedConfig,
    create_typed_config,
)
from .validator import (
    ConfigValidator,
    PatternRule,
    RangeRule,
    RequiredRule,
    TypeRule,
    ValidationError,
    ValidationResult,
    ValidationRule,
)

__all__ = [
    "ConfigLoadResult",
    "ConfigLoader",
    "ConfigOverrideManager",
    "ConfigRegistry",
    "ConfigSource",
    "ConfigValidator",
    "EnvironmentDetector",
    "EnvironmentProfile",
    "KernelTypedConfig",
    "PatternRule",
    "RangeRule",
    "RegistryTypedConfig",
    "RequiredRule",
    "ScopedOverride",
    "SecretConfig",
    "SecretProvider",
    "SecretRef",
    "SecretResolver",
    "TypedConfig",
    "TypeRule",
    "ValidationError",
    "ValidationResult",
    "ValidationRule",
    "create_typed_config",
]
