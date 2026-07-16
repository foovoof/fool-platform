"""
threat_hunting/service.py

Threat Hunting Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

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
    ThreatHuntReport,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._hunts: dict[str, Hunt] = {}
        self._sessions: dict[str, HuntSession] = {}
        self._hypotheses: dict[str, HuntHypothesis] = {}
        self._observations: dict[str, HuntObservation] = {}
        self._findings: dict[str, HuntFinding] = {}
        self._recommendations: dict[str, HuntRecommendation] = {}
        self._evidence_bundles: dict[str, EvidenceBundle] = {}
        self._reports: dict[str, ThreatHuntReport] = {}


_storage = InMemoryStorage()


class HuntService:
    """Service for managing hunts."""
    
    def create(
        self,
        name: str,
        title: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> Hunt:
        """Create new hunt."""
        hunt = Hunt(
            id=str(uuid4()),
            name=name,
            title=title,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._hunts[hunt.id] = hunt
        return hunt
    
    def get(self, hunt_id: str) -> Hunt | None:
        """Get hunt by ID."""
        return _storage._hunts.get(hunt_id)
    
    def update(self, hunt: Hunt) -> Hunt:
        """Update hunt."""
        updated = Hunt(
            id=hunt.id,
            name=hunt.name,
            title=hunt.title,
            description=hunt.description,
            status=hunt.status,
            priority=hunt.priority,
            scopes=hunt.scopes,
            objectives=hunt.objectives,
            hypothesis_ids=hunt.hypothesis_ids,
            session_ids=hunt.session_ids,
            finding_ids=hunt.finding_ids,
            report_ids=hunt.report_ids,
            related_hunts=hunt.related_hunts,
            tags=hunt.tags,
            started_at=hunt.started_at,
            completed_at=hunt.completed_at,
            author=hunt.author,
            reason=hunt.reason,
            source=hunt.source,
            created_at=hunt.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=hunt.created_by,
            modified_by=hunt.modified_by,
            version=hunt.version + 1,
            metadata=hunt.metadata,
            revision_history=hunt.revision_history,
        )
        _storage._hunts[updated.id] = updated
        return updated
    
    def delete(self, hunt_id: str) -> bool:
        """Delete hunt."""
        if hunt_id in _storage._hunts:
            del _storage._hunts[hunt_id]
            return True
        return False
    
    def list_all(self) -> list[Hunt]:
        """List all hunts."""
        return list(_storage._hunts.values())
    
    def find_by_status(self, status: str) -> list[Hunt]:
        """Find by status."""
        return [h for h in _storage._hunts.values() if h.status == status]
    
    def start_hunt(self, hunt_id: str) -> Hunt | None:
        """Start a hunt."""
        hunt = self.get(hunt_id)
        if not hunt:
            return None
        return self.update(Hunt(
            id=hunt.id,
            name=hunt.name,
            title=hunt.title,
            description=hunt.description,
            status="in_progress",
            priority=hunt.priority,
            scopes=hunt.scopes,
            objectives=hunt.objectives,
            hypothesis_ids=hunt.hypothesis_ids,
            session_ids=hunt.session_ids,
            finding_ids=hunt.finding_ids,
            report_ids=hunt.report_ids,
            related_hunts=hunt.related_hunts,
            tags=hunt.tags,
            started_at=datetime.now(timezone.utc).isoformat(),
            completed_at=hunt.completed_at,
            author=hunt.author,
            reason=hunt.reason,
            source=hunt.source,
            created_at=hunt.created_at,
            modified_at=hunt.modified_at,
            created_by=hunt.created_by,
            modified_by=hunt.modified_by,
            version=hunt.version,
            metadata=hunt.metadata,
            revision_history=hunt.revision_history,
        ))
    
    def complete_hunt(self, hunt_id: str) -> Hunt | None:
        """Complete a hunt."""
        hunt = self.get(hunt_id)
        if not hunt:
            return None
        return self.update(Hunt(
            id=hunt.id,
            name=hunt.name,
            title=hunt.title,
            description=hunt.description,
            status="completed",
            priority=hunt.priority,
            scopes=hunt.scopes,
            objectives=hunt.objectives,
            hypothesis_ids=hunt.hypothesis_ids,
            session_ids=hunt.session_ids,
            finding_ids=hunt.finding_ids,
            report_ids=hunt.report_ids,
            related_hunts=hunt.related_hunts,
            tags=hunt.tags,
            started_at=hunt.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            author=hunt.author,
            reason=hunt.reason,
            source=hunt.source,
            created_at=hunt.created_at,
            modified_at=hunt.modified_at,
            created_by=hunt.created_by,
            modified_by=hunt.modified_by,
            version=hunt.version,
            metadata=hunt.metadata,
            revision_history=hunt.revision_history,
        ))


class HypothesisService:
    """Service for managing hypotheses."""
    
    def create(
        self,
        hunt_id: str,
        title: str,
        hypothesis_text: str,
        author: str = "",
        **kwargs: Any,
    ) -> HuntHypothesis:
        """Create new hypothesis."""
        hypothesis = HuntHypothesis(
            id=str(uuid4()),
            hunt_id=hunt_id,
            title=title,
            hypothesis_text=hypothesis_text,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._hypotheses[hypothesis.id] = hypothesis
        return hypothesis
    
    def get(self, hypothesis_id: str) -> HuntHypothesis | None:
        """Get hypothesis by ID."""
        return _storage._hypotheses.get(hypothesis_id)
    
    def update(self, hypothesis: HuntHypothesis) -> HuntHypothesis:
        """Update hypothesis."""
        updated = HuntHypothesis(
            id=hypothesis.id,
            hunt_id=hypothesis.hunt_id,
            title=hypothesis.title,
            description=hypothesis.description,
            hypothesis_text=hypothesis.hypothesis_text,
            assumptions=hypothesis.assumptions,
            supporting_evidence=hypothesis.supporting_evidence,
            contradicting_evidence=hypothesis.contradicting_evidence,
            status=hypothesis.status,
            validated=hypothesis.validated,
            validated_by=hypothesis.validated_by,
            validated_at=hypothesis.validated_at,
            validation_notes=hypothesis.validation_notes,
            confidence_level=hypothesis.confidence_level,
            confidence_score=hypothesis.confidence_score,
            confidence_explanation=hypothesis.confidence_explanation,
            related_indicators=hypothesis.related_indicators,
            related_actors=hypothesis.related_actors,
            related_malware=hypothesis.related_malware,
            related_campaigns=hypothesis.related_campaigns,
            related_infrastructure=hypothesis.related_infrastructure,
            related_vulnerabilities=hypothesis.related_vulnerabilities,
            related_ttps=hypothesis.related_ttps,
            author=hypothesis.author,
            reason=hypothesis.reason,
            source=hypothesis.source,
            source_url=hypothesis.source_url,
            created_at=hypothesis.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=hypothesis.created_by,
            modified_by=hypothesis.modified_by,
            version=hypothesis.version + 1,
            metadata=hypothesis.metadata,
            revision_history=hypothesis.revision_history,
        )
        _storage._hypotheses[updated.id] = updated
        return updated
    
    def find_by_hunt(self, hunt_id: str) -> list[HuntHypothesis]:
        """Find hypotheses by hunt ID."""
        return [h for h in _storage._hypotheses.values() if h.hunt_id == hunt_id]


class ObservationService:
    """Service for managing observations."""
    
    def create(
        self,
        hunt_id: str,
        description: str,
        source: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> HuntObservation:
        """Create new observation."""
        observation = HuntObservation(
            id=str(uuid4()),
            hunt_id=hunt_id,
            description=description,
            source=source,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._observations[observation.id] = observation
        return observation
    
    def get(self, observation_id: str) -> HuntObservation | None:
        """Get observation by ID."""
        return _storage._observations.get(observation_id)
    
    def find_by_hunt(self, hunt_id: str) -> list[HuntObservation]:
        """Find observations by hunt ID."""
        return [o for o in _storage._observations.values() if o.hunt_id == hunt_id]


class FindingService:
    """Service for managing findings."""
    
    def create(
        self,
        hunt_id: str,
        title: str,
        description: str,
        author: str = "",
        **kwargs: Any,
    ) -> HuntFinding:
        """Create new finding."""
        finding = HuntFinding(
            id=str(uuid4()),
            hunt_id=hunt_id,
            title=title,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._findings[finding.id] = finding
        return finding
    
    def get(self, finding_id: str) -> HuntFinding | None:
        """Get finding by ID."""
        return _storage._findings.get(finding_id)
    
    def find_by_hunt(self, hunt_id: str) -> list[HuntFinding]:
        """Find findings by hunt ID."""
        return [f for f in _storage._findings.values() if f.hunt_id == hunt_id]


class ReportService:
    """Service for generating hunt reports."""
    
    def create(
        self,
        hunt_id: str,
        title: str,
        author: str = "",
        **kwargs: Any,
    ) -> ThreatHuntReport:
        """Create new report."""
        hunt = HuntService().get(hunt_id)
        
        report = ThreatHuntReport(
            id=str(uuid4()),
            hunt_id=hunt_id,
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._reports[report.id] = report
        return report
    
    def get(self, report_id: str) -> ThreatHuntReport | None:
        """Get report by ID."""
        return _storage._reports.get(report_id)
    
    def find_by_hunt(self, hunt_id: str) -> list[ThreatHuntReport]:
        """Find reports by hunt ID."""
        return [r for r in _storage._reports.values() if r.hunt_id == hunt_id]
