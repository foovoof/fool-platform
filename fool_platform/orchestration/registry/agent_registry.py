"""
fool_platform/orchestration/registry/agent_registry.py

Agent registry for managing agent definitions.
"""
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any

from fool_platform.orchestration.orchestration_exceptions import AgentRegistryError


@dataclass
class AgentDefinition:
    """Definition of an agent type."""
    agent_type: str
    version: str
    description: str | None = None
    capabilities: list[str] = field(default_factory=list)
    manifest_schema_ref: str | None = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentRegistry:
    """
    Registry for agent definitions.
    
    Loads agents from agents.yaml files.
    Does not execute agents - only references them.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        self._agents: dict[str, AgentDefinition] = {}
        self._capability_index: dict[str, list[str]] = {}
        self._lock = Lock()
        self._loaded = False
        self._registry_path = registry_path
        if registry_path and registry_path.exists():
            self.load_agents(registry_path)

    def load_agents(self, registry_path: Path | None = None) -> None:
        """
        Load agent definitions from YAML.
        
        Args:
            registry_path: Path to agents.yaml (uses default if None)
        """
        path = registry_path or self._registry_path
        if not path or not path.exists():
            return

        with self._lock:
            try:
                import yaml
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                if data and "agents" in data:
                    for agent_data in data["agents"]:
                        agent = AgentDefinition(
                            agent_type=agent_data["agent_type"],
                            version=agent_data.get("version", "1.0.0"),
                            description=agent_data.get("description"),
                            capabilities=agent_data.get("capabilities", []),
                            manifest_schema_ref=agent_data.get("manifest_schema_ref"),
                            enabled=True,
                        )
                        self._agents[agent.agent_type] = agent
                        
                        for cap in agent.capabilities:
                            if cap not in self._capability_index:
                                self._capability_index[cap] = []
                            self._capability_index[cap].append(agent.agent_type)
                
                self._loaded = True
            except ImportError:
                self._load_simple_yaml(path)
            except Exception as e:
                raise AgentRegistryError(
                    f"Failed to load agents from {path}: {e}",
                    cause=e,
                )

    def _load_simple_yaml(self, path: Path) -> None:
        """Simple YAML fallback without PyYAML."""
        try:
            with open(path, "r") as f:
                content = f.read()
            
            agent_type = None
            version = None
            capabilities = []
            
            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                if "agent_type:" in line:
                    agent_type = line.split("agent_type:")[1].strip()
                elif "version:" in line and version is None:
                    version = line.split("version:")[1].strip()
                elif "capabilities:" in line:
                    continue
                elif "- " in line and agent_type:
                    capabilities.append(line.replace("- ", "").strip())
                
                if agent_type and version and line.startswith("agents:"):
                    agent = AgentDefinition(
                        agent_type=agent_type,
                        version=version,
                        capabilities=capabilities,
                    )
                    self._agents[agent.agent_type] = agent
                    for cap in capabilities:
                        if cap not in self._capability_index:
                            self._capability_index[cap] = []
                        self._capability_index[cap].append(agent.agent_type)
                    agent_type = None
                    version = None
                    capabilities = []
            
            self._loaded = True
        except Exception:
            pass

    def list_agents(self) -> list[str]:
        """List all registered agent types."""
        with self._lock:
            return list(self._agents.keys())

    def get_agent(self, agent_id: str) -> AgentDefinition | None:
        """Get agent definition by type."""
        with self._lock:
            return self._agents.get(agent_id)

    def has_agent(self, agent_id: str) -> bool:
        """Check if agent type is registered."""
        with self._lock:
            return agent_id in self._agents

    def has_capability(self, capability_id: str) -> bool:
        """Check if any agent provides a capability."""
        with self._lock:
            return capability_id in self._capability_index

    def list_agents_with_capability(self, capability_id: str) -> list[str]:
        """List agents that provide a capability."""
        with self._lock:
            return self._capability_index.get(capability_id, []).copy()

    def list_enabled_agents(self) -> list[str]:
        """List all enabled agent types."""
        with self._lock:
            return [
                agent_id
                for agent_id, agent in self._agents.items()
                if agent.enabled
            ]

    def validate_agent_reference(self, agent_id: str) -> bool:
        """
        Validate that an agent reference is valid.
        
        Args:
            agent_id: The agent type to validate
            
        Returns:
            True if valid
            
        Raises:
            AgentRegistryError: If agent is not found
        """
        if not self.has_agent(agent_id):
            raise AgentRegistryError(
                f"Agent not found: {agent_id}",
                agent_id=agent_id,
            )
        return True

    def is_loaded(self) -> bool:
        """Check if agents have been loaded."""
        with self._lock:
            return self._loaded

    def clear(self) -> None:
        """Clear all registered agents."""
        with self._lock:
            self._agents.clear()
            self._capability_index.clear()
            self._loaded = False
