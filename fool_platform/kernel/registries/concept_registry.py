"""
platform/kernel/registries/concept_registry.py

Loader for concept definitions.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConceptDefinition:
    """Loaded concept definition."""
    name: str
    path: str
    content: str


@dataclass(frozen=True)
class ConceptRegistry:
    """Loaded concept registry."""
    concepts: tuple[ConceptDefinition, ...]
    loaded_from: str
    loaded_at: str


class ConceptRegistryLoader:
    """
    Loads concept definitions from markdown files.
    
    Reads concept definitions from standards/concepts/ directory.
    """
    
    def __init__(self) -> None:
        self._registry: ConceptRegistry | None = None
    
    def load(self, path: str | Path) -> ConceptRegistry:
        """
        Load concept registry from directory.
        
        Args:
            path: Path to concepts directory
            
        Returns:
            ConceptRegistry with loaded concepts
        """
        path = Path(path)
        concepts = []
        
        if not path.exists():
            raise FileNotFoundError(f"Concept registry not found: {path}")
        
        if path.is_dir():
            # Load all markdown files
            for md_file in sorted(path.rglob("*.md")):
                try:
                    content = md_file.read_text()
                    relative_path = str(md_file.relative_to(path))
                    
                    concept = ConceptDefinition(
                        name=md_file.stem,
                        path=relative_path,
                        content=content,
                    )
                    concepts.append(concept)
                except Exception as e:
                    logger.warning(f"Failed to load concept {md_file}: {e}")
        
        self._registry = ConceptRegistry(
            concepts=tuple(concepts),
            loaded_from=str(path),
            loaded_at=datetime.now(timezone.utc).isoformat(),
        )
        
        logger.info(f"Loaded {len(concepts)} concepts from {path}")
        return self._registry
    
    def get_registry(self) -> ConceptRegistry | None:
        """Get the loaded registry."""
        return self._registry
    
    def get_concept(self, name: str) -> ConceptDefinition | None:
        """Get a specific concept by name."""
        if not self._registry:
            return None
        for concept in self._registry.concepts:
            if concept.name == name:
                return concept
        return None


__all__ = [
    "ConceptDefinition",
    "ConceptRegistry",
    "ConceptRegistryLoader",
]
