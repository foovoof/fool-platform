"""
threat_intelligence/products/validation.py

Intelligence Products Validation.
"""
from __future__ import annotations

from dataclasses import dataclass

from threat_intelligence.products.models import IntelligenceProduct


@dataclass
class ValidationResult:
    """Validation result."""
    is_valid: bool = True
    issues: list[str] = None
    
    def __post_init__(self) -> None:
        if self.issues is None:
            self.issues = []
    
    def add_issue(self, issue: str) -> None:
        """Add a validation issue."""
        self.is_valid = False
        self.issues.append(issue)


class ProductValidator:
    """Validator for intelligence products."""
    
    @staticmethod
    def validate(product: IntelligenceProduct) -> ValidationResult:
        """Validate product."""
        result = ValidationResult()
        
        if not product.name:
            result.add_issue("Product name is required")
        
        if not product.product_type:
            result.add_issue("Product type is required")
        
        if not product.title:
            result.add_issue("Product title is required")
        
        return result


class StructureValidator:
    """Validator for product structure."""
    
    @staticmethod
    def validate(product: IntelligenceProduct) -> ValidationResult:
        """Validate product structure."""
        result = ValidationResult()
        
        if not product.id:
            result.add_issue("Product ID is required")
        
        if product.version < 1:
            result.add_issue("Product version must be >= 1")
        
        return result


class LifecycleValidator:
    """Validator for lifecycle transitions."""
    
    VALID_TRANSITIONS = {
        "draft": ["under_review", "archived"],
        "under_review": ["validated", "draft", "archived"],
        "validated": ["approved", "under_review", "archived"],
        "approved": ["published", "archived"],
        "published": ["superseded", "deprecated", "archived"],
        "superseded": ["deprecated", "archived"],
        "deprecated": ["archived"],
        "archived": [],
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        valid_targets = cls.VALID_TRANSITIONS.get(from_status, [])
        return to_status in valid_targets
    
    @classmethod
    def validate_transition(cls, from_status: str, to_status: str) -> ValidationResult:
        """Validate transition."""
        result = ValidationResult()
        
        if not cls.can_transition(from_status, to_status):
            result.add_issue(f"Invalid transition from {from_status} to {to_status}")
        
        return result


class ReferenceValidator:
    """Validator for product references."""
    
    @staticmethod
    def validate_references(product: IntelligenceProduct) -> ValidationResult:
        """Validate product references."""
        result = ValidationResult()
        
        ref_fields = [
            "indicator_refs",
            "observable_refs",
            "actor_refs",
            "campaign_refs",
            "malware_refs",
            "infrastructure_refs",
            "vulnerability_refs",
            "ttp_refs",
            "evidence_refs",
            "assertion_refs",
            "knowledge_refs",
            "inference_refs",
        ]
        
        for field in ref_fields:
            refs = getattr(product, field, ())
            if not isinstance(refs, (list, tuple)):
                result.add_issue(f"{field} must be a list or tuple")
        
        return result


class VersionValidator:
    """Validator for versioning."""
    
    @staticmethod
    def validate_version(version: int) -> ValidationResult:
        """Validate version number."""
        result = ValidationResult()
        
        if version < 1:
            result.add_issue("Version must be >= 1")
        
        return result
    
    @staticmethod
    def parse_version_string(version: str) -> tuple[int, int, int] | None:
        """Parse version string."""
        try:
            parts = version.split(".")
            if len(parts) != 3:
                return None
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, AttributeError):
            return None


class RegistryValidator:
    """Validator for registry values."""
    
    @staticmethod
    def validate_product_type(product_type: str) -> ValidationResult:
        """Validate product type."""
        result = ValidationResult()
        
        valid_types = [
            "threat_report", "technical_report", "strategic_report",
            "operational_report", "tactical_report", "executive_summary",
            "indicator_list", "ioc_bulletin", "ttp_analysis",
            "campaign_report", "threat_actor_profile", "malware_analysis",
            "vulnerability_advisory", "infrastructure_report",
        ]
        
        if product_type and product_type not in valid_types:
            result.add_issue(f"Invalid product type: {product_type}")
        
        return result
    
    @staticmethod
    def validate_classification(classification: str) -> ValidationResult:
        """Validate classification level."""
        result = ValidationResult()
        
        valid_levels = ["unclassified", "internal", "confidential", "secret", "top_secret"]
        if classification and classification not in valid_levels:
            result.add_issue(f"Invalid classification: {classification}")
        
        return result
    
    @staticmethod
    def validate_status(status: str) -> ValidationResult:
        """Validate status."""
        result = ValidationResult()
        
        valid_statuses = [
            "draft", "under_review", "validated", "approved",
            "published", "superseded", "deprecated", "archived",
        ]
        if status and status not in valid_statuses:
            result.add_issue(f"Invalid status: {status}")
        
        return result
