"""
intelligence/__init__.py

Intelligence Runtime Foundation for FOOL Platform.

IMPORTANT: This is Phase 4A. This does NOT implement:
- Real Intelligence Capabilities
- Cyber Intelligence
- Threat Intelligence
- OSINT
- AI/LLM
- Planning
- Autonomous Decisions
- Connectors

The Intelligence Runtime ONLY:
- Coordinates execution
- Orchestrates workflows
- Validates inputs
- Records outputs
- Delegates to other layers

Real intelligence capabilities begin only in Phase 4B.
"""
from intelligence.models import (
    IntelligenceTask,
    IntelligenceResult,
    IntelligenceFinding,
    IntelligenceArtifact,
    TaskStatus,
    FindingType,
    ArtifactType,
)

__all__ = [
    "IntelligenceTask",
    "IntelligenceResult",
    "IntelligenceFinding",
    "IntelligenceArtifact",
    "TaskStatus",
    "FindingType",
    "ArtifactType",
]
