from __future__ import annotations

"""
knowledge/graph/queries/query_context.py

Query context for the Knowledge Layer.

Provides context for all query operations.
"""
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Pagination:
    """Pagination parameters."""
    offset: int = 0
    limit: int = 100
    
    def apply(self, items: list[Any]) -> list[Any]:
        """Apply pagination to a list of items."""
        return items[self.offset : self.offset + self.limit]
    
    @classmethod
    def first(cls, count: int = 100) -> "Pagination":
        """Create pagination for first n items."""
        return cls(offset=0, limit=count)


@dataclass
class Filters:
    """Filter parameters for queries."""
    filters: dict[str, Any] = field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a filter value."""
        return self.filters.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a filter value."""
        self.filters[key] = value
    
    def has(self, key: str) -> bool:
        """Check if a filter exists."""
        return key in self.filters
    
    def match(self, item: dict[str, Any]) -> bool:
        """Check if an item matches all filters."""
        for key, value in self.filters.items():
            if key not in item:
                return False
            if item[key] != value:
                return False
        return True


@dataclass
class QueryContext:
    """
    Context for query operations.
    
    Provides tracing, correlation, filtering, and pagination.
    """
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str | None = None
    filters: Filters = field(default_factory=Filters)
    pagination: Pagination = field(default_factory=Pagination)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        trace_id: str | None = None,
        correlation_id: str | None = None,
        **kwargs: Any,
    ) -> "QueryContext":
        """Create a new query context."""
        return cls(
            trace_id=trace_id or str(uuid4()),
            correlation_id=correlation_id,
            **kwargs,
        )
    
    def with_filter(self, key: str, value: Any) -> "QueryContext":
        """Create a new context with an additional filter."""
        new_filters = Filters(filters=self.filters.filters.copy())
        new_filters.set(key, value)
        return QueryContext(
            trace_id=self.trace_id,
            correlation_id=self.correlation_id,
            filters=new_filters,
            pagination=self.pagination,
            metadata=self.metadata.copy(),
        )
    
    def with_pagination(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ) -> "QueryContext":
        """Create a new context with modified pagination."""
        return QueryContext(
            trace_id=self.trace_id,
            correlation_id=self.correlation_id,
            filters=self.filters,
            pagination=Pagination(
                offset=offset if offset is not None else self.pagination.offset,
                limit=limit if limit is not None else self.pagination.limit,
            ),
            metadata=self.metadata.copy(),
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "filters": self.filters.filters,
            "pagination": {
                "offset": self.pagination.offset,
                "limit": self.pagination.limit,
            },
            "metadata": self.metadata,
        }
