"""
platform/kernel/app_context.py

Application context for the FOOL Platform kernel.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AppContext:
    """
    Immutable application context containing kernel-wide information.
    
    The app context is created during kernel bootstrap and provides
    access to kernel identity, configuration, and runtime information.
    """
    context_id: str
    kernel_id: str
    started_at: str
    environment: str
    version: str
    metadata: dict = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        environment: str = "development",
        version: str = "1.0.0",
        metadata: dict | None = None,
    ) -> "AppContext":
        """Factory method to create a new application context."""
        return cls(
            context_id=str(uuid4()),
            kernel_id=str(uuid4()),
            started_at=datetime.now(timezone.utc).isoformat(),
            environment=environment,
            version=version,
            metadata=metadata or {},
        )
    
    def with_metadata(self, **kwargs: Any) -> "AppContext":
        """Return a new AppContext with additional metadata."""
        return AppContext(
            context_id=self.context_id,
            kernel_id=self.kernel_id,
            started_at=self.started_at,
            environment=self.environment,
            version=self.version,
            metadata={**self.metadata, **kwargs},
        )
    
    def is_production(self) -> bool:
        """Returns True if running in production environment."""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Returns True if running in development environment."""
        return self.environment == "development"
    
    def is_testing(self) -> bool:
        """Returns True if running in testing environment."""
        return self.environment == "testing"


__all__ = [
    "AppContext",
]
