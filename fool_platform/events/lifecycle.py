"""
fool_platform/events/lifecycle.py

Event Bus lifecycle management.
"""
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock


class EventBusState(str, Enum):
    """Possible states of the Event Bus."""
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    DISPOSED = "disposed"


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


@dataclass
class EventBusLifecycle:
    """
    Lifecycle manager for the Event Bus.
    
    Manages state transitions and ensures proper initialization,
    startup, shutdown, and disposal.
    """
    _state: EventBusState = field(default=EventBusState.UNINITIALIZED)
    _lock: Lock = field(default_factory=Lock)

    @property
    def state(self) -> EventBusState:
        """Get the current lifecycle state."""
        with self._lock:
            return self._state

    @property
    def is_initialized(self) -> bool:
        """Check if the Event Bus is initialized."""
        return self.state in (
            EventBusState.INITIALIZED,
            EventBusState.RUNNING,
            EventBusState.STOPPING,
            EventBusState.STOPPED,
        )

    @property
    def is_running(self) -> bool:
        """Check if the Event Bus is running."""
        return self.state == EventBusState.RUNNING

    @property
    def is_stopped(self) -> bool:
        """Check if the Event Bus is stopped."""
        return self.state in (EventBusState.STOPPED, EventBusState.DISPOSED)

    @property
    def is_disposed(self) -> bool:
        """Check if the Event Bus is disposed."""
        return self.state == EventBusState.DISPOSED

    def _transition(self, target: EventBusState) -> None:
        """Perform a state transition with validation."""
        with self._lock:
            current = self._state
            valid_transitions = {
                EventBusState.UNINITIALIZED: {EventBusState.INITIALIZED},
                EventBusState.INITIALIZED: {EventBusState.RUNNING, EventBusState.DISPOSED},
                EventBusState.RUNNING: {EventBusState.STOPPING},
                EventBusState.STOPPING: {EventBusState.STOPPED},
                EventBusState.STOPPED: {EventBusState.INITIALIZED, EventBusState.DISPOSED},
                EventBusState.DISPOSED: set(),
            }
            
            if target not in valid_transitions.get(current, set()):
                raise InvalidStateTransitionError(
                    f"Cannot transition from {current.value} to {target.value}"
                )
            
            self._state = target

    def initialize(self) -> None:
        """
        Initialize the Event Bus.
        
        Must be called before start(). Can be called after stop() to reinitialize.
        
        Raises:
            InvalidStateTransitionError: If called from an invalid state
        """
        self._transition(EventBusState.INITIALIZED)

    def start(self) -> None:
        """
        Start the Event Bus.
        
        Must be called after initialize(). Enables publishing and dispatching.
        
        Raises:
            InvalidStateTransitionError: If called from an invalid state
        """
        self._transition(EventBusState.RUNNING)

    def stop(self) -> None:
        """
        Stop the Event Bus.
        
        Prevents new dispatches but preserves history unless reset is called.
        
        Raises:
            InvalidStateTransitionError: If called from an invalid state
        """
        self._transition(EventBusState.STOPPING)
        self._transition(EventBusState.STOPPED)

    def reset(self) -> None:
        """
        Reset the Event Bus to uninitialized state.
        
        Clears in-memory state. Must be called before reinitializing after stop().
        
        Raises:
            InvalidStateTransitionError: If called from an invalid state
        """
        with self._lock:
            if self._state == EventBusState.RUNNING:
                raise InvalidStateTransitionError(
                    "Cannot reset while running. Call stop() first."
                )
            self._state = EventBusState.UNINITIALIZED

    def dispose(self) -> None:
        """
        Dispose the Event Bus permanently.
        
        After disposal, the Event Bus cannot be reused.
        
        Raises:
            InvalidStateTransitionError: If called from an invalid state
        """
        self._transition(EventBusState.DISPOSED)

    def ensure_can_publish(self) -> None:
        """
        Ensure the Event Bus can accept published events.
        
        Raises:
            InvalidStateTransitionError: If the Event Bus cannot accept events
        """
        with self._lock:
            if self._state == EventBusState.DISPOSED:
                raise InvalidStateTransitionError("Event Bus is disposed and cannot accept events")
            if self._state not in (EventBusState.RUNNING, EventBusState.INITIALIZED):
                raise InvalidStateTransitionError(
                    f"Event Bus cannot accept events in state {self._state.value}"
                )

    def ensure_can_dispatch(self) -> None:
        """
        Ensure the Event Bus can dispatch events.
        
        Raises:
            InvalidStateTransitionError: If the Event Bus cannot dispatch events
        """
        with self._lock:
            if self._state == EventBusState.DISPOSED:
                raise InvalidStateTransitionError("Event Bus is disposed and cannot dispatch events")
            if self._state != EventBusState.RUNNING:
                raise InvalidStateTransitionError(
                    f"Event Bus cannot dispatch events in state {self._state.value}"
                )

    def __repr__(self) -> str:
        return f"EventBusLifecycle(state={self._state.value})"
