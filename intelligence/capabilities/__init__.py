"""
intelligence/capabilities/__init__.py

Intelligence Capabilities Foundation.

Provides generic intelligence capabilities for FOOL Platform.

IMPORTANT: This phase implements generic capabilities only.
- No Cyber Intelligence
- No OSINT
- No AI/LLM
- No Connectors

Phase 5A will implement Connectors Foundation.
"""
from intelligence.capabilities.models import (
    CapabilityDefinition,
    CapabilityTask,
    CapabilityResult,
    CapabilityArtifact,
    CapabilityFinding,
    CapabilityExecutionRecord,
    CapabilityType,
    CapabilityStatus,
    FindingType,
)

__all__ = [
    "CapabilityDefinition",
    "CapabilityTask",
    "CapabilityResult",
    "CapabilityArtifact",
    "CapabilityFinding",
    "CapabilityExecutionRecord",
    "CapabilityType",
    "CapabilityStatus",
    "FindingType",
]
