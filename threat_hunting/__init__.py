"""
threat_hunting/__init__.py

Threat Hunting Module.

Phase 6G - Threat Hunting Foundation.

IMPORTANT: This module does NOT perform:
- AI/LLM
- Autonomous Hunting
- SOAR
- Incident Response
- Response Actions
- Containment
- Remediation
- Live Endpoint Collection
- Detection Rule Execution
- Threat Feed Polling
- External Lookups
- Risk Scoring

Threat Hunting is a consumer of intelligence.
Threat Hunting does NOT produce canonical knowledge.
"""
from threat_hunting.models import (
    Hunt,
    HuntSession,
    HuntScope,
    HuntObjective,
    HuntHypothesis,
    HuntObservation,
    HuntFinding,
    HuntRecommendation,
    EvidenceBundle,
    EvidenceReference,
    EvidenceChain,
    ThreatHuntReport,
    ReportSection,
    HuntExplanation,
    ConfidenceHistory,
)

from threat_hunting.models.enums import (
    HuntStatus,
    SessionStatus,
    HypothesisStatus,
    FindingSeverity,
    RecommendationType,
    EvidenceType,
    ConfidenceLevel,
)

from threat_hunting.service import (
    HuntService,
    HypothesisService,
    ObservationService,
    FindingService,
    ReportService,
)

from threat_hunting.validation import (
    HuntValidator,
    HypothesisValidator,
    ObservationValidator,
    FindingValidator,
    EvidenceValidator,
    SessionValidator,
    ExplanationValidator,
    ValidationResult,
)

from threat_hunting.events import (
    HuntEventEmitter,
    HuntEventType,
)

__all__ = [
    # Models
    "Hunt",
    "HuntSession",
    "HuntScope",
    "HuntObjective",
    "HuntHypothesis",
    "HuntObservation",
    "HuntFinding",
    "HuntRecommendation",
    "EvidenceBundle",
    "EvidenceReference",
    "EvidenceChain",
    "ThreatHuntReport",
    "ReportSection",
    "HuntExplanation",
    "ConfidenceHistory",
    # Enums
    "HuntStatus",
    "SessionStatus",
    "HypothesisStatus",
    "FindingSeverity",
    "RecommendationType",
    "EvidenceType",
    "ConfidenceLevel",
    # Services
    "HuntService",
    "HypothesisService",
    "ObservationService",
    "FindingService",
    "ReportService",
    # Validation
    "HuntValidator",
    "HypothesisValidator",
    "ObservationValidator",
    "FindingValidator",
    "EvidenceValidator",
    "SessionValidator",
    "ExplanationValidator",
    "ValidationResult",
    # Events
    "HuntEventEmitter",
    "HuntEventType",
]
