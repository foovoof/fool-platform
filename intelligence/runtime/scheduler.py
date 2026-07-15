"""
intelligence/runtime/scheduler.py

Runtime Scheduler.

Schedules and coordinates task execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from intelligence.models import IntelligenceTask


class ScheduleStatus(Enum):
    """Schedule status."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Schedule:
    """Represents a task schedule."""
    schedule_id: str = field(default_factory=lambda: str(uuid4()))
    task: IntelligenceTask | None = None
    scheduled_at: str | None = None
    status: ScheduleStatus = ScheduleStatus.PENDING
    metadata: dict[str, Any] = field(default_factory=dict)


class RuntimeScheduler:
    """
    Schedules and coordinates task execution.
    
    Responsibilities:
    - Queue tasks
    - Schedule execution
    - Coordinate execution order
    - Track schedules
    
    NOTE: This is a coordinator, not an executor.
    """
    
    def __init__(self) -> None:
        """Initialize the scheduler."""
        self._queue: list[IntelligenceTask] = []
        self._schedules: dict[str, Schedule] = {}
    
    def submit(self, task: IntelligenceTask) -> str:
        """
        Submit a task to the queue.
        
        Args:
            task: Task to submit
            
        Returns:
            Schedule ID
        """
        schedule = Schedule(task=task)
        self._schedules[schedule.schedule_id] = schedule
        self._queue.append(task)
        schedule.status = ScheduleStatus.SCHEDULED
        return schedule.schedule_id
    
    def cancel(self, schedule_id: str) -> bool:
        """
        Cancel a scheduled task.
        
        Args:
            schedule_id: Schedule ID to cancel
            
        Returns:
            True if cancelled
        """
        schedule = self._schedules.get(schedule_id)
        if schedule and schedule.status in (
            ScheduleStatus.PENDING,
            ScheduleStatus.SCHEDULED,
        ):
            schedule.status = ScheduleStatus.CANCELLED
            if schedule.task in self._queue:
                self._queue.remove(schedule.task)
            return True
        return False
    
    def get_next(self) -> IntelligenceTask | None:
        """
        Get the next task from the queue.
        
        Returns:
            Next task or None
        """
        if self._queue:
            return self._queue.pop(0)
        return None
    
    def get_schedule(self, schedule_id: str) -> Schedule | None:
        """Get schedule by ID."""
        return self._schedules.get(schedule_id)
    
    def list_pending(self) -> list[str]:
        """List pending schedule IDs."""
        return [
            sid for sid, s in self._schedules.items()
            if s.status == ScheduleStatus.PENDING
        ]
    
    def queue_size(self) -> int:
        """Get queue size."""
        return len(self._queue)
