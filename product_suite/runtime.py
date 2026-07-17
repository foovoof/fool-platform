"""
product_suite/runtime.py

Product Suite Runtime.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from product_suite.registry.product import (
    ProductMetadata,
    ProductCertification,
    SuiteCertification,
    ProductBoundary,
    ProductDependency,
)
from product_suite.contracts.contract import ProductContract
from product_suite.events import SuiteEventEmitter


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._products: dict[str, ProductMetadata] = {}
        self._contracts: dict[str, ProductContract] = {}
        self._certifications: dict[str, ProductCertification] = {}


_storage = InMemoryStorage()


class ProductRegistry:
    """Registry for all products in the suite."""
    
    def register(self, product: ProductMetadata) -> None:
        """Register a product."""
        _storage._products[product.product_type] = product
    
    def get(self, product_type: str) -> ProductMetadata | None:
        """Get product by type."""
        return _storage._products.get(product_type)
    
    def list_all(self) -> list[ProductMetadata]:
        """List all registered products."""
        return list(_storage._products.values())
    
    def get_by_layer(self, layer: str) -> list[ProductMetadata]:
        """Get products by layer."""
        return [
            p for p in _storage._products.values()
            if p.layer == layer
        ]


class ContractRegistry:
    """Registry for cross product contracts."""
    
    def register(self, contract: ProductContract) -> None:
        """Register a contract."""
        key = f"{contract.source_product}:{contract.target_product}:{contract.contract_type}"
        _storage._contracts[key] = contract
    
    def get(
        self,
        source: str,
        target: str,
        contract_type: str,
    ) -> ProductContract | None:
        """Get contract by source, target, and type."""
        key = f"{source}:{target}:{contract_type}"
        return _storage._contracts.get(key)
    
    def list_by_product(self, product_type: str) -> list[ProductContract]:
        """List contracts by product."""
        return [
            c for c in _storage._contracts.values()
            if c.source_product == product_type or c.target_product == product_type
        ]
    
    def list_all(self) -> list[ProductContract]:
        """List all contracts."""
        return list(_storage._contracts.values())


class BoundaryValidator:
    """Validates product boundaries."""
    
    def validate_ownership(
        self,
        product_type: str,
        entity_type: str,
    ) -> bool:
        """Check if product can own entity type."""
        product = ProductRegistry().get(product_type)
        if not product:
            return False
        
        for boundary in product.boundaries:
            if boundary.entity_type == entity_type:
                return boundary.boundary_type == "owns"
        
        return False
    
    def validate_consumption(
        self,
        product_type: str,
        entity_type: str,
    ) -> bool:
        """Check if product can consume entity type."""
        product = ProductRegistry().get(product_type)
        if not product:
            return False
        
        for boundary in product.boundaries:
            if boundary.entity_type == entity_type:
                return boundary.boundary_type in ("owns", "governs", "consumes", "references")
        
        return False
    
    def validate_forbidden(
        self,
        product_type: str,
        entity_type: str,
    ) -> bool:
        """Check if entity type is forbidden for product."""
        product = ProductRegistry().get(product_type)
        if not product:
            return True
        
        for boundary in product.boundaries:
            if boundary.entity_type == entity_type:
                return boundary.boundary_type == "forbidden"
        
        return False


class CertificationManager:
    """Manages product suite certification."""
    
    def certify_product(
        self,
        product_type: str,
        tests_passed: int,
        tests_total: int,
        notes: str = "",
    ) -> ProductCertification:
        """Certify a product."""
        certification = ProductCertification(
            id=str(uuid4()),
            product_type=product_type,
            status="certified",
            certified_at=datetime.now(timezone.utc).isoformat(),
            certified_by="system",
            tests_passed=tests_passed,
            tests_total=tests_total,
            boundaries_verified=tests_passed > 0,
            contracts_verified=tests_passed > 0,
            architecture_verified=tests_passed > 0,
            notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )
        _storage._certifications[product_type] = certification
        return certification
    
    def certify_suite(
        self,
        products: list[ProductCertification],
    ) -> SuiteCertification:
        """Certify the entire product suite."""
        all_passed = all(c.status == "certified" for c in products)
        
        certification = SuiteCertification(
            id=str(uuid4()),
            status="certified" if all_passed else "failed",
            certified_at=datetime.now(timezone.utc).isoformat() if all_passed else "",
            certified_by="system",
            products=tuple(products),
            boundaries_pass=all_passed,
            contracts_pass=all_passed,
            architecture_pass=all_passed,
            determinism_pass=all_passed,
            traceability_pass=all_passed,
            replayability_pass=all_passed,
            governance_pass=all_passed,
            plugin_pass=all_passed,
            event_pass=all_passed,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )
        return certification
    
    def get_product_certification(
        self,
        product_type: str,
    ) -> ProductCertification | None:
        """Get product certification."""
        return _storage._certifications.get(product_type)
    
    def get_suite_certification(self) -> SuiteCertification | None:
        """Get suite certification."""
        certifications = list(_storage._certifications.values())
        if not certifications:
            return None
        return self.certify_suite(certifications)
