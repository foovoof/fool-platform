"""
product_suite/__init__.py

Product Suite Integration Module.

Phase 8F - Product Suite Integration & Certification Foundation.

ARCHITECTURAL PRINCIPLES:
1. Platform Owns Capabilities
2. Products Orchestrate Capabilities
3. Products Never Reimplement Platform Logic
4. Reference, Never Copy
5. Govern, Never Own
6. Publish, Never Produce
7. Consume, Never Mutate
8. Contracts Before Implementations
9. Deterministic Before Intelligent
10. Certification Before Expansion

PRODUCT CHAIN:
Platform → owns intelligence
Analyst Workspace → Analyze
Investigation Workspace → Investigate
Threat Intelligence Workbench → Govern
Publishing → Publish
Executive Portal → Consume
"""
from product_suite.registry import (
    ProductType,
    ProductLayer,
    ProductStatus,
    ProductCapability,
    ProductBoundaryType,
    ContractType,
    CompatibilityLevel,
    SuiteBase,
    ProductMetadata,
    ProductDependency,
    ProductBoundary,
    ProductCertification,
    SuiteCertification,
)

from product_suite.contracts import (
    ContractInput,
    ContractOutput,
    ContractEvent,
    ContractReference,
    ReplayRule,
    ProductContract,
    ContractCompatibilityMatrix,
)

from product_suite.runtime import (
    ProductRegistry,
    ContractRegistry,
    BoundaryValidator,
    CertificationManager,
)

from product_suite.events import (
    SuiteEventEmitter,
    SuiteEventType,
    SuiteEvent,
)

__all__ = [
    # Enums
    "ProductType",
    "ProductLayer",
    "ProductStatus",
    "ProductCapability",
    "ProductBoundaryType",
    "ContractType",
    "CompatibilityLevel",
    # Base
    "SuiteBase",
    # Registry
    "ProductMetadata",
    "ProductDependency",
    "ProductBoundary",
    "ProductCertification",
    "SuiteCertification",
    # Contracts
    "ContractInput",
    "ContractOutput",
    "ContractEvent",
    "ContractReference",
    "ReplayRule",
    "ProductContract",
    "ContractCompatibilityMatrix",
    # Runtime
    "ProductRegistry",
    "ContractRegistry",
    "BoundaryValidator",
    "CertificationManager",
    # Events
    "SuiteEventEmitter",
    "SuiteEventType",
    "SuiteEvent",
]
