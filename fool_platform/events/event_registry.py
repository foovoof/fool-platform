"""
fool_platform/events/event_registry.py

Event registry for managing event type definitions from contracts/standards.
"""
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock

from fool_platform.events.exceptions import EventRegistryError


@dataclass
class EventDefinition:
    """Definition of an event type from contracts."""
    event_type: str
    event_version: str
    description: str | None = None
    schema_ref: str | None = None
    compatibility: str | None = None
    metadata_schema: dict | None = None
    payload_schema: dict | None = None


@dataclass
class EventRegistry:
    """
    Registry for event type definitions.
    
    Loads event definitions from contracts/events/ and standards/events/.
    Provides validation and lookup of event types and versions.
    """
    _definitions: dict[str, dict[str, EventDefinition]] = field(default_factory=dict)
    _loaded: bool = False
    _lock: Lock = field(default_factory=Lock)
    _contracts_path: Path | None = None
    _standards_path: Path | None = None

    def __init__(
        self,
        contracts_path: Path | None = None,
        standards_path: Path | None = None,
        auto_load: bool = True,
    ) -> None:
        """
        Initialize the EventRegistry.
        
        Args:
            contracts_path: Path to contracts/events/ directory
            standards_path: Path to standards/events/ directory
            auto_load: Whether to auto-load definitions on initialization
        """
        self._definitions: dict[str, dict[str, EventDefinition]] = {}
        self._loaded = False
        self._lock = Lock()
        self._contracts_path = contracts_path
        self._standards_path = standards_path
        if auto_load:
            self.load_definitions()

    def load_definitions(self) -> None:
        """
        Load event definitions from contracts and standards directories.
        
        This method looks for YAML or JSON files in the configured paths.
        """
        with self._lock:
            if self._contracts_path:
                self._load_from_directory(self._contracts_path)
            if self._standards_path:
                self._load_from_directory(self._standards_path)
            self._loaded = True

    def _load_from_directory(self, directory: Path) -> None:
        """
        Load event definitions from a directory.
        
        Args:
            directory: Path to the events directory
        """
        if not directory.exists():
            return

        for file_path in directory.rglob("*.yaml"):
            self._load_yaml_file(file_path)
        for file_path in directory.rglob("*.yml"):
            self._load_yaml_file(file_path)
        for file_path in directory.rglob("*.json"):
            self._load_json_file(file_path)

    def _load_yaml_file(self, file_path: Path) -> None:
        """
        Load event definitions from a YAML file.
        
        Args:
            file_path: Path to the YAML file
        """
        try:
            import yaml
            
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            
            self._parse_event_catalog(data, file_path.stem)
        except ImportError:
            self._load_simple_yaml_fallback(file_path)
        except Exception:
            pass

    def _load_simple_yaml_fallback(self, file_path: Path) -> None:
        """
        Minimal YAML parsing fallback without PyYAML.
        
        Supports simple key: value format.
        """
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            event_type = None
            event_version = None
            description = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    
                    if key == "event_type":
                        event_type = value
                    elif key == "version" or key == "event_version":
                        event_version = value
                    elif key == "description":
                        description = value
                
                if event_type and event_version:
                    self._register_definition(
                        EventDefinition(
                            event_type=event_type,
                            event_version=event_version,
                            description=description,
                        )
                    )
                    event_type = None
                    event_version = None
                    description = None
        except Exception:
            pass

    def _load_json_file(self, file_path: Path) -> None:
        """
        Load event definitions from a JSON file.
        
        Args:
            file_path: Path to the JSON file
        """
        try:
            import json
            
            with open(file_path, "r") as f:
                data = json.load(f)
            
            self._parse_event_catalog(data, file_path.stem)
        except Exception:
            pass

    def _parse_event_catalog(self, data: dict, source: str) -> None:
        """
        Parse event catalog from loaded data.
        
        Args:
            data: The loaded catalog data
            source: The source identifier for the catalog
        """
        if not isinstance(data, dict):
            return

        if "events" in data and isinstance(data["events"], list):
            for event in data["events"]:
                self._register_definition(
                    EventDefinition(
                        event_type=event.get("event_type", ""),
                        event_version=event.get("version", event.get("event_version", "")),
                        description=event.get("description"),
                        schema_ref=event.get("schema_ref"),
                        compatibility=event.get("compatibility"),
                    )
                )
        elif "event_types" in data and isinstance(data["event_types"], list):
            for event in data["event_types"]:
                self._register_definition(
                    EventDefinition(
                        event_type=event.get("name", ""),
                        event_version=event.get("version", ""),
                        description=event.get("description"),
                    )
                )

    def _register_definition(self, definition: EventDefinition) -> None:
        """
        Register an event definition.
        
        Args:
            definition: The event definition to register
        """
        if not definition.event_type or not definition.event_version:
            return

        if definition.event_type not in self._definitions:
            self._definitions[definition.event_type] = {}

        self._definitions[definition.event_type][definition.event_version] = definition

    def list_event_types(self) -> list[str]:
        """
        List all registered event types.
        
        Returns:
            List of event type names
        """
        with self._lock:
            return list(self._definitions.keys())

    def get_event_definition(
        self,
        event_type: str,
        event_version: str | None = None,
    ) -> EventDefinition | None:
        """
        Get an event definition by type and version.
        
        Args:
            event_type: The event type name
            event_version: The event version (returns latest if None)
            
        Returns:
            The EventDefinition or None if not found
        """
        with self._lock:
            if event_type not in self._definitions:
                return None

            versions = self._definitions[event_type]

            if event_version is None:
                versions_list = sorted(
                    versions.keys(),
                    key=lambda v: [int(x) for x in v.split(".")],
                    reverse=True,
                )
                if versions_list:
                    return versions[versions_list[0]]
                return None

            return versions.get(event_version)

    def has_event_type(self, event_type: str) -> bool:
        """
        Check if an event type is registered.
        
        Args:
            event_type: The event type name
            
        Returns:
            True if the event type is registered
        """
        with self._lock:
            return event_type in self._definitions

    def has_event_version(self, event_type: str, event_version: str) -> bool:
        """
        Check if a specific event version is registered.
        
        Args:
            event_type: The event type name
            event_version: The event version
            
        Returns:
            True if the version is registered
        """
        with self._lock:
            if event_type not in self._definitions:
                return False
            return event_version in self._definitions[event_type]

    def validate_event_type(
        self,
        event_type: str,
        event_version: str | None = None,
    ) -> bool:
        """
        Validate that an event type and version are registered.
        
        Args:
            event_type: The event type name
            event_version: The event version (optional)
            
        Returns:
            True if valid, False otherwise
        """
        if not self.has_event_type(event_type):
            return False

        if event_version is not None and not self.has_event_version(event_type, event_version):
            return False

        return True

    def get_latest_version(self, event_type: str) -> str | None:
        """
        Get the latest registered version for an event type.
        
        Args:
            event_type: The event type name
            
        Returns:
            The latest version string or None
        """
        with self._lock:
            if event_type not in self._definitions:
                return None

            versions = self._definitions[event_type]
            versions_list = sorted(
                versions.keys(),
                key=lambda v: [int(x) if x.isdigit() else 0 for x in v.split(".")],
                reverse=True,
            )
            return versions_list[0] if versions_list else None

    def is_loaded(self) -> bool:
        """Check if definitions have been loaded."""
        with self._lock:
            return self._loaded

    def clear(self) -> None:
        """Clear all registered definitions."""
        with self._lock:
            self._definitions.clear()
            self._loaded = False

    def register_standard_event(
        self,
        event_type: str,
        event_version: str,
        description: str | None = None,
        schema_ref: str | None = None,
    ) -> None:
        """
        Programmatically register a standard event definition.
        
        Args:
            event_type: The event type name
            event_version: The event version
            description: Optional description
            schema_ref: Optional schema reference
        """
        with self._lock:
            self._register_definition(
                EventDefinition(
                    event_type=event_type,
                    event_version=event_version,
                    description=description,
                    schema_ref=schema_ref,
                )
            )
            self._loaded = True
