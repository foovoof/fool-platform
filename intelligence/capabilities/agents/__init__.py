"""
intelligence/capabilities/agents/__init__.py

Intelligence Capability Agents.

Reference agents for intelligence capabilities.
"""
from intelligence.capabilities.agents.base import BaseAgent
from intelligence.capabilities.agents.research import ResearchAgent
from intelligence.capabilities.agents.discovery import DiscoveryAgent
from intelligence.capabilities.agents.extraction import ExtractionAgent
from intelligence.capabilities.agents.correlation import CorrelationAgent
from intelligence.capabilities.agents.investigation import InvestigationAgent
from intelligence.capabilities.agents.assessment import AssessmentAgent
from intelligence.capabilities.agents.reporting import ReportingAgent
from intelligence.capabilities.agents.timeline import TimelineAgent
from intelligence.capabilities.agents.evidence_analysis import EvidenceAnalysisAgent


class AgentFactory:
    """Factory for creating capability agents."""
    
    _agents: dict[str, type[BaseAgent]] = {
        "research": ResearchAgent,
        "discovery": DiscoveryAgent,
        "extraction": ExtractionAgent,
        "correlation": CorrelationAgent,
        "investigation": InvestigationAgent,
        "assessment": AssessmentAgent,
        "reporting": ReportingAgent,
        "timeline": TimelineAgent,
        "evidence_analysis": EvidenceAnalysisAgent,
    }
    
    @classmethod
    def create(cls, agent_type: str) -> BaseAgent | None:
        """Create an agent by type."""
        agent_class = cls._agents.get(agent_type)
        if agent_class:
            return agent_class()
        return None
    
    @classmethod
    def register(cls, agent_type: str, agent_class: type[BaseAgent]) -> None:
        """Register a new agent type."""
        cls._agents[agent_type] = agent_class
    
    @classmethod
    def list_types(cls) -> list[str]:
        """List available agent types."""
        return list(cls._agents.keys())


__all__ = [
    "BaseAgent",
    "ResearchAgent",
    "DiscoveryAgent",
    "ExtractionAgent",
    "CorrelationAgent",
    "InvestigationAgent",
    "AssessmentAgent",
    "ReportingAgent",
    "TimelineAgent",
    "EvidenceAnalysisAgent",
    "AgentFactory",
]
