"""
platform/kernel/config/registry.py

Configuration registry for managing configuration values.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConfigEntry:
    """A single configuration entry."""
    key: str
    value: Any
    source: str
    readonly: bool = False


class ConfigRegistry:
    """
    Registry for managing configuration entries.
    
    Provides centralized access to all configuration values
    with support for source tracking and readonly enforcement.
    """
    
    def __init__(self) -> None:
        self._entries: dict[str, ConfigEntry] = {}
        self._listeners: list[callable] = []
    
    def register(
        self,
        key: str,
        value: Any,
        source: str = "unknown",
        readonly: bool = False,
    ) -> None:
        """
        Register a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            source: Source of the configuration
            readonly: Whether the value can be modified
        """
        self._entries[key] = ConfigEntry(
            key=key,
            value=value,
            source=source,
            readonly=readonly,
        )
        self._notify_listeners(key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        entry = self._entries.get(key)
        if entry is None:
            return default
        return entry.value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: New value
            
        Raises:
            ValueError: If key is readonly
        """
        entry = self._entries.get(key)
        if entry and entry.readonly:
            raise ValueError(f"Configuration key is readonly: {key}")
        
        if entry:
            self._entries[key] = ConfigEntry(
                key=key,
                value=value,
                source=entry.source,
                readonly=entry.readonly,
            )
        else:
            self._entries[key] = ConfigEntry(
                key=key,
                value=value,
                source="runtime",
                readonly=False,
            )
        
        self._notify_listeners(key, value)
    
    def get_source(self, key: str) -> str | None:
        """Get the source of a configuration value."""
        entry = self._entries.get(key)
        return entry.source if entry else None
    
    def is_readonly(self, key: str) -> bool:
        """Check if a key is readonly."""
        entry = self._entries.get(key)
        return entry.readonly if entry else False
    
    def keys(self) -> list[str]:
        """Get all configuration keys."""
        return list(self._entries.keys())
    
    def items(self) -> list[tuple[str, Any]]:
        """Get all configuration items."""
        return [(k, e.value) for k, e in self._entries.items()]
    
    def add_listener(self, listener: callable) -> None:
        """Add a configuration change listener."""
        self._listeners.append(listener)
    
    def remove_listener(self, listener: callable) -> None:
        """Remove a configuration change listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_listeners(self, key: str, value: Any) -> None:
        """Notify all listeners of a configuration change."""
        for listener in self._listeners:
            try:
                listener(key, value)
            except Exception:
                pass  # Log but don't fail on listener errors
    
    def clear(self) -> None:
        """Clear all non-readonly entries."""
        self._entries = {
            k: e for k, e in self._entries.items() if e.readonly
        }


__all__ = [
    "ConfigEntry",
    "ConfigRegistry",
]
