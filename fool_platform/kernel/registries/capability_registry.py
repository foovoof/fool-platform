"""
platform/kernel/registries/capability_registry.py

Loader for capability registry.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Capability:
    """Represents a capability from the registry."""
    capability: str
    version: str
    description: str
    input_schema_ref: str
    output_schema_ref: str


@dataclass(frozen=True)
class CapabilityRegistry:
    """Loaded capability registry."""
    capabilities: tuple[Capability, ...]
    loaded_from: str
    loaded_at: str


class CapabilityRegistryLoader:
    """
    Loads capability registry from YAML.
    
    Reads platform/agents/registry/capabilities.yaml
    """
    
    def __init__(self) -> None:
        self._registry: CapabilityRegistry | None = None
    
    def load(self, path: str | Path) -> CapabilityRegistry:
        """
        Load capability registry from file.
        
        Args:
            path: Path to capabilities.yaml file
            
        Returns:
            CapabilityRegistry with loaded capabilities
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Capability registry not found: {path}")
        
        try:
            import yaml
            with open(path) as f:
                data = yaml.safe_load(f)
        except ImportError:
            logger.warning("PyYAML not available, using minimal YAML parsing")
            data = self._minimal_yaml_load(path)
        
        caps_data = data.get("capabilities", [])
        capabilities = []
        for cap_data in caps_data:
            cap = Capability(
                capability=cap_data.get("capability", ""),
                version=cap_data.get("version", "1.0.0"),
                description=cap_data.get("description", ""),
                input_schema_ref=cap_data.get("input_schema_ref", ""),
                output_schema_ref=cap_data.get("output_schema_ref", ""),
            )
            capabilities.append(cap)
        
        self._registry = CapabilityRegistry(
            capabilities=tuple(capabilities),
            loaded_from=str(path),
            loaded_at=datetime.now(timezone.utc).isoformat(),
        )
        
        logger.info(f"Loaded {len(capabilities)} capabilities from {path}")
        return self._registry
    
    def get_registry(self) -> CapabilityRegistry | None:
        """Get the loaded registry."""
        return self._registry
    
    def get_capability(self, name: str) -> Capability | None:
        """Get a specific capability by name."""
        if not self._registry:
            return None
        for cap in self._registry.capabilities:
            if cap.capability == name:
                return cap
        return None
    
    def _minimal_yaml_load(self, path: Path) -> dict:
        """Minimal YAML parsing without PyYAML."""
        content = path.read_text()
        data = {"capabilities": []}
        
        in_caps = False
        current_cap = {}
        
        for line in content.split("\n"):
            stripped = line.strip()
            
            if stripped.startswith("capabilities:"):
                in_caps = True
                continue
            
            if in_caps:
                if stripped.startswith("- capability:"):
                    if current_cap:
                        data["capabilities"].append(current_cap)
                    current_cap = {"capability": stripped.split(":", 1)[1].strip()}
                elif ":" in stripped and current_cap:
                    key, _, value = stripped.partition(":")
                    key = key.strip()
                    value = value.strip()
                    
                    if key in ("version", "description", "input_schema_ref", "output_schema_ref"):
                        current_cap[key] = value
        
        if current_cap:
            data["capabilities"].append(current_cap)
        
        return data


__all__ = [
    "CapabilityRegistry",
    "CapabilityRegistryLoader",
    "Capability",
]
