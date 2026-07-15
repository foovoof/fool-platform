"""
platform/kernel/registries/agent_registry.py

Loader for agent registry.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AgentType:
    """Represents an agent type from the registry."""
    agent_type: str
    version: str
    description: str
    capabilities: tuple[str, ...]
    manifest_schema_ref: str


@dataclass(frozen=True)
class AgentRegistry:
    """Loaded agent registry."""
    agents: tuple[AgentType, ...]
    loaded_from: str
    loaded_at: str


class AgentRegistryLoader:
    """
    Loads agent registry from YAML.
    
    Reads platform/agents/registry/agents.yaml
    """
    
    def __init__(self) -> None:
        self._registry: AgentRegistry | None = None
    
    def load(self, path: str | Path) -> AgentRegistry:
        """
        Load agent registry from file.
        
        Args:
            path: Path to agents.yaml file
            
        Returns:
            AgentRegistry with loaded agents
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Agent registry not found: {path}")
        
        try:
            import yaml
            with open(path) as f:
                data = yaml.safe_load(f)
        except ImportError:
            logger.warning("PyYAML not available, using minimal YAML parsing")
            data = self._minimal_yaml_load(path)
        
        agents_data = data.get("agents", [])
        agents = []
        for agent_data in agents_data:
            agent = AgentType(
                agent_type=agent_data.get("agent_type", ""),
                version=agent_data.get("version", "1.0.0"),
                description=agent_data.get("description", ""),
                capabilities=tuple(agent_data.get("capabilities", [])),
                manifest_schema_ref=agent_data.get("manifest_schema_ref", ""),
            )
            agents.append(agent)
        
        from datetime import datetime, timezone
        self._registry = AgentRegistry(
            agents=tuple(agents),
            loaded_from=str(path),
            loaded_at=datetime.now(timezone.utc).isoformat(),
        )
        
        logger.info(f"Loaded {len(agents)} agents from {path}")
        return self._registry
    
    def get_registry(self) -> AgentRegistry | None:
        """Get the loaded registry."""
        return self._registry
    
    def get_agent(self, agent_type: str) -> AgentType | None:
        """Get a specific agent by type."""
        if not self._registry:
            return None
        for agent in self._registry.agents:
            if agent.agent_type == agent_type:
                return agent
        return None
    
    def _minimal_yaml_load(self, path: Path) -> dict:
        """Minimal YAML parsing without PyYAML."""
        content = path.read_text()
        data = {"agents": []}
        
        in_agents = False
        current_agent = {}
        
        for line in content.split("\n"):
            stripped = line.strip()
            
            if stripped.startswith("agents:"):
                in_agents = True
                continue
            
            if in_agents:
                if stripped.startswith("- agent_type:"):
                    if current_agent:
                        data["agents"].append(current_agent)
                    current_agent = {"agent_type": stripped.split(":", 1)[1].strip()}
                elif ":" in stripped and current_agent:
                    key, _, value = stripped.partition(":")
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "version":
                        current_agent["version"] = value
                    elif key == "description":
                        current_agent["description"] = value
                    elif key == "capabilities":
                        pass  # Skip for minimal parsing
                    elif key == "manifest_schema_ref":
                        current_agent["manifest_schema_ref"] = value
        
        if current_agent:
            data["agents"].append(current_agent)
        
        return data


__all__ = [
    "AgentRegistry",
    "AgentRegistryLoader",
    "AgentType",
]
