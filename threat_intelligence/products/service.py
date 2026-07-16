"""
threat_intelligence/products/service.py

Intelligence Products Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.products.models import (
    IntelligenceProduct,
    ProductAssertion,
    ProductEvidence,
    ProductConfidence,
    ProductProvenance,
    ProductVersion,
    ProductHistory,
    LifecycleState,
    LifecycleTransition,
    ApprovalRecord,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._products: dict[str, IntelligenceProduct] = {}
        self._assertions: dict[str, ProductAssertion] = {}
        self._evidence: dict[str, ProductEvidence] = {}
        self._confidence: dict[str, ProductConfidence] = {}
        self._provenance: dict[str, ProductProvenance] = {}
        self._versions: dict[str, ProductVersion] = {}
        self._histories: dict[str, ProductHistory] = {}
        self._lifecycle: dict[str, LifecycleState] = {}
        self._approvals: dict[str, ApprovalRecord] = {}


_storage = InMemoryStorage()


class ProductService:
    """Service for managing intelligence products."""
    
    def create(
        self,
        name: str,
        product_type: str,
        title: str,
        author: str = "",
        **kwargs: Any,
    ) -> IntelligenceProduct:
        """Create new product."""
        product = IntelligenceProduct(
            id=str(uuid4()),
            name=name,
            product_type=product_type,
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        _storage._products[product.id] = product
        return product
    
    def get(self, product_id: str) -> IntelligenceProduct | None:
        """Get product by ID."""
        return _storage._products.get(product_id)
    
    def update(self, product: IntelligenceProduct) -> IntelligenceProduct:
        """Update product."""
        updated = IntelligenceProduct(
            id=product.id,
            name=product.name,
            product_type=product.product_type,
            title=product.title,
            description=product.description,
            summary=product.summary,
            status=product.status,
            classification=product.classification,
            sensitivity=product.sensitivity,
            audience=product.audience,
            author=product.author,
            created_at=product.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=product.created_by,
            modified_by=product.modified_by,
            version=product.version + 1,
            metadata=product.metadata,
            published_at=product.published_at,
            valid_until=product.valid_until,
            superseded_by=product.superseded_by,
            parent_product_id=product.parent_product_id,
            indicator_refs=product.indicator_refs,
            observable_refs=product.observable_refs,
            actor_refs=product.actor_refs,
            campaign_refs=product.campaign_refs,
            malware_refs=product.malware_refs,
            infrastructure_refs=product.infrastructure_refs,
            vulnerability_refs=product.vulnerability_refs,
            ttp_refs=product.ttp_refs,
            evidence_refs=product.evidence_refs,
            assertion_refs=product.assertion_refs,
            knowledge_refs=product.knowledge_refs,
            inference_refs=product.inference_refs,
            related_products=product.related_products,
            tags=product.tags,
            governance_status=product.governance_status,
        )
        _storage._products[updated.id] = updated
        return updated
    
    def delete(self, product_id: str) -> bool:
        """Delete product."""
        if product_id in _storage._products:
            del _storage._products[product_id]
            return True
        return False
    
    def list_all(self) -> list[IntelligenceProduct]:
        """List all products."""
        return list(_storage._products.values())
    
    def search(self, query: dict[str, Any]) -> list[IntelligenceProduct]:
        """Search products."""
        results = []
        for product in _storage._products.values():
            if self._matches_query(product, query):
                results.append(product)
        return results
    
    def _matches_query(self, product: IntelligenceProduct, query: dict[str, Any]) -> bool:
        """Check if product matches query."""
        for key, value in query.items():
            product_value = getattr(product, key, None)
            if product_value is None:
                return False
            if isinstance(value, (list, tuple)):
                if product_value not in value:
                    return False
            elif product_value != value:
                return False
        return True
    
    def find_by_type(self, product_type: str) -> list[IntelligenceProduct]:
        """Find by type."""
        return self.search({"product_type": product_type})
    
    def find_by_status(self, status: str) -> list[IntelligenceProduct]:
        """Find by status."""
        return self.search({"status": status})
    
    def find_by_author(self, author: str) -> list[IntelligenceProduct]:
        """Find by author."""
        return self.search({"author": author})
    
    def find_by_actor(self, actor_id: str) -> list[IntelligenceProduct]:
        """Find by actor reference."""
        return self.search({"actor_refs": actor_id})
    
    def find_by_campaign(self, campaign_id: str) -> list[IntelligenceProduct]:
        """Find by campaign reference."""
        return self.search({"campaign_refs": campaign_id})
    
    def find_by_malware(self, malware_id: str) -> list[IntelligenceProduct]:
        """Find by malware reference."""
        return self.search({"malware_refs": malware_id})
    
    def find_by_indicator(self, indicator_id: str) -> list[IntelligenceProduct]:
        """Find by indicator reference."""
        return self.search({"indicator_refs": indicator_id})
    
    def find_by_ttp(self, ttp_id: str) -> list[IntelligenceProduct]:
        """Find by TTP reference."""
        return self.search({"ttp_refs": ttp_id})
    
    def count(self) -> int:
        """Count products."""
        return len(_storage._products)


class LifecycleService:
    """Service for managing product lifecycle."""
    
    VALID_TRANSITIONS: dict[str, list[str]] = {
        "draft": ["under_review", "archived"],
        "under_review": ["validated", "draft", "archived"],
        "validated": ["approved", "under_review", "archived"],
        "approved": ["published", "archived"],
        "published": ["superseded", "deprecated", "archived"],
        "superseded": ["deprecated", "archived"],
        "deprecated": ["archived"],
        "archived": [],
    }
    
    def __init__(self) -> None:
        self._states: dict[str, LifecycleState] = {}
    
    def get_lifecycle(self, product_id: str) -> LifecycleState | None:
        """Get lifecycle for product."""
        return self._states.get(product_id)
    
    def can_transition(self, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        valid_targets = self.VALID_TRANSITIONS.get(from_status, [])
        return to_status in valid_targets
    
    def transition(
        self,
        product_id: str,
        to_status: str,
        reason: str = "",
        transitioned_by: str = "",
    ) -> tuple[bool, str]:
        """
        Attempt a status transition.
        
        Returns:
            Tuple of (success, message)
        """
        lifecycle = self._states.get(product_id)
        
        if not lifecycle:
            lifecycle = LifecycleState(
                product_id=product_id,
                status="draft",
            )
            self._states[product_id] = lifecycle
        
        from_status = lifecycle.status
        
        if not self.can_transition(from_status, to_status):
            return (False, f"Cannot transition from {from_status} to {to_status}")
        
        transition = LifecycleTransition(
            product_id=product_id,
            from_status=from_status,
            to_status=to_status,
            reason=reason,
            transitioned_by=transitioned_by,
        )
        
        updated_transitions = list(lifecycle.transitions) + [transition.to_dict()]
        
        updated_lifecycle = LifecycleState(
            product_id=product_id,
            status=to_status,
            transitions=tuple(updated_transitions),
            last_reviewed=lifecycle.last_reviewed,
            next_review=lifecycle.next_review,
        )
        
        self._states[product_id] = updated_lifecycle
        
        return (True, f"Transitioned from {from_status} to {to_status}")
    
    def get_status(self, product_id: str) -> str | None:
        """Get current status."""
        lifecycle = self._states.get(product_id)
        return lifecycle.status if lifecycle else None
    
    def get_transition_history(self, product_id: str) -> list[dict[str, Any]]:
        """Get transition history."""
        lifecycle = self._states.get(product_id)
        if not lifecycle:
            return []
        return list(lifecycle.transitions)
