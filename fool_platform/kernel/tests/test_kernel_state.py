"""
platform/kernel/tests/test_kernel_state.py

Tests for kernel state management.
"""
import pytest

from fool_platform.kernel.kernel_state import KernelState, KernelStateManager


class TestKernelState:
    """Tests for KernelState enum."""
    
    def test_state_values(self):
        """Test that all expected states exist."""
        assert KernelState.CREATED is not None
        assert KernelState.STARTING is not None
        assert KernelState.RUNNING is not None
        assert KernelState.STOPPING is not None
        assert KernelState.STOPPED is not None
        assert KernelState.FAILED is not None
    
    def test_can_transition_valid(self):
        """Test valid state transitions."""
        assert KernelState.CREATED.can_transition_to(KernelState.STARTING)
        assert KernelState.STARTING.can_transition_to(KernelState.RUNNING)
        assert KernelState.RUNNING.can_transition_to(KernelState.STOPPING)
        assert KernelState.STOPPING.can_transition_to(KernelState.STOPPED)
        assert KernelState.STOPPED.can_transition_to(KernelState.STARTING)
        assert KernelState.FAILED.can_transition_to(KernelState.STARTING)
    
    def test_cannot_transition_invalid(self):
        """Test invalid state transitions."""
        assert not KernelState.CREATED.can_transition_to(KernelState.RUNNING)
        assert not KernelState.RUNNING.can_transition_to(KernelState.CREATED)
        assert not KernelState.STOPPED.can_transition_to(KernelState.RUNNING)


class TestKernelStateManager:
    """Tests for KernelStateManager."""
    
    def test_initial_state(self):
        """Test initial state is CREATED."""
        manager = KernelStateManager()
        assert manager.state == KernelState.CREATED
        assert not manager.is_running
        assert not manager.is_started
        assert not manager.is_stopped
    
    def test_valid_transition(self):
        """Test valid state transition."""
        manager = KernelStateManager()
        manager.transition_to(KernelState.STARTING)
        assert manager.state == KernelState.STARTING
    
    def test_invalid_transition(self):
        """Test invalid state transition raises."""
        manager = KernelStateManager()
        with pytest.raises(ValueError):
            manager.transition_to(KernelState.RUNNING)
    
    def test_is_running(self):
        """Test is_running property."""
        manager = KernelStateManager()
        assert not manager.is_running
        manager.transition_to(KernelState.STARTING)
        assert not manager.is_running
        manager.transition_to(KernelState.RUNNING)
        assert manager.is_running
    
    def test_is_started(self):
        """Test is_started property."""
        manager = KernelStateManager()
        assert not manager.is_started
        manager.transition_to(KernelState.STARTING)
        assert not manager.is_started  # STARTING is not started yet
        manager.transition_to(KernelState.RUNNING)
        assert manager.is_started
        manager.transition_to(KernelState.STOPPING)
        assert manager.is_started
    
    def test_failure_with_reason(self):
        """Test failure state with reason."""
        manager = KernelStateManager()
        manager.transition_to(KernelState.STARTING)
        manager.transition_to(KernelState.FAILED, "Test failure")
        assert manager.state == KernelState.FAILED
        assert manager.failure_reason == "Test failure"
    
    def test_repr(self):
        """Test string representation."""
        manager = KernelStateManager()
        assert "CREATED" in repr(manager)
