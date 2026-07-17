"""
product_suite/registry/__init__.py

Registry Module.
"""
from product_suite.registry.enums import (
    ProductType,
    ProductLayer,
    ProductStatus,
    ProductCapability,
    ProductBoundaryType,
    ContractType,
    CompatibilityLevel,
)

from product_suite.registry.base import SuiteBase

from product_suite.registry.product import (
    ProductMetadata,
    ProductDependency,
    ProductBoundary,
    ProductCapability,
    ProductVersionMatrix,
    ProductCertification,
    SuiteCertification,
)

__all__ = [
    "ProductType",
    "ProductLayer",
    "ProductStatus",
    "ProductCapability",
    "ProductBoundaryType",
    "ContractType",
    "CompatibilityLevel",
    "SuiteBase",
    "ProductMetadata",
    "ProductDependency",
    "ProductBoundary",
    "ProductCapability",
    "ProductVersionMatrix",
    "ProductCertification",
    "SuiteCertification",
]
