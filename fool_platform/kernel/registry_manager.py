"""
platform/kernel/registry_manager.py

Registry management for loading and accessing platform registries.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .kernel_exceptions import RegistryError, RegistryLoadError

if TYPE_CHECKING:
    from .kernel_config import KernelConfig

logger = logging.getLogger(__name__)


class RegistryManager:
    """
    Manages loading and access to platform registries.
    
    Handles:
    - Agent Registry
    - Capability Registry
    - Workflow Registry
    - Concept Registry
    - Contract Registry
    """
    
    def __init__(self, config: "KernelConfig") -> None:
        self._config = config
        self._initialized = False
        self._registries: dict[str, Any] = {}
        self._registry_paths: dict[str, Path] = {}
    
    def initialize(self) -> None:
        """Initialize the registry manager and load registries."""
        if self._initialized:
            logger.warning("RegistryManager already initialized")
            return
        
        logger.debug("RegistryManager initializing")
        
        # Build registry paths from config
        base_path = Path.cwd()
        for name, path in self._config.registry_paths.items():
            self._registry_paths[name] = base_path / path
        
        # Load each registry
        self._load_registries()
        
        self._initialized = True
        logger.info("RegistryManager initialized")
    
    def dispose(self) -> None:
        """Dispose the registry manager."""
        self._registries.clear()
        self._registry_paths.clear()
        logger.info("RegistryManager disposed")
    
    def get_registry(self, name: str) -> Any | None:
        """
        Get a registry by name.
        
        Args:
            name: Registry name (e.g., 'agents', 'capabilities', 'workflows')
            
        Returns:
            Registry contents or None if not found
        """
        return self._registries.get(name)
    
    def _load_registries(self) -> None:
        """Load all configured registries."""
        loaders = {
            "agents": self._load_agents_registry,
            "capabilities": self._load_capabilities_registry,
            "workflows": self._load_workflows_registry,
            "contracts": self._load_contracts_registry,
            "concepts": self._load_concepts_registry,
        }
        
        for name, loader in loaders.items():
            if name in self._registry_paths:
                try:
                    loader(name)
                except Exception as e:
                    logger.warning(f"Failed to load registry '{name}': {e}")
    
    def _load_agents_registry(self, name: str) -> None:
        """Load the agents registry from YAML."""
        path = self._registry_paths[name]
        if not path.exists():
            logger.debug(f"Agents registry not found at {path}")
            return
        
        try:
            # Try to load YAML using safe loader
            data = self._load_yaml(path)
            self._registries[name] = data
            logger.debug(f"Loaded agents registry: {len(data.get('agents', []))} agents")
        except ImportError:
            logger.warning("PyYAML not available, registry loading skipped")
    
    def _load_capabilities_registry(self, name: str) -> None:
        """Load the capabilities registry from YAML."""
        path = self._registry_paths[name]
        if not path.exists():
            logger.debug(f"Capabilities registry not found at {path}")
            return
        
        try:
            data = self._load_yaml(path)
            self._registries[name] = data
            logger.debug(f"Loaded capabilities registry: {len(data.get('capabilities', []))} capabilities")
        except ImportError:
            logger.warning("PyYAML not available, registry loading skipped")
    
    def _load_workflows_registry(self, name: str) -> None:
        """Load workflow definitions from YAML directory."""
        path = self._registry_paths[name]
        if not path.exists():
            logger.debug(f"Workflows registry not found at {path}")
            return
        
        try:
            workflows = {}
            if path.is_file():
                data = self._load_yaml(path)
                workflows[path.stem] = data
            elif path.is_dir():
                for yaml_file in path.glob("*.yaml"):
                    workflow_data = self._load_yaml(yaml_file)
                    workflows[yaml_file.stem] = workflow_data
            self._registries[name] = workflows
            logger.debug(f"Loaded workflows registry: {len(workflows)} workflows")
        except ImportError:
            logger.warning("PyYAML not available, registry loading skipped")
    
    def _load_contracts_registry(self, name: str) -> None:
        """Load contract schemas."""
        path = self._registry_paths[name]
        if not path.exists():
            logger.debug(f"Contracts registry not found at {path}")
            return
        
        contracts = {}
        if path.is_dir():
            for schema_file in path.rglob("*.schema.json"):
                try:
                    import json
                    with open(schema_file) as f:
                        data = json.load(f)
                    contracts[str(schema_file.relative_to(path))] = data
                except Exception as e:
                    logger.warning(f"Failed to load schema {schema_file}: {e}")
        self._registries[name] = contracts
        logger.debug(f"Loaded contracts registry: {len(contracts)} schemas")
    
    def _load_concepts_registry(self, name: str) -> None:
        """Load concept definitions."""
        path = self._registry_paths[name]
        if not path.exists():
            logger.debug(f"Concepts registry not found at {path}")
            return
        
        concepts = {}
        if path.is_dir():
            for concept_file in path.rglob("*.md"):
                try:
                    with open(concept_file) as f:
                        concepts[concept_file.stem] = f.read()
                except Exception as e:
                    logger.warning(f"Failed to load concept {concept_file}: {e}")
        self._registries[name] = concepts
        logger.debug(f"Loaded concepts registry: {len(concepts)} concepts")
    
    def _load_yaml(self, path: Path) -> dict:
        """Load YAML file using safe loader."""
        try:
            import yaml
            with open(path) as f:
                return yaml.safe_load(f) or {}
        except ImportError as e:
            raise ImportError("PyYAML required for YAML parsing") from e
    
    @property
    def registry_names(self) -> list[str]:
        """Return list of loaded registry names."""
        return list(self._registries.keys())


__all__ = [
    "RegistryManager",
]
