"""
fool_platform/events/history.py

In-memory event history for the Event Bus.
"""
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from threading import Lock
from typing import Iterator

from fool_platform.events.envelope import EventEnvelope


class EventHistory(ABC):
    """
    Abstract interface for event history storage.
    
    Implement this interface for different storage backends.
    """
    
    @abstractmethod
    def append(self, event: EventEnvelope) -> None:
        """Append an event to history."""
        pass

    @abstractmethod
    def list_events(self) -> list[EventEnvelope]:
        """List all events in history."""
        pass

    @abstractmethod
    def get_event(self, event_id: str) -> EventEnvelope | None:
        """Get an event by ID."""
        pass

    @abstractmethod
    def find_by_type(self, event_type: str) -> list[EventEnvelope]:
        """Find events by type."""
        pass

    @abstractmethod
    def find_by_correlation_id(self, correlation_id: str) -> list[EventEnvelope]:
        """Find events by correlation ID."""
        pass

    @abstractmethod
    def find_by_idempotency_key(self, idempotency_key: str) -> list[EventEnvelope]:
        """Find events by idempotency key."""
        pass

    @abstractmethod
    def has_event(self, event_id: str) -> bool:
        """Check if an event exists."""
        pass

    @abstractmethod
    def has_idempotency_key(self, idempotency_key: str) -> bool:
        """Check if an idempotency key exists."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all events from history."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Get the total number of events."""
        pass


@dataclass
class InMemoryEventHistory(EventHistory):
    """
    Thread-safe in-memory event history implementation.
    
    Preserves insertion order and provides O(1) append operations.
    """
    _events: OrderedDict[str, EventEnvelope] = field(default_factory=OrderedDict)
    _idempotency_index: dict[str, str] = field(default_factory=dict)
    _correlation_index: dict[str, list[str]] = field(default_factory=dict)
    _type_index: dict[str, list[str]] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock)

    def append(self, event: EventEnvelope) -> None:
        """
        Append an event to history.
        
        O(1) operation.
        
        Args:
            event: The event to append
        """
        with self._lock:
            self._events[event.event_id] = event
            
            if event.metadata.idempotency_key:
                self._idempotency_index[event.metadata.idempotency_key] = event.event_id
            
            if event.metadata.correlation_id:
                if event.metadata.correlation_id not in self._correlation_index:
                    self._correlation_index[event.metadata.correlation_id] = []
                self._correlation_index[event.metadata.correlation_id].append(event.event_id)
            
            event_type = event.event_type
            if event_type not in self._type_index:
                self._type_index[event_type] = []
            self._type_index[event_type].append(event.event_id)

    def list_events(self) -> list[EventEnvelope]:
        """
        List all events in history preserving insertion order.
        
        Returns:
            List of all events
        """
        with self._lock:
            return list(self._events.values())

    def get_event(self, event_id: str) -> EventEnvelope | None:
        """
        Get an event by ID.
        
        Args:
            event_id: The event ID to look up
            
        Returns:
            The event or None if not found
        """
        with self._lock:
            return self._events.get(event_id)

    def find_by_type(self, event_type: str) -> list[EventEnvelope]:
        """
        Find events by type.
        
        Args:
            event_type: The event type to find
            
        Returns:
            List of matching events in insertion order
        """
        with self._lock:
            event_ids = self._type_index.get(event_type, [])
            return [self._events[eid] for eid in event_ids if eid in self._events]

    def find_by_correlation_id(self, correlation_id: str) -> list[EventEnvelope]:
        """
        Find events by correlation ID.
        
        Args:
            correlation_id: The correlation ID to find
            
        Returns:
            List of matching events in insertion order
        """
        with self._lock:
            event_ids = self._correlation_index.get(correlation_id, [])
            return [self._events[eid] for eid in event_ids if eid in self._events]

    def find_by_idempotency_key(self, idempotency_key: str) -> list[EventEnvelope]:
        """
        Find events by idempotency key.
        
        Args:
            idempotency_key: The idempotency key to find
            
        Returns:
            List of matching events (typically 0 or 1)
        """
        with self._lock:
            event_id = self._idempotency_index.get(idempotency_key)
            if event_id and event_id in self._events:
                return [self._events[event_id]]
            return []

    def has_event(self, event_id: str) -> bool:
        """
        Check if an event exists.
        
        Args:
            event_id: The event ID to check
            
        Returns:
            True if the event exists
        """
        with self._lock:
            return event_id in self._events

    def has_idempotency_key(self, idempotency_key: str) -> bool:
        """
        Check if an idempotency key exists.
        
        Args:
            idempotency_key: The idempotency key to check
            
        Returns:
            True if the key exists
        """
        with self._lock:
            return idempotency_key in self._idempotency_index

    def clear(self) -> None:
        """Clear all events from history."""
        with self._lock:
            self._events.clear()
            self._idempotency_index.clear()
            self._correlation_index.clear()
            self._type_index.clear()

    def count(self) -> int:
        """
        Get the total number of events.
        
        Returns:
            The number of events in history
        """
        with self._lock:
            return len(self._events)

    def iterate(self) -> Iterator[EventEnvelope]:
        """
        Iterate over events in insertion order.
        
        Yields:
            Events in order
        """
        with self._lock:
            for event in self._events.values():
                yield event

    def iterate_by_type(self, event_type: str) -> Iterator[EventEnvelope]:
        """
        Iterate over events of a specific type in insertion order.
        
        Args:
            event_type: The event type to iterate
            
        Yields:
            Events of the specified type
        """
        with self._lock:
            event_ids = self._type_index.get(event_type, [])
            for eid in event_ids:
                if eid in self._events:
                    yield self._events[eid]

    def iterate_by_correlation(self, correlation_id: str) -> Iterator[EventEnvelope]:
        """
        Iterate over events with a specific correlation ID.
        
        Args:
            correlation_id: The correlation ID to iterate
            
        Yields:
            Events with the specified correlation ID
        """
        with self._lock:
            event_ids = self._correlation_index.get(correlation_id, [])
            for eid in event_ids:
                if eid in self._events:
                    yield self._events[eid]

    def get_stats(self) -> dict:
        """
        Get statistics about the history.
        
        Returns:
            Dictionary with statistics
        """
        with self._lock:
            return {
                "total_events": len(self._events),
                "event_types": len(self._type_index),
                "correlation_ids": len(self._correlation_index),
                "idempotency_keys": len(self._idempotency_index),
            }
