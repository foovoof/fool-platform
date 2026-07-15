"""
fool_platform/agents/registry/registry_adapter.py

Registry Adapter for FOOL Platform.

Loads agent and capability definitions from YAML files.
"""
from pathlib import Path
from typing import Any

import yaml


class RegistryAdapter:
    """
    Adapter for loading agent and capability definitions.
    
    Reads from:
    - platform/agents/registry/agents.yaml
    - platform/agents/registry/capabilities.yaml
    
    This is read-only. Does not instantiate real agents.
    """

    def __init__(
        self,
        registry_path: Path | None = None,
    ) -> None:
        """
        Initialize the registry adapter.
        
        Args:
            registry_path: Path to the registry directory
        """
        if registry_path is None:
            self._registry_path = Path(__file__).parent
        else:
            self._registry_path = registry_path

        self._agents_cache: list[dict[str, Any]] | None = None
        self._capabilities_cache: list[dict[str, Any]] | None = None

    def _load_agents_yaml(self) -> list[dict[str, Any]]:
        """
        Load agents from YAML file.
        
        Returns:
            List of agent definitions
        """
        if self._agents_cache is not None:
            return self._agents_cache

        agents_file = self._registry_path / "agents.yaml"
        if not agents_file.exists():
            return []

        with open(agents_file, "r") as f:
            data = yaml.safe_load(f)

        self._agents_cache = data.get("agents", [])
        return self._agents_cache

    def _load_capabilities_yaml(self) -> list[dict[str, Any]]:
        """
        Load capabilities from YAML file.
        
        Returns:
            List of capability definitions
        """
        if self._capabilities_cache is not None:
            return self._capabilities_cache

        capabilities_file = self._registry_path / "capabilities.yaml"
        if not capabilities_file.exists():
            return []

        with open(capabilities_file, "r") as f:
            data = yaml.safe_load(f)

        self._capabilities_cache = data.get("capabilities", [])
        return self._capabilities_cache

    def list_registered_agents(self) -> list[dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            List of agent definitions
        """
        return self._load_agents_yaml()

    def list_registered_capabilities(self) -> list[dict[str, Any]]:
        """
        List all registered capabilities.
        
        Returns:
            List of capability definitions
        """
        return self._load_capabilities_yaml()

    def get_agent_definition(
        self, agent_type: str
    ) -> dict[str, Any] | None:
        """
        Get an agent definition by type.
        
        Args:
            agent_type: The agent type
            
        Returns:
            Agent definition or None if not found
        """
        agents = self._load_agents_yaml()
        for agent in agents:
            if agent.get("agent_type") == agent_type:
                return agent
        return None

    def get_capability_definition(
        self, capability_id: str
    ) -> dict[str, Any] | None:
        """
        Get a capability definition by ID.
        
        Args:
            capability_id: The capability ID
            
        Returns:
            Capability definition or None if not found
        """
        capabilities = self._load_capabilities_yaml()
        for cap in capabilities:
            if cap.get("capability_id") == capability_id:
                return cap
        return None

    def validate_agent_manifest(
        self, agent_manifest: dict[str, Any]
    ) -> tuple[bool, list[str]]:
        """
        Validate an agent manifest against the registry.
        
        Args:
            agent_manifest: Agent manifest to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors: list[str] = []

        if "agent_type" not in agent_manifest:
            errors.append("Agent manifest must have agent_type")
            return False, errors

        agent_type = agent_manifest["agent_type"]
        agent_def = self.get_agent_definition(agent_type)

        if not agent_def:
            errors.append(f"Agent type {agent_type} not found in registry")
            return False, errors

        declared_capabilities = set(agent_manifest.get("capabilities", []))
        registered_capabilities = set(agent_def.get("capabilities", []))

        for cap in declared_capabilities:
            if cap not in registered_capabilities:
                errors.append(
                    f"Capability {cap} not registered for agent type {agent_type}"
                )

        return len(errors) == 0, errors

    def get_agents_by_capability(
        self, capability_id: str
    ) -> list[dict[str, Any]]:
        """
        Get all agents that have a specific capability.
        
        Args:
            capability_id: The capability ID
            
        Returns:
            List of agent definitions
        """
        agents = self._load_agents_yaml()
        return [
            agent
            for agent in agents
            if capability_id in agent.get("capabilities", [])
        ]

    def reload(self) -> None:
        """
        Reload the registry from disk.
        
        Clears caches and reloads YAML files.
        """
        self._agents_cache = None
        self._capabilities_cache = None
        self._load_agents_yaml()
        self._load_capabilities_yaml()
