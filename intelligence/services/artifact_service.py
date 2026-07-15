"""
intelligence/services/artifact_service.py

Artifact Service.

Manages intelligence artifacts.
"""
from typing import Any

from intelligence.models import IntelligenceArtifact, ArtifactType


class ArtifactService:
    """
    Service for artifact management.
    
    Coordinates:
    - Artifact creation
    - Artifact retrieval
    - Artifact storage
    """
    
    def __init__(self) -> None:
        """Initialize the service."""
        self._artifacts: dict[str, IntelligenceArtifact] = {}
    
    def create_artifact(
        self,
        artifact_type: str,
        content: Any,
        name: str = "",
        source_task_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new artifact.
        
        Args:
            artifact_type: Type of artifact
            content: Artifact content
            name: Artifact name
            source_task_id: Source task ID
            metadata: Optional metadata
            
        Returns:
            Created artifact
        """
        artifact = IntelligenceArtifact(
            artifact_type=ArtifactType(artifact_type),
            content=content,
            name=name,
            source_task_id=source_task_id,
            metadata=metadata or {},
        )
        
        self._artifacts[artifact.artifact_id] = artifact
        
        return artifact.to_dict()
    
    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        """Get artifact by ID."""
        artifact = self._artifacts.get(artifact_id)
        if artifact:
            return artifact.to_dict()
        return None
    
    def list_artifacts(
        self,
        artifact_type: str | None = None,
        source_task_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        List artifacts with optional filters.
        
        Args:
            artifact_type: Optional type filter
            source_task_id: Optional task filter
            
        Returns:
            List of artifacts
        """
        artifacts = list(self._artifacts.values())
        
        if artifact_type:
            artifacts = [
                a for a in artifacts
                if a.artifact_type.value == artifact_type
            ]
        
        if source_task_id:
            artifacts = [
                a for a in artifacts
                if a.source_task_id == source_task_id
            ]
        
        return [a.to_dict() for a in artifacts]
    
    def delete_artifact(self, artifact_id: str) -> bool:
        """Delete an artifact."""
        if artifact_id in self._artifacts:
            del self._artifacts[artifact_id]
            return True
        return False
