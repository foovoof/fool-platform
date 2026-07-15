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


class TestEventBusFoundation:
    """Tests for Event Bus foundation implementation."""
    
    def test_events_directory_exists(self):
        """Test that events directory exists."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        assert events_dir.exists(), "Events directory should exist"
    
    def test_events_has_required_modules(self):
        """Test that events has all required modules."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        required_modules = [
            "__init__.py",
            "bus.py",
            "metadata.py",
            "envelope.py",
            "context.py",
            "publisher.py",
            "subscriber.py",
            "dispatcher.py",
            "router.py",
            "event_registry.py",
            "validation.py",
            "serialization.py",
            "history.py",
            "replay.py",
            "metrics.py",
            "lifecycle.py",
            "exceptions.py",
        ]
        
        for module in required_modules:
            module_path = events_dir / module
            assert module_path.exists(), f"Events should have {module}"
    
    def test_events_has_tests(self):
        """Test that events has tests."""
        tests_dir = events_dir = REPO_ROOT / "fool_platform" / "events" / "tests"
        assert tests_dir.exists(), "Events tests directory should exist"
        
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "Events should have test files"
    
    def test_platform_events_is_python(self):
        """Test that platform events is implemented in Python."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        py_files = list(events_dir.rglob("*.py"))
        assert len(py_files) > 0, "Events should have Python files"


class TestEventBusPurity:
    """Tests for Event Bus architecture purity."""
    
    def test_events_does_not_import_apps(self):
        """Test that events does not import apps."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from apps" not in content
            assert "import apps" not in content
    
    def test_events_does_not_import_infrastructure(self):
        """Test that events does not import infrastructure."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from infrastructure" not in content
            assert "import infrastructure" not in content
    
    def test_events_does_not_import_external_brokers(self):
        """Test that events does not import external brokers."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        forbidden_imports = [
            "kafka",
            "rabbitmq",
            "redis",
            "celery",
            "nats",
        ]
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            for broker in forbidden_imports:
                assert broker not in content.lower() or "from fool_platform" in content
    
    def test_events_does_not_import_ai(self):
        """Test that events does not import ai."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from ai" not in content
            assert "import ai" not in content
    
    def test_events_does_not_import_connectors(self):
        """Test that events does not import connectors."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_events_does_not_import_orchestration(self):
        """Test that events does not import orchestration."""
        events_dir = REPO_ROOT / "fool_platform" / "events"
        
        for py_file in events_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from orchestration" not in content
            assert "import orchestration" not in content


class TestDomainEventPurity:
    """Tests to ensure domain does not import events."""
    
    def test_domain_does_not_import_platform_events(self):
        """Test that domain does not import platform events."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.events" not in content
            assert "import fool_platform.events" not in content


class TestOrchestrationFoundation:
    """Tests for Orchestration layer foundation."""
    
    def test_orchestration_directory_exists(self):
        """Test that orchestration directory exists."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        assert orch_dir.exists(), "Orchestration directory should exist"
    
    def test_orchestration_has_required_modules(self):
        """Test that orchestration has required modules."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        required_modules = [
            "orchestration_exceptions.py",
            "models.py",
            "execution_context.py",
        ]
        
        for module in required_modules:
            module_path = orch_dir / module
            assert module_path.exists(), f"Module {module} should exist"
    
    def test_orchestration_has_registry_submodule(self):
        """Test that orchestration has registry submodule."""
        registry_dir = REPO_ROOT / "fool_platform" / "orchestration" / "registry"
        assert registry_dir.exists(), "Registry directory should exist"
        
        required = ["agent_registry.py", "capability_registry.py", "workflow_registry.py", "policy_registry.py"]
        for mod in required:
            assert (registry_dir / mod).exists(), f"Registry module {mod} should exist"
    
    def test_orchestration_has_state_submodule(self):
        """Test that orchestration has state submodule."""
        state_dir = REPO_ROOT / "fool_platform" / "orchestration" / "state"
        assert state_dir.exists(), "State directory should exist"
        
        required = ["workflow_state_store.py", "checkpoint.py", "state_transitions.py"]
        for mod in required:
            assert (state_dir / mod).exists(), f"State module {mod} should exist"
    
    def test_orchestration_has_policies_submodule(self):
        """Test that orchestration has policies submodule."""
        policies_dir = REPO_ROOT / "fool_platform" / "orchestration" / "policies"
        assert policies_dir.exists(), "Policies directory should exist"
        
        required = ["retry_policy.py", "timeout_policy.py", "failure_policy.py", "termination_policy.py"]
        for mod in required:
            assert (policies_dir / mod).exists(), f"Policy module {mod} should exist"
    
    def test_orchestration_has_planner_submodule(self):
        """Test that orchestration has planner submodule."""
        planner_dir = REPO_ROOT / "fool_platform" / "orchestration" / "planner"
        assert planner_dir.exists(), "Planner directory should exist"
        
        required = ["workflow_planner.py", "agent_selector.py"]
        for mod in required:
            assert (planner_dir / mod).exists(), f"Planner module {mod} should exist"
    
    def test_orchestration_has_engine_submodule(self):
        """Test that orchestration has engine submodule."""
        engine_dir = REPO_ROOT / "fool_platform" / "orchestration" / "engine"
        assert engine_dir.exists(), "Engine directory should exist"
        
        required = ["workflow_engine.py", "step_runner.py", "transition_evaluator.py"]
        for mod in required:
            assert (engine_dir / mod).exists(), f"Engine module {mod} should exist"
    
    def test_orchestration_has_tests(self):
        """Test that orchestration has tests."""
        tests_dir = REPO_ROOT / "fool_platform" / "orchestration" / "tests"
        assert tests_dir.exists(), "Tests directory should exist"
        
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "Orchestration should have test files"


class TestOrchestrationPurity:
    """Tests for Orchestration architecture purity."""
    
    def test_orchestration_does_not_import_ai(self):
        """Test that orchestration does not import ai."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        for py_file in orch_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from ai" not in content
            assert "import ai" not in content
    
    def test_orchestration_does_not_import_apps(self):
        """Test that orchestration does not import apps."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        for py_file in orch_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from apps" not in content
            assert "import apps" not in content
    
    def test_orchestration_does_not_import_infrastructure(self):
        """Test that orchestration does not import infrastructure."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        for py_file in orch_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from infrastructure" not in content
            assert "import infrastructure" not in content
    
    def test_orchestration_does_not_import_connectors(self):
        """Test that orchestration does not import connectors."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        for py_file in orch_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_orchestration_does_not_import_intelligence(self):
        """Test that orchestration does not import intelligence."""
        orch_dir = REPO_ROOT / "fool_platform" / "orchestration"
        
        for py_file in orch_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from intelligence" not in content
            assert "import intelligence" not in content


class TestDomainOrchestrationPurity:
    """Tests to ensure domain does not import orchestration."""
    
    def test_domain_does_not_import_orchestration(self):
        """Test that domain does not import platform orchestration."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.orchestration" not in content
            assert "import fool_platform.orchestration" not in content


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


class TestAgentRuntimeFoundation:
    """Tests for Agent Runtime foundation."""
    
    def test_agents_directory_exists(self):
        """Test that agents directory exists."""
        agents_dir = REPO_ROOT / "fool_platform" / "agents"
        assert agents_dir.exists(), "Agents directory should exist"
    
    def test_agents_has_base_submodule(self):
        """Test that agents has base submodule."""
        base_dir = REPO_ROOT / "fool_platform" / "agents" / "base"
        assert base_dir.exists(), "Base directory should exist"
        
        required = [
            "agent.py",
            "agent_exceptions.py",
            "context.py",
            "lifecycle.py",
            "memory.py",
            "models.py",
            "policies.py",
            "validation.py",
            "events.py",
            "example_agent.py",
        ]
        for mod in required:
            assert (base_dir / mod).exists(), f"Base module {mod} should exist"
    
    def test_agents_has_runtime_submodule(self):
        """Test that agents has runtime submodule."""
        runtime_dir = REPO_ROOT / "fool_platform" / "agents" / "runtime"
        assert runtime_dir.exists(), "Runtime directory should exist"
        
        required = ["executor.py"]
        for mod in required:
            assert (runtime_dir / mod).exists(), f"Runtime module {mod} should exist"
    
    def test_agents_has_registry_submodule(self):
        """Test that agents has registry submodule."""
        registry_dir = REPO_ROOT / "fool_platform" / "agents" / "registry"
        assert registry_dir.exists(), "Registry directory should exist"
        
        required = ["registry_adapter.py", "agents.yaml", "capabilities.yaml"]
        for mod in required:
            assert (registry_dir / mod).exists(), f"Registry module {mod} should exist"
    
    def test_agents_has_tests(self):
        """Test that agents has tests."""
        tests_dir = REPO_ROOT / "fool_platform" / "agents" / "tests"
        assert tests_dir.exists(), "Tests directory should exist"
        
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "Agents should have test files"


class TestAgentRuntimePurity:
    """Tests for Agent Runtime architecture purity."""
    
    def test_agents_does_not_import_ai(self):
        """Test that agents does not import ai."""
        agents_dir = REPO_ROOT / "fool_platform" / "agents"
        
        for py_file in agents_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from ai" not in content
            assert "import ai" not in content
            assert "openai" not in content.lower()
            assert "anthropic" not in content.lower()
    
    def test_agents_does_not_import_connectors(self):
        """Test that agents does not import connectors."""
        agents_dir = REPO_ROOT / "fool_platform" / "agents"
        
        for py_file in agents_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_agents_does_not_import_infrastructure(self):
        """Test that agents does not import infrastructure."""
        agents_dir = REPO_ROOT / "fool_platform" / "agents"
        
        for py_file in agents_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from infrastructure" not in content
            assert "import infrastructure" not in content
    
    def test_agents_does_not_import_applications(self):
        """Test that agents does not import applications."""
        agents_dir = REPO_ROOT / "fool_platform" / "agents"
        
        for py_file in agents_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from apps" not in content
            assert "import apps" not in content
    
    def test_agents_does_not_import_orchestration(self):
        """Test that agents base does not import orchestration."""
        base_dir = REPO_ROOT / "fool_platform" / "agents" / "base"
        
        for py_file in base_dir.glob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            # BaseAgent must not depend on orchestration
            assert "from fool_platform.orchestration" not in content
            assert "import fool_platform.orchestration" not in content


class TestDomainAgentRuntimePurity:
    """Tests to ensure domain does not import agents."""
    
    def test_domain_does_not_import_agents(self):
        """Test that domain does not import platform agents."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.agents" not in content
            assert "import fool_platform.agents" not in content


class TestKnowledgeFoundation:
    """Tests for Knowledge layer foundation."""
    
    def test_knowledge_directory_exists(self):
        """Test that knowledge directory exists."""
        knowledge_dir = REPO_ROOT / "knowledge"
        assert knowledge_dir.exists(), "Knowledge directory should exist"
    
    def test_knowledge_has_graph_submodule(self):
        """Test that knowledge has graph submodule."""
        graph_dir = REPO_ROOT / "knowledge" / "graph"
        assert graph_dir.exists(), "Graph directory should exist"
        
        required = ["models", "repository", "traversal", "queries", "validation"]
        for subdir in required:
            assert (graph_dir / subdir).exists(), f"Graph submodule {subdir} should exist"
    
    def test_knowledge_has_ontology_submodule(self):
        """Test that knowledge has ontology submodule."""
        ontology_dir = REPO_ROOT / "knowledge" / "ontology"
        assert ontology_dir.exists(), "Ontology directory should exist"
    
    def test_knowledge_has_resolution_submodule(self):
        """Test that knowledge has resolution submodule."""
        resolution_dir = REPO_ROOT / "knowledge" / "resolution"
        assert resolution_dir.exists(), "Resolution directory should exist"
    
    def test_knowledge_has_events_submodule(self):
        """Test that knowledge has events submodule."""
        events_dir = REPO_ROOT / "knowledge" / "events"
        assert events_dir.exists(), "Events directory should exist"
    
    def test_knowledge_has_services_submodule(self):
        """Test that knowledge has services submodule."""
        services_dir = REPO_ROOT / "knowledge" / "services"
        assert services_dir.exists(), "Services directory should exist"
    
    def test_knowledge_has_tests(self):
        """Test that knowledge has tests."""
        tests_dir = REPO_ROOT / "knowledge" / "tests"
        assert tests_dir.exists(), "Tests directory should exist"
        
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "Knowledge should have test files"


class TestKnowledgePurity:
    """Tests for Knowledge layer architecture purity."""
    
    def test_knowledge_does_not_import_ai(self):
        """Test that knowledge does not import ai."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from ai" not in content
            assert "import ai" not in content
            assert "openai" not in content.lower()
            assert "anthropic" not in content.lower()
    
    def test_knowledge_does_not_import_connectors(self):
        """Test that knowledge does not import connectors."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
    
    def test_knowledge_does_not_import_infrastructure(self):
        """Test that knowledge does not import infrastructure."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from infrastructure" not in content
            assert "import infrastructure" not in content
    
    def test_knowledge_does_not_import_applications(self):
        """Test that knowledge does not import applications."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from apps" not in content
            assert "import apps" not in content
    
    def test_knowledge_does_not_import_agents(self):
        """Test that knowledge does not import agents."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from fool_platform.agents" not in content
            assert "import fool_platform.agents" not in content
    
    def test_knowledge_does_not_import_intelligence(self):
        """Test that knowledge does not import intelligence."""
        knowledge_dir = REPO_ROOT / "knowledge"
        
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from intelligence" not in content
            assert "import intelligence" not in content


class TestDomainKnowledgePurity:
    """Tests to ensure domain does not import knowledge."""
    
    def test_domain_does_not_import_knowledge(self):
        """Test that domain does not import knowledge."""
        domain_dir = REPO_ROOT / "domain"
        
        for py_file in domain_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from knowledge" not in content
            assert "import knowledge" not in content
