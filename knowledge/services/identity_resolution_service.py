from __future__ import annotations

"""
knowledge/services/identity_resolution_service.py

Identity Resolution Service for the Knowledge Layer.

Orchestrates identity resolution operations.
"""
from typing import Any

from knowledge.graph.repository import IdentityRepository
from knowledge.resolution import IdentityResolutionEngine, IdentityMatch
from knowledge.events import KnowledgeEventEmitter


class IdentityResolutionService:
    """
    Service for identity resolution.
    
    Orchestrates:
    - Identity matching
    - Identity deduplication
    - Event emission
    """

    def __init__(
        self,
        identity_repository: IdentityRepository | None = None,
        resolution_engine: IdentityResolutionEngine | None = None,
        event_emitter: KnowledgeEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            identity_repository: Optional identity repository
            resolution_engine: Optional resolution engine
            event_emitter: Optional event emitter
        """
        self._repository = identity_repository or IdentityRepository()
        self._engine = resolution_engine or IdentityResolutionEngine()
        self._event_emitter = event_emitter or KnowledgeEventEmitter()

    def match_identities(
        self,
        source: dict[str, str],
        target: dict[str, str],
    ) -> IdentityMatch:
        """
        Match two identities.
        
        Args:
            source: Source identity with type and value
            target: Target identity with type and value
            
        Returns:
            IdentityMatch result
        """
        result = self._engine.match(source, target)
        
        if result.is_match:
            self._event_emitter.emit_entity_resolved(
                result.source_identity_id,
                result.target_identity_id,
                result.match_type.value,
                result.confidence,
            )
        
        return result

    def find_duplicate_identities(
        self,
        identities: list[dict[str, str]],
    ) -> list[IdentityMatch]:
        """
        Find duplicate identities.
        
        Args:
            identities: List of identities to check
            
        Returns:
            List of duplicate matches
        """
        return self._engine.find_duplicates(identities)

    def create_identity(
        self,
        identity_type: str,
        raw_value: str,
        normalized_value: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new identity record.
        
        Args:
            identity_type: Identity type
            raw_value: Raw identity value
            normalized_value: Optional normalized value
            
        Returns:
            Created identity
        """
        from knowledge.graph.repository.identity_repository import IdentityRecord
        
        record = IdentityRecord(
            identity_type=identity_type,
            raw_value=raw_value,
            normalized_value=normalized_value or self._engine.normalize(raw_value),
        )
        
        self._repository.create(record)
        
        return {
            "identity_id": record.identity_id,
            "identity_type": record.identity_type,
            "raw_value": record.raw_value,
            "normalized_value": record.normalized_value,
        }

    def get_identity(self, identity_id: str) -> dict[str, Any] | None:
        """Get an identity by ID."""
        record = self._repository.get_by_id(identity_id)
        if record:
            return {
                "identity_id": record.identity_id,
                "identity_type": record.identity_type,
                "raw_value": record.raw_value,
                "normalized_value": record.normalized_value,
                "entity_refs": record.entity_refs,
                "resolved": record.resolved,
            }
        return None
