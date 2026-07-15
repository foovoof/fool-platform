"""
intelligence/registry/integration.py

Registry Integration.

Integrates with existing registries:
- Agent Registry
- Capability Registry
- Workflow Registry

NOTE: This is an integration layer, NOT a duplicate registry.
"""
from typing import Any


class RegistryIntegration:
    """
    Integrates with existing registries.
    
    Does NOT implement its own registry.
    Only delegates to existing registries.
    """
    
    def __init__(
        self,
        agent_registry: Any = None,
        capability_registry: Any = None,
        workflow_registry: Any = None,
    ) -> None:
        """
        Initialize registry integration.
        
        Args:
            agent_registry: Agent registry instance
            capability_registry: Capability registry instance
            workflow_registry: Workflow registry instance
        """
        self._agent_registry = agent_registry
        self._capability_registry = capability_registry
        self._workflow_registry = workflow_registry
    
    @property
    def has_agent_registry(self) -> bool:
        """Check if agent registry is available."""
        return self._agent_registry is not None
    
    @property
    def has_capability_registry(self) -> bool:
        """Check if capability registry is available."""
        return self._capability_registry is not None
    
    @property
    def has_workflow_registry(self) -> bool:
        """Check if workflow registry is available."""
        return self._workflow_registry is not None
    
    def get_agent(self, agent_id: str) -> dict[str, Any] | None:
        """
        Get agent from registry.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent data or None
        """
        if not self._agent_registry:
            return None
        
        if hasattr(self._agent_registry, "get"):
            return self._agent_registry.get(agent_id)
        if hasattr(self._agent_registry, "get_agent"):
            return self._agent_registry.get_agent(agent_id)
        
        return None
    
    def list_agents(self) -> list[dict[str, Any]]:
        """List agents from registry."""
        if not self._agent_registry:
            return []
        
        if hasattr(self._agent_registry, "list"):
            return self._agent_registry.list()
        if hasattr(self._agent_registry, "list_agents"):
            return self._agent_registry.list_agents()
        
        return []
    
    def get_capability(self, capability_id: str) -> dict[str, Any] | None:
        """
        Get capability from registry.
        
        Args:
            capability_id: Capability ID
            
        Returns:
            Capability data or None
        """
        if not self._capability_registry:
            return None
        
        if hasattr(self._capability_registry, "get"):
            return self._capability_registry.get(capability_id)
        if hasattr(self._capability_registry, "get_capability"):
            return self._capability_registry.get_capability(capability_id)
        
        return None
    
    def list_capabilities(self) -> list[dict[str, Any]]:
        """List capabilities from registry."""
        if not self._capability_registry:
            return []
        
        if hasattr(self._capability_registry, "list"):
            return self._capability_registry.list()
        if hasattr(self._capability_registry, "list_capabilities"):
            return self._capability_registry.list_capabilities()
        
        return []
    
    def get_workflow(self, workflow_id: str) -> dict[str, Any] | None:
        """
        Get workflow from registry.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow data or None
        """
        if not self._workflow_registry:
            return None
        
        if hasattr(self._workflow_registry, "get"):
            return self._workflow_registry.get(workflow_id)
        if hasattr(self._workflow_registry, "get_workflow"):
            return self._workflow_registry.get_workflow(workflow_id)
        
        return None
    
    def list_workflows(self) -> list[dict[str, Any]]:
        """List workflows from registry."""
        if not self._workflow_registry:
            return []
        
        if hasattr(self._workflow_registry, "list"):
            return self._workflow_registry.list()
        if hasattr(self._workflow_registry, "list_workflows"):
            return self._workflow_registry.list_workflows()
        
        return []
