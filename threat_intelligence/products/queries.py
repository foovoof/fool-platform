"""
threat_intelligence/products/queries.py

Intelligence Products Queries.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.products.service import ProductService


class ProductQueryService:
    """Service for querying intelligence products."""
    
    def __init__(self, service: ProductService | None = None) -> None:
        self._service = service or ProductService()
    
    def find_all(self) -> list[dict[str, Any]]:
        """Find all products."""
        results = self._service.list_all()
        return [r.to_dict() for r in results]
    
    def find_by_id(self, product_id: str) -> dict[str, Any] | None:
        """Find by ID."""
        result = self._service.get(product_id)
        return result.to_dict() if result else None
    
    def find_by_type(self, product_type: str) -> list[dict[str, Any]]:
        """Find by product type."""
        results = self._service.find_by_type(product_type)
        return [r.to_dict() for r in results]
    
    def find_by_status(self, status: str) -> list[dict[str, Any]]:
        """Find by status."""
        results = self._service.find_by_status(status)
        return [r.to_dict() for r in results]
    
    def find_by_author(self, author: str) -> list[dict[str, Any]]:
        """Find by author."""
        results = self._service.find_by_author(author)
        return [r.to_dict() for r in results]
    
    def find_by_actor(self, actor_id: str) -> list[dict[str, Any]]:
        """Find by actor reference."""
        results = self._service.find_by_actor(actor_id)
        return [r.to_dict() for r in results]
    
    def find_by_campaign(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find by campaign reference."""
        results = self._service.find_by_campaign(campaign_id)
        return [r.to_dict() for r in results]
    
    def find_by_malware(self, malware_id: str) -> list[dict[str, Any]]:
        """Find by malware reference."""
        results = self._service.find_by_malware(malware_id)
        return [r.to_dict() for r in results]
    
    def find_by_indicator(self, indicator_id: str) -> list[dict[str, Any]]:
        """Find by indicator reference."""
        results = self._service.find_by_indicator(indicator_id)
        return [r.to_dict() for r in results]
    
    def find_by_ttp(self, ttp_id: str) -> list[dict[str, Any]]:
        """Find by TTP reference."""
        results = self._service.find_by_ttp(ttp_id)
        return [r.to_dict() for r in results]
    
    def find_by_infrastructure(self, infra_id: str) -> list[dict[str, Any]]:
        """Find by infrastructure reference."""
        results = self._service.search({"infrastructure_refs": infra_id})
        return [r.to_dict() for r in results]
    
    def find_by_vulnerability(self, vuln_id: str) -> list[dict[str, Any]]:
        """Find by vulnerability reference."""
        results = self._service.search({"vulnerability_refs": vuln_id})
        return [r.to_dict() for r in results]
    
    def find_by_classification(self, classification: str) -> list[dict[str, Any]]:
        """Find by classification."""
        results = self._service.search({"classification": classification})
        return [r.to_dict() for r in results]
    
    def find_by_sensitivity(self, sensitivity: str) -> list[dict[str, Any]]:
        """Find by sensitivity."""
        results = self._service.search({"sensitivity": sensitivity})
        return [r.to_dict() for r in results]
    
    def find_published(self) -> list[dict[str, Any]]:
        """Find published products."""
        return self.find_by_status("published")
    
    def find_drafts(self) -> list[dict[str, Any]]:
        """Find draft products."""
        return self.find_by_status("draft")
    
    def find_by_tag(self, tag: str) -> list[dict[str, Any]]:
        """Find by tag."""
        results = self._service.search({"tags": tag})
        return [r.to_dict() for r in results]
