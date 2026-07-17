"""
product_suite/registry/product.py

Product Registry Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from product_suite.registry.base import SuiteBase
from product_suite.registry.enums import (
    ProductType,
    ProductLayer,
    ProductStatus,
    ProductCapability,
)


@dataclass(frozen=True)
class ProductDependency:
    """Product dependency."""
    product_type: str = ""
    min_version: str = ""
    max_version: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "product_type": self.product_type,
            "min_version": self.min_version,
            "max_version": self.max_version,
        }


@dataclass(frozen=True)
class ProductBoundary:
    """Product boundary definition."""
    entity_type: str = ""
    boundary_type: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "boundary_type": self.boundary_type,
            "description": self.description,
        }


@dataclass(frozen=True)
class ProductCapability:
    """Product capability."""
    capability: str = ""
    description: str = ""
    consumes: tuple[str, ...] = field(default_factory=tuple)
    produces: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "capability": self.capability,
            "description": self.description,
            "consumes": list(self.consumes),
            "produces": list(self.produces),
        }


@dataclass(frozen=True)
class ProductMetadata(SuiteBase):
    """Product metadata."""
    product_type: str = ""
    name: str = ""
    description: str = ""
    layer: str = ""
    status: str = "draft"
    version: str = "1.0.0"
    module_path: str = ""
    dependencies: tuple[ProductDependency, ...] = field(default_factory=tuple)
    boundaries: tuple[ProductBoundary, ...] = field(default_factory=tuple)
    capabilities: tuple[ProductCapability, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_type": self.product_type,
            "name": self.name,
            "description": self.description,
            "layer": self.layer,
            "status": self.status,
            "version": self.version,
            "module_path": self.module_path,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "boundaries": [b.to_dict() for b in self.boundaries],
            "capabilities": [c.to_dict() for c in self.capabilities],
        })
        return base


@dataclass(frozen=True)
class ProductVersionMatrix(SuiteBase):
    """Product version compatibility matrix."""
    product_type: str = ""
    versions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    compatibility: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_type": self.product_type,
            "versions": list(self.versions),
            "compatibility": list(self.compatibility),
        })
        return base


@dataclass(frozen=True)
class ProductCertification(SuiteBase):
    """Product certification record."""
    product_type: str = ""
    status: str = "pending"
    certified_at: str = ""
    certified_by: str = ""
    tests_passed: int = 0
    tests_total: int = 0
    boundaries_verified: bool = False
    contracts_verified: bool = False
    architecture_verified: bool = False
    notes: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "product_type": self.product_type,
            "status": self.status,
            "certified_at": self.certified_at,
            "certified_by": self.certified_by,
            "tests_passed": self.tests_passed,
            "tests_total": self.tests_total,
            "boundaries_verified": self.boundaries_verified,
            "contracts_verified": self.contracts_verified,
            "architecture_verified": self.architecture_verified,
            "notes": self.notes,
        })
        return base


@dataclass(frozen=True)
class SuiteCertification(SuiteBase):
    """Product suite certification."""
    status: str = "pending"
    certified_at: str = ""
    certified_by: str = ""
    products: tuple[ProductCertification, ...] = field(default_factory=tuple)
    boundaries_pass: bool = False
    contracts_pass: bool = False
    architecture_pass: bool = False
    determinism_pass: bool = False
    traceability_pass: bool = False
    replayability_pass: bool = False
    governance_pass: bool = False
    plugin_pass: bool = False
    event_pass: bool = False
    notes: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "status": self.status,
            "certified_at": self.certified_at,
            "certified_by": self.certified_by,
            "products": [p.to_dict() for p in self.products],
            "boundaries_pass": self.boundaries_pass,
            "contracts_pass": self.contracts_pass,
            "architecture_pass": self.architecture_pass,
            "determinism_pass": self.determinism_pass,
            "traceability_pass": self.traceability_pass,
            "replayability_pass": self.replayability_pass,
            "governance_pass": self.governance_pass,
            "plugin_pass": self.plugin_pass,
            "event_pass": self.event_pass,
            "notes": self.notes,
        })
        return base
