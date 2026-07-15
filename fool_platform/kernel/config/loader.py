"""
platform/kernel/config/loader.py

Configuration loading from various sources.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .environment import EnvironmentProfile


@dataclass
class ConfigSource:
    """
    Represents a configuration source with priority.
    """
    name: str
    data: dict
    priority: int = 0


@dataclass
class ConfigLoadResult:
    """
    Result of configuration loading operation.
    """
    sources: list[ConfigSource]
    merged: dict
    errors: list[str] = field(default_factory=list)


class ConfigLoader:
    """
    Loads configuration from multiple sources with layered override.
    
    Priority (highest wins):
    1. Environment variables
    2. Runtime overrides
    3. Environment-specific file
    4. Base configuration file
    5. Default values
    """
    
    def __init__(self, profile: EnvironmentProfile | None = None) -> None:
        self._profile = profile or EnvironmentDetector.detect_from_env()
        self._sources: list[ConfigSource] = []
        self._runtime_overrides: dict = {}
    
    @property
    def profile(self) -> EnvironmentProfile:
        """Current environment profile."""
        return self._profile
    
    def add_source(self, source: ConfigSource) -> None:
        """Add a configuration source."""
        self._sources.append(source)
    
    def add_dict(self, name: str, data: dict, priority: int = 0) -> None:
        """Add a dictionary as a configuration source."""
        self.add_source(ConfigSource(name=name, data=data, priority=priority))
    
    def set_overrides(self, overrides: dict) -> None:
        """Set runtime overrides (highest priority)."""
        self._runtime_overrides = overrides
    
    def add_override(self, key: str, value: Any) -> None:
        """Add a single runtime override."""
        self._runtime_overrides[key] = value
    
    def load(self) -> ConfigLoadResult:
        """
        Load and merge all configuration sources.
        
        Returns:
            ConfigLoadResult with merged configuration
        """
        errors: list[str] = []
        
        # Start with empty config
        merged: dict = {}
        sources: list[ConfigSource] = []
        
        # Load from sources in priority order
        sorted_sources = sorted(self._sources, key=lambda s: s.priority)
        for source in sorted_sources:
            try:
                merged = self._deep_merge(merged, source.data)
                sources.append(source)
            except Exception as e:
                errors.append(f"Error loading {source.name}: {e}")
        
        # Load from environment variables
        env_config = self._load_from_environment()
        if env_config:
            sources.append(ConfigSource(name="environment", data=env_config, priority=100))
            merged = self._deep_merge(merged, env_config)
        
        # Apply runtime overrides
        if self._runtime_overrides:
            sources.append(
                ConfigSource(name="runtime", data=self._runtime_overrides, priority=1000)
            )
            merged = self._deep_merge(merged, self._runtime_overrides)
        
        return ConfigLoadResult(
            sources=sources,
            merged=merged,
            errors=errors,
        )
    
    def _load_from_environment(self) -> dict:
        """Load configuration from environment variables."""
        config = {}
        
        # Look for FOOL_ prefixed variables
        for key, value in os.environ.items():
            if key.startswith("FOOL_"):
                config_key = key[5:].lower().replace("_", ".")
                config[config_key] = self._parse_value(value)
        
        return config
    
    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse a string value to appropriate type."""
        # Boolean
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
        
        # Number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # JSON-like arrays
        if value.startswith("[") and value.endswith("]"):
            try:
                import json
                return json.loads(value)
            except Exception:
                pass
        
        # Return as string
        return value
    
    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = ConfigLoader._deep_merge(result[key], value)
            else:
                result[key] = value
        return result


__all__ = [
    "ConfigLoadResult",
    "ConfigLoader",
    "ConfigSource",
]
