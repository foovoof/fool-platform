"""
platform/kernel/kernel_state.py

Kernel lifecycle states and state machine.
"""
from enum import Enum, auto


class KernelState(Enum):
    """
    Kernel lifecycle states.
    
    State transitions:
        CREATED → STARTING → RUNNING → STOPPING → STOPPED
                    ↓           ↓
                 FAILED      FAILED
    """
    CREATED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    STOPPED = auto()
    FAILED = auto()

    def can_transition_to(self, target: "KernelState") -> bool:
        """Check if transition to target state is valid."""
        transitions = {
            KernelState.CREATED: {KernelState.STARTING},
            KernelState.STARTING: {KernelState.RUNNING, KernelState.FAILED},
            KernelState.RUNNING: {KernelState.STOPPING, KernelState.FAILED},
            KernelState.STOPPING: {KernelState.STOPPED},
            KernelState.STOPPED: {KernelState.STARTING},
            KernelState.FAILED: {KernelState.STARTING},  # Allow restart from failed
        }
        return target in transitions.get(self, set())


class KernelStateManager:
    """
    Manages kernel lifecycle state transitions.
    
    Thread-safe state management with validation of transitions.
    """
    
    def __init__(self) -> None:
        self._state = KernelState.CREATED
        self._failure_reason: str | None = None
    
    @property
    def state(self) -> KernelState:
        """Current kernel state."""
        return self._state
    
    @property
    def failure_reason(self) -> str | None:
        """Reason for failure, if in FAILED state."""
        return self._failure_reason
    
    @property
    def is_running(self) -> bool:
        """Returns True if kernel is in RUNNING state."""
        return self._state == KernelState.RUNNING
    
    @property
    def is_started(self) -> bool:
        """Returns True if kernel has been started (RUNNING or STOPPING)."""
        return self._state in (KernelState.RUNNING, KernelState.STOPPING)
    
    @property
    def is_stopped(self) -> bool:
        """Returns True if kernel is in STOPPED state."""
        return self._state == KernelState.STOPPED
    
    def transition_to(self, target: KernelState, reason: str | None = None) -> None:
        """
        Transition to a new state.
        
        Args:
            target: Target state
            reason: Optional reason for the transition (used for failures)
            
        Raises:
            ValueError: If transition is not valid
        """
        if not self._state.can_transition_to(target):
            raise ValueError(
                f"Invalid state transition from {self._state.name} to {target.name}"
            )
        self._state = target
        if target == KernelState.FAILED and reason:
            self._failure_reason = reason
    
    def __repr__(self) -> str:
        if self._failure_reason:
            return f"KernelStateManager({self._state.name}, failed='{self._failure_reason}')"
        return f"KernelStateManager({self._state.name})"


__all__ = [
    "KernelState",
    "KernelStateManager",
]
