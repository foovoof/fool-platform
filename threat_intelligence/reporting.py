"""
threat_intelligence/reporting.py

Reporting Module.

Provides reporting capabilities for threat intelligence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from threat_intelligence.models import (
    ThreatReport,
    ExecutiveReport,
    TechnicalReport,
    ReportType,
    ReportStatus,
)


@dataclass(frozen=True)
class ReportSection:
    """Section of a report."""
    title: str = ""
    content: str = ""
    section_type: str = ""
    order: int = 0


class ReportBuilder:
    """
    Builder for threat reports.
    
    Provides structured report creation.
    """
    
    def __init__(self) -> None:
        self._title: str = ""
        self._description: str = ""
        self._report_type: str = ReportType.TECHNICAL.value
        self._author: str = ""
        self._sections: list[dict[str, Any]] = []
        self._tags: list[str] = []
        self._related_indicators: list[str] = []
        self._related_actors: list[str] = []
        self._related_malware: list[str] = []
    
    def set_title(self, title: str) -> ReportBuilder:
        """Set report title."""
        self._title = title
        return self
    
    def set_description(self, description: str) -> ReportBuilder:
        """Set report description."""
        self._description = description
        return self
    
    def set_report_type(self, report_type: str) -> ReportBuilder:
        """Set report type."""
        self._report_type = report_type
        return self
    
    def set_author(self, author: str) -> ReportBuilder:
        """Set report author."""
        self._author = author
        return self
    
    def add_section(
        self, title: str, content: str, section_type: str = ""
    ) -> ReportBuilder:
        """Add a section to the report."""
        self._sections.append({
            "title": title,
            "content": content,
            "section_type": section_type,
            "order": len(self._sections),
        })
        return self
    
    def add_tag(self, tag: str) -> ReportBuilder:
        """Add a tag."""
        self._tags.append(tag)
        return self
    
    def add_indicator(self, indicator_id: str) -> ReportBuilder:
        """Add a related indicator."""
        self._related_indicators.append(indicator_id)
        return self
    
    def add_actor(self, actor_id: str) -> ReportBuilder:
        """Add a related actor."""
        self._related_actors.append(actor_id)
        return self
    
    def add_malware(self, malware_id: str) -> ReportBuilder:
        """Add related malware."""
        self._related_malware.append(malware_id)
        return self
    
    def build(self) -> ThreatReport:
        """Build the report."""
        return ThreatReport(
            title=self._title,
            description=self._description,
            report_type=self._report_type,
            status=ReportStatus.DRAFT.value,
            author=self._author,
            sections=tuple(self._sections),
            tags=tuple(self._tags),
            related_indicators=tuple(self._related_indicators),
            related_actors=tuple(self._related_actors),
            related_malware=tuple(self._related_malware),
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )


class ReportValidator:
    """
    Validator for threat reports.
    """
    
    @staticmethod
    def validate(report: ThreatReport) -> tuple[bool, list[str]]:
        """
        Validate a report.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if not report.id:
            errors.append("Report ID is required")
        
        if not report.title:
            errors.append("Report title is required")
        
        if not report.report_type:
            errors.append("Report type is required")
        
        if not report.author:
            errors.append("Report author is required")
        
        valid_types = [t.value for t in ReportType]
        if report.report_type not in valid_types:
            errors.append(f"Invalid report type: {report.report_type}")
        
        valid_statuses = [s.value for s in ReportStatus]
        if report.status not in valid_statuses:
            errors.append(f"Invalid report status: {report.status}")
        
        return (len(errors) == 0, errors)


class ReportExporter:
    """
    Exporter for threat reports.
    
    Provides structured export without file I/O.
    """
    
    @staticmethod
    def to_dict(report: ThreatReport) -> dict[str, Any]:
        """Export report to dictionary."""
        return report.to_dict()
    
    @staticmethod
    def to_json(report: ThreatReport) -> str:
        """Export report to JSON string."""
        import json
        return json.dumps(ReportExporter.to_dict(report), indent=2)
    
    @staticmethod
    def to_summary(report: ThreatReport) -> dict[str, Any]:
        """Export report summary."""
        return {
            "id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "status": report.status,
            "author": report.author,
            "created_at": report.created_at,
            "indicator_count": len(report.related_indicators),
            "actor_count": len(report.related_actors),
            "malware_count": len(report.related_malware),
            "section_count": len(report.sections),
        }
