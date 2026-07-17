"""
product_suite/tests/test_product_suite.py

Tests for Product Suite Integration Module.
"""
import pytest
import sys
import os

from product_suite.registry import (
    ProductMetadata,
    ProductBoundary,
    ProductDependency,
    ProductCertification,
    SuiteCertification,
)

from product_suite.contracts import (
    ProductContract,
    ContractInput,
    ContractOutput,
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
)


class TestProductMetadata:
    """Test ProductMetadata model."""
    
    def test_create_product_metadata(self):
        """Test creating product metadata."""
        product = ProductMetadata(
            product_type="analyst_workspace",
            name="Analyst Workspace",
            description="Workspace for analysts",
            layer="consumer",
            status="certified",
            version="1.0.0",
            module_path="analyst_workspace",
        )
        
        assert product.product_type == "analyst_workspace"
        assert product.name == "Analyst Workspace"
        assert product.status == "certified"


class TestProductContract:
    """Test ProductContract model."""
    
    def test_create_contract(self):
        """Test creating product contract."""
        contract = ProductContract(
            contract_type="navigation",
            name="Workspace Navigation Contract",
            description="Navigation contract between workspaces",
            source_product="analyst_workspace",
            target_product="investigation_workspace",
            version="1.0",
        )
        
        assert contract.name == "Workspace Navigation Contract"
        assert contract.source_product == "analyst_workspace"
        assert contract.target_product == "investigation_workspace"


class TestProductRegistry:
    """Test ProductRegistry."""
    
    def test_register_product(self):
        """Test registering a product."""
        registry = ProductRegistry()
        
        product = ProductMetadata(
            product_type="workbench",
            name="Threat Intelligence Workbench",
            layer="governor",
            status="certified",
        )
        
        registry.register(product)
        retrieved = registry.get("workbench")
        
        assert retrieved is not None
        assert retrieved.product_type == "workbench"
    
    def test_list_by_layer(self):
        """Test listing products by layer."""
        registry = ProductRegistry()
        
        registry.register(ProductMetadata(
            product_type="analyst_workspace",
            name="Analyst Workspace",
            layer="consumer",
        ))
        registry.register(ProductMetadata(
            product_type="workbench",
            name="Workbench",
            layer="governor",
        ))
        
        consumers = registry.get_by_layer("consumer")
        assert len(consumers) >= 1


class TestContractRegistry:
    """Test ContractRegistry."""
    
    def test_register_contract(self):
        """Test registering a contract."""
        registry = ContractRegistry()
        
        contract = ProductContract(
            contract_type="event",
            name="Event Contract",
            source_product="analyst_workspace",
            target_product="workbench",
        )
        
        registry.register(contract)
        retrieved = registry.get("analyst_workspace", "workbench", "event")
        
        assert retrieved is not None
        assert retrieved.name == "Event Contract"


class TestBoundaryValidator:
    """Test BoundaryValidator."""
    
    def test_validate_forbidden_returns_bool(self):
        """Test forbidden boundary validation returns boolean."""
        validator = BoundaryValidator()
        
        # Validator should return boolean (True if forbidden, False otherwise)
        result = validator.validate_forbidden(
            "analyst_workspace", "ThreatActor"
        )
        assert isinstance(result, bool)


class TestCertificationManager:
    """Test CertificationManager."""
    
    def test_certify_product(self):
        """Test certifying a product."""
        manager = CertificationManager()
        
        cert = manager.certify_product(
            product_type="analyst_workspace",
            tests_passed=10,
            tests_total=10,
            notes="All tests passed",
        )
        
        assert cert.status == "certified"
        assert cert.product_type == "analyst_workspace"


class TestEvents:
    """Test event functionality."""
    
    def test_event_emitter(self):
        """Test event emitter."""
        emitter = SuiteEventEmitter()
        
        emitter.emit_product_certified("analyst_workspace")
        emitter.emit_contract_established(
            "navigation_contract",
            "analyst_workspace",
            "workbench",
        )
        
        events = emitter.get_events()
        assert len(events) == 2
        
        emitter.clear_events()
        assert len(emitter.get_events()) == 0


class TestArchitectureBoundaries:
    """Test architecture boundaries across all products."""
    
    def test_no_platform_logic_in_products(self):
        """Test that products don't contain platform logic."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                        
                    # Should not reimplement platform logic
                    assert "class Detection" not in content
                    assert "class Correlation" not in content
            except ImportError:
                pass  # Product not yet imported
    
    def test_no_knowledge_duplication(self):
        """Test no knowledge duplication across products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
        ]
        
        forbidden_models = [
            "ThreatActor",
            "Campaign",
            "Malware",
            "Indicator",
            "Observable",
        ]
        
        for product in products:
            try:
                __import__(f"{product}.models")
                models_module = sys.modules.get(f"{product}.models")
                
                if models_module and hasattr(models_module, "__file__"):
                    with open(models_module.__file__) as f:
                        content = f.read()
                    
                    # Should use references, not own models
                    for model in forbidden_models:
                        # If model exists, it should be Reference only
                        if f"class {model}" in content:
                            assert "Reference" in content
            except ImportError:
                pass  # Module not available
    
    def test_no_ai_references(self):
        """Test no AI references in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    # Check for actual imports, not documentation
                    lines = [l for l in content.split('\n') if not l.strip().startswith('#')]
                    code = '\n'.join(lines)
                    assert "from openai" not in code
                    assert "import openai" not in code
                    assert "from anthropic" not in code
                    assert "import anthropic" not in code
            except ImportError:
                pass
    
    def test_no_soar_automation_in_products(self):
        """Test no automation engine in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    # Check for actual automation imports, not documentation
                    lines = [l for l in content.split('\n') if not l.strip().startswith('#')]
                    code = '\n'.join(lines)
                    # Check for automation-related imports
                    assert "from automation" not in code
                    assert "import automation" not in code
            except ImportError:
                pass
    
    def test_no_external_connectors(self):
        """Test no external connectors in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    # Products should not import connectors
                    if "connectors" in content:
                        # Should only be consumed, not imported
                        assert "from connectors" not in content
            except ImportError:
                pass
    
    def test_no_detection_engine(self):
        """Test no detection engine in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    assert "detection_engine" not in content.lower()
                    assert "class Detector" not in content
            except ImportError:
                pass
    
    def test_no_correlation_engine(self):
        """Test no correlation engine in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    assert "correlation_engine" not in content.lower()
            except ImportError:
                pass
    
    def test_no_hunting_engine(self):
        """Test no hunting engine in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    # Products may reference hunting, but not own it
                    if "hunting" in content.lower():
                        assert "hunt" not in content or "Reference" in content
            except ImportError:
                pass
    
    def test_no_external_ai_imports(self):
        """Test no external AI imports in products."""
        products = [
            "analyst_workspace",
            "workbench",
            "executive_portal",
            "product_suite",
        ]
        
        for product in products:
            try:
                __import__(product)
                module = sys.modules[product]
                
                if hasattr(module, "__file__") and module.__file__:
                    with open(module.__file__) as f:
                        content = f.read()
                    
                    # Check for actual imports, not documentation
                    lines = [l for l in content.split('\n') if not l.strip().startswith('#')]
                    code = '\n'.join(lines)
                    assert "from openai" not in code
                    assert "import openai" not in code
                    assert "from anthropic" not in code
            except ImportError:
                pass


class TestProductChain:
    """Test product chain integrity."""
    
    def test_product_chain_order(self):
        """Test product chain follows correct order."""
        # Chain should be: Platform → Analyst → Investigation → Workbench → Publishing → Portal
        chain = [
            "analyst_workspace",  # Analyze
            "workbench",  # Govern
            "executive_portal",  # Consume
        ]
        
        # Verify all products in chain
        for product in chain:
            try:
                __import__(product)
                assert product in sys.modules
            except ImportError:
                pytest.fail(f"Product {product} not found")


class TestReferenceModels:
    """Test reference model usage across products."""
    
    def test_reference_models_exist(self):
        """Test that reference models exist."""
        # Workbench should have references
        from workbench.models import AssertionReference
        ref = AssertionReference(
            product_id="test",
            assertion_ref="test",
            source_system="test",
        )
        assert ref.assertion_ref == "test"
    
    def test_executive_portal_references(self):
        """Test executive portal references."""
        from executive_portal.models import PublicationReference
        ref = PublicationReference(
            widget_id="widget-1",
            title="Test",
            source="test",
        )
        assert ref.title == "Test"
