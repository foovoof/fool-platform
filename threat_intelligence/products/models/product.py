"""
threat_intelligence/products/models/product.py

Intelligence Product Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.products.models.base import (
    ProductBase,
    Auditable,
    Versionable,
    ProvenanceMixin,
    ConfidenceMixin,
)


@dataclass(frozen=True)
class IntelligenceProduct(ProductBase, Auditable, Versionable):
    """Intelligence Product entity."""
    name: str = ""
    product_type: str = ""
    title: str = ""
    description: str = ""
    summary: str = ""
    status: str = "draft"
    classification: str = "unclassified"
    sensitivity: str = "public"
    audience: tuple[str, ...] = field(default_factory=tuple)
    author: str = ""
    created_at: str = ""
    published_at: str = ""
    valid_until: str = ""
    superseded_by: str = ""
    parent_product_id: str = ""
    indicator_refs: tuple[str, ...] = field(default_factory=tuple)
    observable_refs: tuple[str, ...] = field(default_factory=tuple)
    actor_refs: tuple[str, ...] = field(default_factory=tuple)
    campaign_refs: tuple[str, ...] = field(default_factory=tuple)
    malware_refs: tuple[str, ...] = field(default_factory=tuple)
    infrastructure_refs: tuple[str, ...] = field(default_factory=tuple)
    vulnerability_refs: tuple[str, ...] = field(default_factory=tuple)
    ttp_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    assertion_refs: tuple[str, ...] = field(default_factory=tuple)
    knowledge_refs: tuple[str, ...] = field(default_factory=tuple)
    inference_refs: tuple[str, ...] = field(default_factory=tuple)
    related_products: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    governance_status: str = "draft"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "product_type": self.product_type,
            "title": self.title,
            "description": self.description,
            "summary": self.summary,
            "status": self.status,
            "classification": self.classification,
            "sensitivity": self.sensitivity,
            "audience": list(self.audience),
            "author": self.author,
            "published_at": self.published_at,
            "valid_until": self.valid_until,
            "superseded_by": self.superseded_by,
            "parent_product_id": self.parent_product_id,
            "indicator_refs": list(self.indicator_refs),
            "observable_refs": list(self.observable_refs),
            "actor_refs": list(self.actor_refs),
            "campaign_refs": list(self.campaign_refs),
            "malware_refs": list(self.malware_refs),
            "infrastructure_refs": list(self.infrastructure_refs),
            "vulnerability_refs": list(self.vulnerability_refs),
            "ttp_refs": list(self.ttp_refs),
            "evidence_refs": list(self.evidence_refs),
            "assertion_refs": list(self.assertion_refs),
            "knowledge_refs": list(self.knowledge_refs),
            "inference_refs": list(self.inference_refs),
            "related_products": list(self.related_products),
            "tags": list(self.tags),
            "governance_status": self.governance_status,
        })
        return base


@dataclass(frozen=True)
class ThreatReport(ProductBase, Auditable, Versionable):
    """Threat Report."""
    product_id: str = ""
    report_type: str = ""
    title: str = ""
    executive_summary: str = ""
    threat_actor_refs: tuple[str, ...] = field(default_factory=tuple)
    malware_refs: tuple[str, ...] = field(default_factory=tuple)
    indicator_refs: tuple[str, ...] = field(default_factory=tuple)
    ttp_refs: tuple[str, ...] = field(default_factory=tuple)
    campaign_refs: tuple[str, ...] = field(default_factory=tuple)
    recommendations: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "report_type": self.report_type,
            "title": self.title,
            "executive_summary": self.executive_summary,
            "threat_actor_refs": list(self.threat_actor_refs),
            "malware_refs": list(self.malware_refs),
            "indicator_refs": list(self.indicator_refs),
            "ttp_refs": list(self.ttp_refs),
            "campaign_refs": list(self.campaign_refs),
            "recommendations": self.recommendations,
        })
        return base


@dataclass(frozen=True)
class TechnicalReport(ProductBase, Auditable, Versionable):
    """Technical Report."""
    product_id: str = ""
    title: str = ""
    technical_summary: str = ""
    indicator_refs: tuple[str, ...] = field(default_factory=tuple)
    observable_refs: tuple[str, ...] = field(default_factory=tuple)
    malware_refs: tuple[str, ...] = field(default_factory=tuple)
    infrastructure_refs: tuple[str, ...] = field(default_factory=tuple)
    detection_rules: str = ""
    ioc_list: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "title": self.title,
            "technical_summary": self.technical_summary,
            "indicator_refs": list(self.indicator_refs),
            "observable_refs": list(self.observable_refs),
            "malware_refs": list(self.malware_refs),
            "infrastructure_refs": list(self.infrastructure_refs),
            "detection_rules": self.detection_rules,
            "ioc_list": self.ioc_list,
        })
        return base


@dataclass(frozen=True)
class StrategicReport(ProductBase, Auditable, Versionable):
    """Strategic Report."""
    product_id: str = ""
    title: str = ""
    strategic_summary: str = ""
    risk_assessment: str = ""
    trend_analysis: str = ""
    business_impact: str = ""
    recommendations: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "title": self.title,
            "strategic_summary": self.strategic_summary,
            "risk_assessment": self.risk_assessment,
            "trend_analysis": self.trend_analysis,
            "business_impact": self.business_impact,
            "recommendations": self.recommendations,
        })
        return base


@dataclass(frozen=True)
class OperationalReport(ProductBase, Auditable, Versionable):
    """Operational Report."""
    product_id: str = ""
    title: str = ""
    operational_summary: str = ""
    ongoing_campaign_refs: tuple[str, ...] = field(default_factory=tuple)
    actor_refs: tuple[str, ...] = field(default_factory=tuple)
    infrastructure_refs: tuple[str, ...] = field(default_factory=tuple)
    current_operations: str = ""
    operational_recommendations: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "title": self.title,
            "operational_summary": self.operational_summary,
            "ongoing_campaign_refs": list(self.ongoing_campaign_refs),
            "actor_refs": list(self.actor_refs),
            "infrastructure_refs": list(self.infrastructure_refs),
            "current_operations": self.current_operations,
            "operational_recommendations": self.operational_recommendations,
        })
        return base


@dataclass(frozen=True)
class TacticalReport(ProductBase, Auditable, Versionable):
    """Tactical Report."""
    product_id: str = ""
    title: str = ""
    tactical_summary: str = ""
    indicator_refs: tuple[str, ...] = field(default_factory=tuple)
    detection_rules: str = ""
    mitigation_actions: str = ""
    ttp_refs: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "title": self.title,
            "tactical_summary": self.tactical_summary,
            "indicator_refs": list(self.indicator_refs),
            "detection_rules": self.detection_rules,
            "mitigation_actions": self.mitigation_actions,
            "ttp_refs": list(self.ttp_refs),
        })
        return base


@dataclass(frozen=True)
class ExecutiveSummary(ProductBase, Auditable, Versionable):
    """Executive Summary."""
    product_id: str = ""
    title: str = ""
    key_findings: tuple[str, ...] = field(default_factory=tuple)
    risk_level: str = ""
    business_impact: str = ""
    strategic_recommendations: tuple[str, ...] = field(default_factory=tuple)
    related_reports: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "title": self.title,
            "key_findings": list(self.key_findings),
            "risk_level": self.risk_level,
            "business_impact": self.business_impact,
            "strategic_recommendations": list(self.strategic_recommendations),
            "related_reports": list(self.related_reports),
        })
        return base


@dataclass(frozen=True)
class ProductMetadata(ProductBase):
    """Product metadata."""
    product_id: str = ""
    metadata_type: str = ""
    key: str = ""
    value: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "metadata_type": self.metadata_type,
            "key": self.key,
            "value": self.value,
        })
        return base
