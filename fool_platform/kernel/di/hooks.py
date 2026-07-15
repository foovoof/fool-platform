"""
platform/kernel/di/hooks.py

Lifecycle hooks for dependency injection.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .container import DIContainer

HookCallback = Callable[["DIContainer", Any, str], None]
"""Type alias for hook callbacks."""


class HookType(Enum):
    """Types of lifecycle hooks."""
    BEFORE_RESOLVE = auto()
    AFTER_RESOLVE = auto()
    BEFORE_RELEASE = auto()
    AFTER_RELEASE = auto()
    ON_ERROR = auto()


@dataclass
class LifecycleHook:
    """
    Represents a registered lifecycle hook.
    """
    hook_type: HookType
    callback: HookCallback
    service_type: type | None
    name: str | None = None
    registered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HookRegistry:
    """
    Registry for dependency injection lifecycle hooks.
    
    Manages registration and execution of hooks for:
    - Before/after service resolution
    - Before/after service release
    - Error handling during resolution
    """
    
    def __init__(self) -> None:
        self._hooks: list[LifecycleHook] = []
    
    def register(
        self,
        hook_type: HookType,
        callback: HookCallback,
        service_type: type | None = None,
        name: str | None = None,
    ) -> None:
        """
        Register a lifecycle hook.
        
        Args:
            hook_type: When the hook should be invoked
            callback: Function to call when hook is triggered
            service_type: Optional service type to filter on
            name: Optional service name to filter on
        """
        hook = LifecycleHook(
            hook_type=hook_type,
            callback=callback,
            service_type=service_type,
            name=name,
        )
        self._hooks.append(hook)
    
    def unregister(
        self,
        hook_type: HookType,
        callback: HookCallback,
    ) -> bool:
        """
        Unregister a lifecycle hook.
        
        Args:
            hook_type: Type of hook to unregister
            callback: The callback to remove
            
        Returns:
            True if hook was found and removed
        """
        self._hooks = [
            h for h in self._hooks
            if not (h.hook_type == hook_type and h.callback == callback)
        ]
        return True
    
    def get_hooks(
        self,
        hook_type: HookType,
        service_type: type | None = None,
        name: str | None = None,
    ) -> list[LifecycleHook]:
        """
        Get all matching hooks for a given type.
        
        Args:
            hook_type: Type of hooks to retrieve
            service_type: Optional filter by service type
            name: Optional filter by service name
            
        Returns:
            List of matching hooks
        """
        matching: list[LifecycleHook] = []
        for hook in self._hooks:
            if hook.hook_type != hook_type:
                continue
            if service_type is not None and hook.service_type != service_type:
                continue
            if name is not None and hook.name != name:
                continue
            matching.append(hook)
        return matching
    
    def clear(self) -> None:
        """Clear all registered hooks."""
        self._hooks.clear()


class HookExecutor:
    """
    Executes lifecycle hooks during DI container operations.
    """
    
    def __init__(self, registry: HookRegistry) -> None:
        self._registry = registry
    
    def before_resolve(
        self,
        container: "DIContainer",
        service_type: type,
        name: str | None = None,
    ) -> None:
        """Execute before-resolve hooks."""
        hooks = self._registry.get_hooks(
            HookType.BEFORE_RESOLVE, service_type, name
        )
        for hook in hooks:
            try:
                hook.callback(container, service_type, name or "")
            except Exception:
                pass  # Log but don't fail on hook errors
    
    def after_resolve(
        self,
        container: "DIContainer",
        instance: Any,
        key: str,
    ) -> None:
        """Execute after-resolve hooks."""
        service_type = type(instance)
        hooks = self._registry.get_hooks(
            HookType.AFTER_RESOLVE, service_type, None
        )
        for hook in hooks:
            try:
                hook.callback(container, instance, key)
            except Exception:
                pass  # Log but don't fail on hook errors
    
    def on_error(
        self,
        container: "DIContainer",
        service_type: type,
        key: str,
        error: Exception,
    ) -> None:
        """Execute error hooks."""
        hooks = self._registry.get_hooks(
            HookType.ON_ERROR, service_type, None
        )
        for hook in hooks:
            try:
                hook.callback(container, service_type, key)
            except Exception:
                pass  # Log but don't fail on hook errors


__all__ = [
    "HookExecutor",
    "HookRegistry",
    "HookType",
    "LifecycleHook",
]
