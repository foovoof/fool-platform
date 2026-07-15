"""
platform/kernel/registries/__init__.py

Registry loaders for FOOL Platform registries.

Loads agent, capability, workflow, concept, and contract registries
from YAML and JSON files.
"""
from .agent_registry import AgentRegistryLoader
from .capability_registry import CapabilityRegistryLoader
from .concept_registry import ConceptRegistryLoader
from .contract_registry import ContractRegistryLoader
from .workflow_registry import WorkflowRegistryLoader

__all__ = [
    "AgentRegistryLoader",
    "CapabilityRegistryLoader",
    "ConceptRegistryLoader",
    "ContractRegistryLoader",
    "WorkflowRegistryLoader",
]
