from __future__ import annotations

"""
knowledge/graph/repository/evidence_repository.py

Evidence repository implementation.

In-memory storage for evidence records.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class EvidenceRecord:
    """Record of evidence supporting a knowledge assertion."""
    evidence_id: str = field(default_factory=lambda: str(uuid4()))
    evidence_type: str = ""
    content: str = ""
    source_ref: str = ""
    entity_refs: list[str] = field(default_factory=list)
    relationship_refs: list[str] = field(default_factory=list)
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    validated: bool = False
    validated_at: str | None = None


class EvidenceRepository:
    """
    In-memory repository for evidence records.
    
    Provides storage and retrieval of evidence information.
    """

    def __init__(self) -> None:
        """Initialize the repository."""
        self._evidence: dict[str, EvidenceRecord] = {}
        self._type_index: dict[str, list[str]] = {}
        self._source_index: dict[str, list[str]] = {}
        self._entity_ref_index: dict[str, list[str]] = {}

    def create(self, evidence: EvidenceRecord) -> EvidenceRecord:
        """
        Create a new evidence record.
        
        Args:
            evidence: The evidence to create
            
        Returns:
            The created evidence
        """
        if evidence.evidence_id in self._evidence:
            raise ValueError(f"Evidence {evidence.evidence_id} already exists")
        
        self._evidence[evidence.evidence_id] = evidence
        
        # Update type index
        if evidence.evidence_type:
            if evidence.evidence_type not in self._type_index:
                self._type_index[evidence.evidence_type] = []
            self._type_index[evidence.evidence_type].append(evidence.evidence_id)
        
        # Update source index
        if evidence.source_ref:
            if evidence.source_ref not in self._source_index:
                self._source_index[evidence.source_ref] = []
            self._source_index[evidence.source_ref].append(evidence.evidence_id)
        
        # Update entity ref index
        for entity_ref in evidence.entity_refs:
            if entity_ref not in self._entity_ref_index:
                self._entity_ref_index[entity_ref] = []
            if evidence.evidence_id not in self._entity_ref_index[entity_ref]:
                self._entity_ref_index[entity_ref].append(evidence.evidence_id)
        
        return evidence

    def update(self, evidence: EvidenceRecord) -> EvidenceRecord:
        """
        Update an existing evidence record.
        
        Args:
            evidence: The evidence to update
            
        Returns:
            The updated evidence
        """
        if evidence.evidence_id not in self._evidence:
            raise ValueError(f"Evidence {evidence.evidence_id} not found")
        self._evidence[evidence.evidence_id] = evidence
        return evidence

    def delete(self, evidence_id: str) -> bool:
        """
        Delete an evidence record by ID.
        
        Args:
            evidence_id: The ID of the evidence to delete
            
        Returns:
            True if deleted
        """
        if evidence_id not in self._evidence:
            return False
        
        evidence = self._evidence[evidence_id]
        
        # Remove from type index
        if evidence.evidence_type in self._type_index:
            self._type_index[evidence.evidence_type] = [
                e for e in self._type_index[evidence.evidence_type]
                if e != evidence_id
            ]
        
        # Remove from source index
        if evidence.source_ref in self._source_index:
            self._source_index[evidence.source_ref] = [
                e for e in self._source_index[evidence.source_ref]
                if e != evidence_id
            ]
        
        # Remove from entity ref index
        for entity_ref in evidence.entity_refs:
            if entity_ref in self._entity_ref_index:
                self._entity_ref_index[entity_ref] = [
                    e for e in self._entity_ref_index[entity_ref]
                    if e != evidence_id
                ]
        
        del self._evidence[evidence_id]
        return True

    def get_by_id(self, evidence_id: str) -> EvidenceRecord | None:
        """Get an evidence record by ID."""
        return self._evidence.get(evidence_id)

    def find_by_type(self, evidence_type: str) -> list[EvidenceRecord]:
        """
        Find evidence by type.
        
        Args:
            evidence_type: The evidence type to filter by
            
        Returns:
            List of matching evidence
        """
        evidence_ids = self._type_index.get(evidence_type, [])
        return [
            self._evidence[eid]
            for eid in evidence_ids
            if eid in self._evidence
        ]

    def find_by_source(self, source_ref: str) -> list[EvidenceRecord]:
        """
        Find evidence by source.
        
        Args:
            source_ref: The source reference to filter by
            
        Returns:
            List of matching evidence
        """
        evidence_ids = self._source_index.get(source_ref, [])
        return [
            self._evidence[eid]
            for eid in evidence_ids
            if eid in self._evidence
        ]

    def find_by_entity_ref(self, entity_ref: str) -> list[EvidenceRecord]:
        """
        Find evidence supporting an entity.
        
        Args:
            entity_ref: The entity reference
            
        Returns:
            List of supporting evidence
        """
        evidence_ids = self._entity_ref_index.get(entity_ref, [])
        return [
            self._evidence[eid]
            for eid in evidence_ids
            if eid in self._evidence
        ]

    def mark_validated(self, evidence_id: str) -> bool:
        """
        Mark evidence as validated.
        
        Args:
            evidence_id: The evidence ID
            
        Returns:
            True if marked
        """
        evidence = self._evidence.get(evidence_id)
        if not evidence:
            return False
        
        evidence.validated = True
        evidence.validated_at = datetime.now(timezone.utc).isoformat()
        return True

    def list(self, **kwargs: Any) -> list[EvidenceRecord]:
        """
        List evidence with optional filtering.
        
        Args:
            **kwargs: Optional filters:
                - validated: Filter by validation status
                - evidence_type: Filter by type
                - min_confidence: Minimum confidence threshold
                
        Returns:
            List of matching evidence
        """
        results = list(self._evidence.values())
        
        validated = kwargs.get("validated")
        if validated is not None:
            results = [e for e in results if e.validated == validated]
        
        evidence_type = kwargs.get("evidence_type")
        if evidence_type:
            results = [e for e in results if e.evidence_type == evidence_type]
        
        min_confidence = kwargs.get("min_confidence")
        if min_confidence is not None:
            results = [e for e in results if e.confidence >= min_confidence]
        
        return results

    def exists(self, evidence_id: str) -> bool:
        """Check if evidence exists."""
        return evidence_id in self._evidence

    def count(self, **kwargs: Any) -> int:
        """Count evidence matching criteria."""
        return len(self.list(**kwargs))

    def clear(self) -> None:
        """Clear all evidence."""
        self._evidence.clear()
        self._type_index.clear()
        self._source_index.clear()
        self._entity_ref_index.clear()
