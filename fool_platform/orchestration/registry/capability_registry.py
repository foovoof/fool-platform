"""
fool_platform/orchestration/registry/capability_registry.py

Capability registry for managing capability definitions.
"""
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any

from fool_platform.orchestration.orchestration_exceptions import CapabilityRegistryError


@dataclass
class CapabilityDefinition:
    """Definition of a capability."""
    id: str
    version: str
    description: str | None = None
    input_schema_ref: str | None = None
    output_schema_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class CapabilityRegistry:
    """
    Registry for capability definitions.
    
    Loads capabilities from capabilities.yaml files.
    Does not implement capabilities - only references them.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        self._capabilities: dict[str, CapabilityDefinition] = {}
        self._lock = Lock()
        self._loaded = False
        self._registry_path = registry_path
        if registry_path and registry_path.exists():
            self.load_capabilities(registry_path)

    def load_capabilities(self, registry_path: Path | None = None) -> None:
        """
        Load capability definitions from YAML.
        
        Args:
            registry_path: Path to capabilities.yaml (uses default if None)
        """
        path = registry_path or self._registry_path
        if not path or not path.exists():
            return

        with self._lock:
            try:
                import yaml
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                if data and "capabilities" in data:
                    for cap_data in data["capabilities"]:
                        cap = CapabilityDefinition(
                            id=cap_data["id"],
                            version=cap_data.get("version", "1.0.0"),
                            description=cap_data.get("description"),
                            input_schema_ref=cap_data.get("input_schema_ref"),
                            output_schema_ref=cap_data.get("output_schema_ref"),
                        )
                        self._capabilities[cap.id] = cap
                
                self._loaded = True
            except ImportError:
                self._load_simple_yaml(path)
            except Exception as e:
                raise CapabilityRegistryError(
                    f"Failed to load capabilities from {path}: {e}",
                    cause=e,
                )

    def _load_simple_yaml(self, path: Path) -> None:
        """Simple YAML fallback without PyYAML."""
        try:
            with open(path, "r") as f:
                content = f.read()
            
            cap_id = None
            version = None
            description = None
            
            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                if "id:" in line and "-" not in line[:10]:
                    parts = line.split(":", 1)
                    if len(parts) == 2 and parts[0].strip() == "id":
                        if cap_id and version:
                            cap = CapabilityDefinition(
                                id=cap_id,
                                version=version,
                                description=description,
                            )
                            self._capabilities[cap.id] = cap
                        cap_id = parts[1].strip()
                        version = None
                        description = None
                elif "version:" in line and version is None:
                    version = line.split("version:")[1].strip()
                elif "description:" in line:
                    desc_line = line.split("description:")[1].strip()
                    if desc_line.startswith(">"):
                        desc_line = " ".join(desc_line.split()[1:])
                    description = desc_line
            
            if cap_id and version:
                cap = CapabilityDefinition(
                    id=cap_id,
                    version=version,
                    description=description,
                )
                self._capabilities[cap.id] = cap
            
            self._loaded = True
        except Exception:
            pass

    def list_capabilities(self) -> list[str]:
        """List all registered capability IDs."""
        with self._lock:
            return list(self._capabilities.keys())

    def get_capability(self, capability_id: str) -> CapabilityDefinition | None:
        """Get capability definition by ID."""
        with self._lock:
            return self._capabilities.get(capability_id)

    def has_capability(self, capability_id: str) -> bool:
        """Check if capability is registered."""
        with self._lock:
            return capability_id in self._capabilities

    def validate_capability_reference(self, capability_id: str) -> bool:
        """
        Validate that a capability reference is valid.
        
        Args:
            capability_id: The capability ID to validate
            
        Returns:
            True if valid
            
        Raises:
            CapabilityRegistryError: If capability is not found
        """
        if not self.has_capability(capability_id):
            raise CapabilityRegistryError(
                f"Capability not found: {capability_id}",
                capability_id=capability_id,
            )
        return True

    def is_loaded(self) -> bool:
        """Check if capabilities have been loaded."""
        with self._lock:
            return self._loaded

    def clear(self) -> None:
        """Clear all registered capabilities."""
        with self._lock:
            self._capabilities.clear()
            self._loaded = False
