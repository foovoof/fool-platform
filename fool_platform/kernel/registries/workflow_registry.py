"""
platform/kernel/registries/workflow_registry.py

Loader for workflow definitions.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WorkflowDefinition:
    """Loaded workflow definition."""
    name: str
    version: str
    description: str
    data: dict


@dataclass(frozen=True)
class WorkflowRegistry:
    """Loaded workflow registry."""
    workflows: tuple[WorkflowDefinition, ...]
    loaded_from: str
    loaded_at: str


class WorkflowRegistryLoader:
    """
    Loads workflow definitions from YAML files.
    
    Reads workflow definitions from workflows/ directory.
    """
    
    def __init__(self) -> None:
        self._registry: WorkflowRegistry | None = None
    
    def load(self, path: str | Path) -> WorkflowRegistry:
        """
        Load workflow registry from directory or file.
        
        Args:
            path: Path to workflows directory or workflow file
            
        Returns:
            WorkflowRegistry with loaded workflows
        """
        path = Path(path)
        workflows = []
        
        if not path.exists():
            raise FileNotFoundError(f"Workflow registry not found: {path}")
        
        if path.is_file():
            # Single file
            workflow = self._load_workflow(path)
            if workflow:
                workflows.append(workflow)
        elif path.is_dir():
            # Directory of workflow files
            for yaml_file in sorted(path.glob("*.yaml")):
                workflow = self._load_workflow(yaml_file)
                if workflow:
                    workflows.append(workflow)
        
        self._registry = WorkflowRegistry(
            workflows=tuple(workflows),
            loaded_from=str(path),
            loaded_at=datetime.now(timezone.utc).isoformat(),
        )
        
        logger.info(f"Loaded {len(workflows)} workflows from {path}")
        return self._registry
    
    def _load_workflow(self, path: Path) -> WorkflowDefinition | None:
        """Load a single workflow file."""
        try:
            import yaml
            with open(path) as f:
                data = yaml.safe_load(f)
        except ImportError:
            logger.warning(f"PyYAML not available, skipping {path}")
            return None
        
        if not data:
            return None
        
        return WorkflowDefinition(
            name=data.get("name", path.stem),
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            data=data,
        )
    
    def get_registry(self) -> WorkflowRegistry | None:
        """Get the loaded registry."""
        return self._registry
    
    def get_workflow(self, name: str) -> WorkflowDefinition | None:
        """Get a specific workflow by name."""
        if not self._registry:
            return None
        for workflow in self._registry.workflows:
            if workflow.name == name:
                return workflow
        return None


__all__ = [
    "WorkflowDefinition",
    "WorkflowRegistry",
    "WorkflowRegistryLoader",
]
