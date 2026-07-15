"""
fool_platform/events/router.py

Event routing logic for matching events to subscribers.
"""
import fnmatch
from dataclasses import dataclass, field
from threading import Lock
from typing import TYPE_CHECKING

from fool_platform.events.exceptions import EventRoutingError

if TYPE_CHECKING:
    from fool_platform.events.subscriber import EventSubscriber


@dataclass
class RoutingRule:
    """A routing rule for matching event types to subscribers."""
    pattern: str
    subscriber: "EventSubscriber"
    priority: int = 0

    def matches(self, event_type: str) -> bool:
        """
        Check if this rule matches the given event type.
        
        Supports exact matching and wildcard patterns:
        - "case.created" - exact match only
        - "case.*" - matches "case.created", "case.updated", etc.
        - "agent.*" - matches "agent.started", "agent.stopped", etc.
        
        Args:
            event_type: The event type to match
            
        Returns:
            True if the pattern matches, False otherwise
        """
        if self.pattern == "*":
            return True
        if self.pattern == event_type:
            return True
        if "*" in self.pattern:
            return fnmatch.fnmatch(event_type, self.pattern)
        return False


@dataclass
class EventRouter:
    """
    Routes events to matching subscribers based on event type patterns.
    
    Thread-safe for concurrent subscriber registration and routing.
    """
    _rules: list[RoutingRule] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock)

    def register(
        self,
        subscriber: "EventSubscriber",
        pattern: str | None = None,
        priority: int = 0,
    ) -> None:
        """
        Register a subscriber for a specific event type pattern.
        
        Args:
            subscriber: The subscriber to register
            pattern: The event type pattern (defaults to subscriber's first supported type)
            priority: Routing priority (higher priority subscribers are checked first)
        """
        with self._lock:
            if pattern is None:
                if subscriber.supported_event_types:
                    pattern = subscriber.supported_event_types[0]
                else:
                    raise EventRoutingError(
                        "Cannot register subscriber without a pattern: "
                        "no supported_event_types defined",
                        event_type=None,
                    )
            
            rule = RoutingRule(
                pattern=pattern,
                subscriber=subscriber,
                priority=priority,
            )
            self._rules.append(rule)
            self._rules.sort(key=lambda r: -r.priority)

    def unregister(self, subscriber_id: str) -> bool:
        """
        Unregister a subscriber by ID.
        
        Args:
            subscriber_id: The subscriber ID to unregister
            
        Returns:
            True if the subscriber was found and removed, False otherwise
        """
        with self._lock:
            initial_count = len(self._rules)
            self._rules = [r for r in self._rules if r.subscriber.subscriber_id != subscriber_id]
            return len(self._rules) < initial_count

    def unregister_all(self) -> int:
        """
        Unregister all subscribers.
        
        Returns:
            The number of subscribers unregistered
        """
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            return count

    def route(self, event_type: str) -> list["EventSubscriber"]:
        """
        Route an event type to all matching subscribers.
        
        Args:
            event_type: The event type to route
            
        Returns:
            A list of matching subscribers in priority order
        """
        with self._lock:
            matching = [rule.subscriber for rule in self._rules if rule.matches(event_type)]
            return matching

    def get_subscriber_count(self) -> int:
        """Get the total number of registered subscriber rules."""
        with self._lock:
            return len(self._rules)

    def get_unique_subscriber_count(self) -> int:
        """Get the number of unique subscribers."""
        with self._lock:
            subscriber_ids = {r.subscriber.subscriber_id for r in self._rules}
            return len(subscriber_ids)

    def has_subscribers(self) -> bool:
        """Check if any subscribers are registered."""
        with self._lock:
            return len(self._rules) > 0

    def get_patterns_for_subscriber(self, subscriber_id: str) -> list[str]:
        """
        Get all patterns registered for a specific subscriber.
        
        Args:
            subscriber_id: The subscriber ID to look up
            
        Returns:
            List of patterns registered for the subscriber
        """
        with self._lock:
            return [
                rule.pattern 
                for rule in self._rules 
                if rule.subscriber.subscriber_id == subscriber_id
            ]
