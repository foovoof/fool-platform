"""
platform/kernel/config/override.py

Configuration override management.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class OverrideRule:
    """A single override rule."""
    key: str
    value: Any
    condition: Callable[[dict], bool] | None = None


class ConfigOverrideManager:
    """
    Manages layered configuration overrides.
    
    Supports:
    - Conditional overrides
    - Priority-based resolution
    - Override stack for undo functionality
    """
    
    def __init__(self) -> None:
        self._overrides: list[OverrideRule] = []
        self._applied: list[tuple[int, OverrideRule]] = []
        self._next_priority = 0
    
    def add_override(
        self,
        key: str,
        value: Any,
        condition: Callable[[dict], bool] | None = None,
    ) -> int:
        """
        Add an override rule.
        
        Args:
            key: Configuration key to override
            value: Value to use
            condition: Optional condition for when override applies
            
        Returns:
            Priority of the override
        """
        priority = self._next_priority
        self._next_priority += 1
        
        rule = OverrideRule(key=key, value=value, condition=condition)
        self._overrides.append(rule)
        
        return priority
    
    def remove_override(self, priority: int) -> bool:
        """
        Remove an override by priority.
        
        Args:
            priority: Priority of the override to remove
            
        Returns:
            True if override was found and removed
        """
        for i, (p, rule) in enumerate(self._applied):
            if p == priority:
                del self._applied[i]
                # Also remove from overrides list
                self._overrides = [
                    r for r in self._overrides
                    if not (r.key == rule.key and r.value == rule.value)
                ]
                return True
        return False
    
    def apply_overrides(self, config: dict) -> dict:
        """
        Apply all applicable overrides to configuration.
        
        Args:
            config: Base configuration dictionary
            
        Returns:
            Configuration with overrides applied
        """
        result = config.copy()
        
        for rule in self._overrides:
            # Check condition if present
            if rule.condition is not None:
                if not rule.condition(result):
                    continue
            
            # Apply override using dot notation
            self._set_nested(result, rule.key, rule.value)
        
        return result
    
    def _set_nested(self, config: dict, key: str, value: Any) -> None:
        """Set a nested configuration value using dot notation."""
        keys = key.split(".")
        current = config
        
        for i, k in enumerate(keys[:-1]):
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def get_overrides(self) -> list[OverrideRule]:
        """Get all registered override rules."""
        return self._overrides.copy()
    
    def clear_overrides(self) -> None:
        """Clear all override rules."""
        self._overrides.clear()
        self._applied.clear()
    
    def create_scoped_override(
        self,
        key: str,
        value: Any,
    ) -> "ScopedOverride":
        """
        Create a scoped override that can be applied and removed.
        
        Args:
            key: Configuration key to override
            value: Value to use
            
        Returns:
            ScopedOverride context manager
        """
        return ScopedOverride(self, key, value)


class ScopedOverride:
    """
    Context manager for scoped configuration overrides.
    
    Applies override on entry and removes on exit.
    """
    
    def __init__(
        self,
        manager: ConfigOverrideManager,
        key: str,
        value: Any,
    ) -> None:
        self._manager = manager
        self._key = key
        self._value = value
        self._priority: int | None = None
    
    def __enter__(self) -> "ScopedOverride":
        self._priority = self._manager.add_override(self._key, self._value)
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._priority is not None:
            self._manager.remove_override(self._priority)


__all__ = [
    "ConfigOverrideManager",
    "OverrideRule",
    "ScopedOverride",
]
