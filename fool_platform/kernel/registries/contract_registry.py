"""
platform/kernel/registries/contract_registry.py

Loader for contract schemas.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ContractSchema:
    """Loaded contract schema."""
    id: str
    title: str
    path: str
    schema: dict


@dataclass(frozen=True)
class ContractRegistry:
    """Loaded contract registry."""
    schemas: tuple[ContractSchema, ...]
    loaded_from: str
    loaded_at: str


class ContractRegistryLoader:
    """
    Loads JSON Schema contract definitions.
    
    Reads contract schemas from contracts/ directory.
    """
    
    def __init__(self) -> None:
        self._registry: ContractRegistry | None = None
    
    def load(self, path: str | Path) -> ContractRegistry:
        """
        Load contract registry from directory.
        
        Args:
            path: Path to contracts directory
            
        Returns:
            ContractRegistry with loaded schemas
        """
        path = Path(path)
        schemas = []
        
        if not path.exists():
            raise FileNotFoundError(f"Contract registry not found: {path}")
        
        if path.is_dir():
            # Load all schema.json files
            for schema_file in sorted(path.rglob("*.schema.json")):
                try:
                    with open(schema_file) as f:
                        schema = json.load(f)
                    
                    relative_path = str(schema_file.relative_to(path))
                    
                    contract = ContractSchema(
                        id=schema.get("$id", schema.get("title", schema_file.stem)),
                        title=schema.get("title", schema_file.stem),
                        path=relative_path,
                        schema=schema,
                    )
                    schemas.append(contract)
                except Exception as e:
                    logger.warning(f"Failed to load schema {schema_file}: {e}")
        
        self._registry = ContractRegistry(
            schemas=tuple(schemas),
            loaded_from=str(path),
            loaded_at=datetime.now(timezone.utc).isoformat(),
        )
        
        logger.info(f"Loaded {len(schemas)} contract schemas from {path}")
        return self._registry
    
    def get_registry(self) -> ContractRegistry | None:
        """Get the loaded registry."""
        return self._registry
    
    def get_contract(self, id_or_title: str) -> ContractSchema | None:
        """Get a specific contract by ID or title."""
        if not self._registry:
            return None
        for contract in self._registry.schemas:
            if contract.id == id_or_title or contract.title == id_or_title:
                return contract
        return None
    
    def get_by_path(self, path: str) -> ContractSchema | None:
        """Get a specific contract by file path."""
        if not self._registry:
            return None
        for contract in self._registry.schemas:
            if contract.path == path:
                return contract
        return None


__all__ = [
    "ContractRegistry",
    "ContractRegistryLoader",
    "ContractSchema",
]
