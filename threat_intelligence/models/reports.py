"""
threat_intelligence/models/reports.py

Report Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import ThreatBase, Auditable, Explainable
from threat_intelligence.models.enums import ReportType, ReportStatus, ThreatLevel


@dataclass(frozen=True)
class ThreatReport(ThreatBase, Auditable, Explainable):
    """Threat report."""
    title: str = ""
    description: str = ""
    report_type: str = ReportType.TECHNICAL.value
    status: str = ReportStatus.DRAFT.value
    author: str = ""
    threat_level: str = ThreatLevel.MEDIUM.value
    executive_summary: str = ""
    key_findings: tuple[str, ...] = field(default_factory=tuple)
    recommendations: tuple[str, ...] = field(default_factory=tuple)
    related_indicators: tuple[str, ...] = field(default_factory=tuple)
    related_actors: tuple[str, ...] = field(default_factory=tuple)
    related_malware: tuple[str, ...] = field(default_factory=tuple)
    related_campaigns: tuple[str, ...] = field(default_factory=tuple)
    affected_sectors: tuple[str, ...] = field(default_factory=tuple)
    affected_geographies: tuple[str, ...] = field(default_factory=tuple)
    published_date: str = ""
    valid_until: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    sections: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "report_type": self.report_type,
            "status": self.status,
            "author": self.author,
            "threat_level": self.threat_level,
            "executive_summary": self.executive_summary,
            "key_findings": list(self.key_findings),
            "recommendations": list(self.recommendations),
            "related_indicators": list(self.related_indicators),
            "related_actors": list(self.related_actors),
            "related_malware": list(self.related_malware),
            "related_campaigns": list(self.related_campaigns),
            "affected_sectors": list(self.affected_sectors),
            "affected_geographies": list(self.affected_geographies),
            "published_date": self.published_date,
            "valid_until": self.valid_until,
            "tags": list(self.tags),
            "sections": list(self.sections),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class ExecutiveReport(ThreatReport):
    """Executive summary report."""
    key_metrics: dict[str, Any] = field(default_factory=dict)
    impact_assessment: str = ""
    risk_rating: str = ""
    time_horizon: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "key_metrics": self.key_metrics,
            "impact_assessment": self.impact_assessment,
            "risk_rating": self.risk_rating,
            "time_horizon": self.time_horizon,
        })
        return base


@dataclass(frozen=True)
class TechnicalReport(ThreatReport):
    """Technical analysis report."""
    technical_details: dict[str, Any] = field(default_factory=dict)
    ioc_list: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    detection_rules: tuple[str, ...] = field(default_factory=tuple)
    malware_analysis: dict[str, Any] = field(default_factory=dict)
    network_indicators: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "technical_details": self.technical_details,
            "ioc_list": list(self.ioc_list),
            "detection_rules": list(self.detection_rules),
            "malware_analysis": self.malware_analysis,
            "network_indicators": list(self.network_indicators),
        })
        return base
