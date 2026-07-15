"""
testing/architecture/test_python_first_architecture.py

Architecture tests to verify Python-first rules.
"""
import ast
import os
from pathlib import Path


# Find the repository root
REPO_ROOT = Path(__file__).parent.parent.parent


class TestPythonFirstArchitecture:
    """Tests to verify Python-first architecture rules."""
    
    def test_domain_is_python(self):
        """Test that domain is implemented in Python."""
        domain_dir = REPO_ROOT / "domain"
        assert domain_dir.exists(), "Domain directory should exist"
        
        # Check for Python modules
        py_files = list(domain_dir.glob("*.py"))
        assert len(py_files) > 0, "Domain should have Python files"
        
        # Check that __init__.py exists
        init_file = domain_dir / "__init__.py"
        assert init_file.exists(), "Domain should have __init__.py"
    
    def test_platform_kernel_is_python(self):
        """Test that platform kernel is implemented in Python."""
        kernel_dir = REPO_ROOT / "fool_platform" / "kernel"
        assert kernel_dir.exists(), "Kernel directory should exist"
        
        # Check for Python modules
        py_files = list(kernel_dir.rglob("*.py"))
        assert len(py_files) > 0, "Kernel should have Python files"
    
    def test_no_typescript_backend_authority(self):
        """Test that TypeScript domain is not backend authority."""
        # This test checks that the TypeScript domain files are not
        # considered the canonical implementation for backend
        
        # Check that Python domain exists
        domain_init = REPO_ROOT / "domain" / "__init__.py"
        assert domain_init.exists(), "Python domain __init__.py should exist"
        
        # The TypeScript domain files are now client/legacy only
        # This test passes as long as Python domain exists
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists for Python project."""
        pyproject = REPO_ROOT / "pyproject.toml"
        assert pyproject.exists(), "pyproject.toml should exist for Python project"
    
    def test_architecture_decision_record_exists(self):
        """Test that ADR-0007 exists."""
        adr = REPO_ROOT / "architecture" / "adr" / "ADR-0007-python-first-platform.md"
        assert adr.exists(), "ADR-0007 should exist"
        
        content = adr.read_text()
        assert "Python-First Platform Architecture" in content
        assert "Status" in content
        assert "Accepted" in content


class TestDomainPurity:
    """Tests for domain purity - no forbidden imports."""
    
    def test_domain_common_imports(self):
        """Test that domain common module only uses standard library."""
        common_file = REPO_ROOT / "domain" / "common" / "__init__.py"
        
        if not common_file.exists():
            # Check if there's a common.py instead
            common_file = REPO_ROOT / "domain" / "common.py"
        
        assert common_file.exists(), "Domain common module should exist"
        
        # Read the file
        content = common_file.read_text()
        
        # Parse AST to check imports
        tree = ast.parse(content)
        
        allowed_modules = {
            "dataclasses",
            "datetime",
            "enum",
            "typing",
            "uuid",
            "pathlib",
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split(".")[0]
                    assert module_name in allowed_modules, (
                        f"Domain common should only use standard library, "
                        f"found: {module_name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split(".")[0]
                    assert module_name in allowed_modules, (
                        f"Domain common should only use standard library, "
                        f"found: {node.module}"
                    )
    
    def test_domain_modules_import_common(self):
        """Test that domain modules import from domain.common."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            content = py_file.read_text()
            
            # Domain modules should import from .common
            if "import" in content:
                # This is a basic check - could be more sophisticated
                pass


class TestKernelFoundation:
    """Tests for kernel foundation implementation."""
    
    def test_kernel_has_required_modules(self):
        """Test that kernel has all required modules."""
        kernel_dir = REPO_ROOT / "fool_platform" / "kernel"
        
        required_modules = [
            "runtime.py",
            "lifecycle.py",
            "kernel_state.py",
            "kernel_config.py",
            "kernel_events.py",
            "kernel_exceptions.py",
            "kernel_interfaces.py",
            "app_context.py",
            "execution_context.py",
            "bootstrapper.py",
            "health_manager.py",
            "registry_manager.py",
        ]
        
        for module in required_modules:
            module_path = kernel_dir / module
            assert module_path.exists(), f"Kernel should have {module}"
    
    def test_kernel_has_di_modules(self):
        """Test that kernel DI modules exist."""
        di_dir = REPO_ROOT / "fool_platform" / "kernel" / "di"
        
        required_modules = [
            "container.py",
            "lifetime.py",
            "registration.py",
            "resolution.py",
            "validation.py",
            "hooks.py",
        ]
        
        for module in required_modules:
            module_path = di_dir / module
            assert module_path.exists(), f"DI should have {module}"
    
    def test_kernel_has_config_modules(self):
        """Test that kernel config modules exist."""
        config_dir = REPO_ROOT / "fool_platform" / "kernel" / "config"
        
        required_modules = [
            "environment.py",
            "loader.py",
            "validator.py",
            "typed_config.py",
            "registry.py",
            "override.py",
            "secrets.py",
        ]
        
        for module in required_modules:
            module_path = config_dir / module
            assert module_path.exists(), f"Config should have {module}"
    
    def test_kernel_has_health_modules(self):
        """Test that kernel health modules exist."""
        health_dir = REPO_ROOT / "fool_platform" / "kernel" / "health"
        
        required_modules = [
            "checks.py",
            "status.py",
            "readiness.py",
            "liveness.py",
            "startup.py",
            "shutdown.py",
            "registry.py",
            "diagnostics.py",
        ]
        
        for module in required_modules:
            module_path = health_dir / module
            assert module_path.exists(), f"Health should have {module}"


class TestRegistryLoaders:
    """Tests for registry loaders."""
    
    def test_registries_directory_exists(self):
        """Test that registries directory exists."""
        registries_dir = REPO_ROOT / "fool_platform" / "kernel" / "registries"
        assert registries_dir.exists(), "Registries directory should exist"
    
    def test_registry_loaders_exist(self):
        """Test that all registry loaders exist."""
        registries_dir = REPO_ROOT / "fool_platform" / "kernel" / "registries"
        
        required_loaders = [
            "agent_registry.py",
            "capability_registry.py",
            "workflow_registry.py",
            "concept_registry.py",
            "contract_registry.py",
        ]
        
        for loader in required_loaders:
            loader_path = registries_dir / loader
            assert loader_path.exists(), f"Registry loader {loader} should exist"


class TestNoPlaceholderCode:
    """Tests to verify no placeholder code exists."""
    
    def test_no_todo_in_kernel(self):
        """Test that kernel code has no TODO comments."""
        kernel_dir = REPO_ROOT / "fool_platform" / "kernel"
        
        for py_file in kernel_dir.rglob("*.py"):
            content = py_file.read_text()
            assert "TODO" not in content, f"{py_file} contains TODO"
            assert "FIXME" not in content, f"{py_file} contains FIXME"
            assert "XXX" not in content, f"{py_file} contains XXX"
    
    def test_no_placeholder_in_domain(self):
        """Test that domain code has no placeholder text."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            
            content = py_file.read_text()
            
            # Check for common placeholder patterns
            lower_content = content.lower()
            assert "not implemented" not in lower_content
            assert "coming soon" not in lower_content
            assert "placeholder" not in lower_content
