"""
product_suite/registry/enums.py

Product Suite Enums.
"""
from __future__ import annotations

from enum import Enum


class ProductType(Enum):
    """Product types in the suite."""
    ANALYST_WORKSPACE = "analyst_workspace"
    INVESTIGATION_WORKSPACE = "investigation_workspace"
    THREAT_INTELLIGENCE_WORKBENCH = "workbench"
    PUBLISHING = "publishing"
    EXECUTIVE_PORTAL = "executive_portal"


class ProductLayer(Enum):
    """Product layer classification."""
    CONSUMER = "consumer"  # Consumes platform capabilities
    ORCHESTRATOR = "orchestrator"  # Orchestrates platform capabilities
    GOVERNOR = "governor"  # Governs platform assets


class ProductStatus(Enum):
    """Product lifecycle status."""
    DRAFT = "draft"
    CERTIFIED = "certified"
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class ProductCapability(Enum):
    """Product capabilities."""
    ANALYZE = "analyze"
    INVESTIGATE = "investigate"
    GOVERN = "govern"
    PUBLISH = "publish"
    CONSUME = "consume"
    ORCHESTRATE = "orchestrate"


class ProductBoundaryType(Enum):
    """Boundary types."""
    OWNS = "owns"  # Entity ownership
    GOVERNS = "governs"  # Governance rights
    CONSUMES = "consumes"  # Consumption rights
    REFERENCES = "references"  # Reference only
    FORBIDDEN = "forbidden"  # Prohibited


class ContractType(Enum):
    """Contract types between products."""
    NAVIGATION = "navigation"
    CONTEXT = "context"
    EVENT = "event"
    REFERENCE = "reference"
    COMMAND = "command"


class CompatibilityLevel(Enum):
    """Compatibility levels."""
    FULL = "full"  # Fully compatible
    PARTIAL = "partial"  # Partially compatible
    INCOMPATIBLE = "incompatible"  # Not compatible
