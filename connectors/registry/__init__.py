"""
connectors/registry/__init__.py

Connector Registry.

Loads connector manifests from YAML.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


class ConnectorRegistryLoader:
    """
    Loads connector manifests from YAML.
    
    Responsibilities:
    - Load manifest files
    - Parse connector definitions
    - Validate manifests
    """
    
    def __init__(self) -> None:
        """Initialize loader."""
        self._manifests: dict[str, dict] = {}
        self._connectors: dict[str, dict] = {}
    
    def load_manifest(self, path: str | Path) -> bool:
        """
        Load manifest from file.
        
        Args:
            path: Path to manifest file
            
        Returns:
            True if loaded
        """
        try:
            manifest_path = Path(path)
            if not manifest_path.exists():
                return False
            
            with open(manifest_path) as f:
                manifest = yaml.safe_load(f)
            
            if not manifest:
                return False
            
            self._manifests[str(manifest_path)] = manifest
            
            connectors = manifest.get("connectors", [])
            for connector in connectors:
                cid = connector.get("connector_id")
                if cid:
                    self._connectors[cid] = connector
            
            return True
        
        except Exception:
            return False
    
    def load_directory(self, directory: str | Path) -> int:
        """
        Load all manifests from directory.
        
        Args:
            directory: Directory containing manifests
            
        Returns:
            Number of manifests loaded
        """
        manifest_dir = Path(directory)
        if not manifest_dir.exists():
            return 0
        
        count = 0
        for manifest_path in manifest_dir.glob("*.yaml"):
            if self.load_manifest(manifest_path):
                count += 1
        
        for manifest_path in manifest_dir.glob("*.yml"):
            if self.load_manifest(manifest_path):
                count += 1
        
        return count
    
    def get_connector(self, connector_id: str) -> dict | None:
        """Get connector by ID."""
        return self._connectors.get(connector_id)
    
    def list_connectors(self) -> list[dict]:
        """List all connectors."""
        return list(self._connectors.values())
    
    def validate_manifest(self, manifest: dict) -> tuple[bool, list[str]]:
        """
        Validate manifest structure.
        
        Args:
            manifest: Manifest to validate
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        if not isinstance(manifest, dict):
            errors.append("Manifest must be a dictionary")
            return False, errors
        
        if "connectors" not in manifest:
            errors.append("Manifest must have 'connectors' key")
        
        connectors = manifest.get("connectors", [])
        if not isinstance(connectors, list):
            errors.append("'connectors' must be a list")
            return False, errors
        
        for i, connector in enumerate(connectors):
            if not isinstance(connector, dict):
                errors.append(f"Connector {i} must be a dictionary")
                continue
            
            required_fields = ["connector_id", "name", "connector_type"]
            for field in required_fields:
                if field not in connector:
                    errors.append(f"Connector {i} missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def get_manifests(self) -> dict[str, dict]:
        """Get all loaded manifests."""
        return self._manifests.copy()
    
    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._manifests.clear()
        self._connectors.clear()


def create_default_registry() -> ConnectorRegistryLoader:
    """Create default registry loader."""
    loader = ConnectorRegistryLoader()
    
    base_path = Path(__file__).parent.parent
    
    default_manifest_path = base_path / "manifest.yaml"
    if default_manifest_path.exists():
        loader.load_manifest(default_manifest_path)
    
    return loader
