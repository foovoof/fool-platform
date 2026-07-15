"""
domain/annotation.py

Annotation domain model - human-added commentary on domain objects.
Mirrors contracts/domain/annotation.schema.json field-for-field.
"""
from dataclasses import dataclass, field
from enum import Enum

from .common import (
    EMPTY_METADATA,
    Metadata,
    new_id,
    utc_now,
)


class AnnotationType(str, Enum):
    """Types of annotations that can be added."""
    COMMENT = "comment"
    NOTE = "note"
    TAG = "tag"
    CLASSIFICATION = "classification"
    FLAG = "flag"
    RESOLUTION = "resolution"
    REVIEW = "review"
    OTHER = "other"


@dataclass(frozen=True)
class Annotation:
    """
    Annotation represents human-added commentary on domain objects.
    
    Annotations provide human context, review notes, and editorial
    commentary that supplements automated analysis.
    """
    id: str
    created_at: str
    updated_at: str
    annotation_type: AnnotationType
    content: str
    author: str
    target_ref: str
    provenance: str | None = None
    parent_annotation_ref: str | None = None
    tags: frozenset = field(default_factory=frozenset)
    metadata: Metadata = field(default_factory=lambda: dict(EMPTY_METADATA))

    @classmethod
    def create(
        cls,
        annotation_type: AnnotationType,
        content: str,
        author: str,
        target_ref: str,
        provenance: str | None = None,
        parent_annotation_ref: str | None = None,
        tags: list[str] | None = None,
        metadata: Metadata | None = None,
    ) -> "Annotation":
        """Create a new Annotation."""
        timestamp = utc_now()
        return cls(
            id=new_id(),
            created_at=timestamp,
            updated_at=timestamp,
            annotation_type=annotation_type,
            content=content,
            author=author,
            target_ref=target_ref,
            provenance=provenance,
            parent_annotation_ref=parent_annotation_ref,
            tags=frozenset(tags) if tags else frozenset(),
            metadata=dict(metadata) if metadata else dict(EMPTY_METADATA),
        )


__all__ = [
    "Annotation",
    "AnnotationType",
]
