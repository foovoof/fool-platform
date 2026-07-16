"""
cyber/mapping/ontology_mapper.py

Ontology Mapper.

Maps cyber domain concepts to knowledge ontology concepts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cyber.mapping.models import (
    OntologyBinding,
    MappingMetadata,
    MappingType,
)


@dataclass(frozen=True)
class OntologyMappingResult:
    """Result of ontology mapping."""
    bindings: tuple[OntologyBinding, ...] = ()
    errors: tuple[str, ...] = ()
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "bindings": [b.to_dict() for b in self.bindings],
            "errors": list(self.errors),
        }


class CyberOntologyMapper:
    """
    Maps cyber domain concepts to knowledge ontology.
    
    Reuses existing Knowledge Ontology.
    Does NOT duplicate ontology definitions.
    """
    
    KNOWLEDGE_NAMESPACE = "knowledge"
    CYBER_NAMESPACE = "cyber"
    
    CONCEPT_MAPPINGS: dict[str, tuple[str, ...]] = {
        "indicator": ("Indicator", "Observable", "IOC"),
        "observable": ("Observable", "CyberObject", "Artifact"),
        "threat_actor": ("Actor", "ThreatActor", "Attacker"),
        "campaign": ("Campaign", "Operation", "Activity"),
        "malware": ("Malware", "MalwareFamily", "Tool"),
        "infrastructure": ("Infrastructure", "Host", "Network", "Service"),
        "vulnerability": ("Vulnerability", "Weakness", "CVE"),
        "tool": ("Tool", "Software", "Utility"),
        "technique": ("Technique", "AttackTechnique", "Method"),
        "tactic": ("Tactic", "AttackTactic", "Phase"),
        "procedure": ("Procedure", "AttackProcedure", "Method"),
        "attack_pattern": ("AttackPattern", "Technique", "Method"),
        "evidence": ("Evidence", "Proof", "Indicator"),
        "finding": ("Finding", "Observation", "Result"),
        "artifact": ("Artifact", "IOC", "Indicator"),
        "identity": ("Identity", "Entity", "Actor"),
        "victim": ("Victim", "Target", "Entity"),
        "organization": ("Organization", "Entity", "Group"),
    }
    
    def map_concept(
        self,
        cyber_concept: str,
        metadata: MappingMetadata | None = None,
    ) -> OntologyMappingResult:
        """
        Map a cyber concept to knowledge ontology concepts.
        
        Args:
            cyber_concept: Cyber concept to map
            metadata: Optional metadata
            
        Returns:
            Ontology mapping result with bindings
        """
        bindings = []
        errors = []
        
        knowledge_concepts = self.CONCEPT_MAPPINGS.get(cyber_concept.lower(), ())
        
        if not knowledge_concepts:
            errors.append(f"No mapping found for concept: {cyber_concept}")
            return OntologyMappingResult(
                bindings=(),
                errors=tuple(errors),
            )
        
        for concept in knowledge_concepts:
            binding = OntologyBinding(
                cyber_concept=cyber_concept,
                knowledge_concept=concept,
                cyber_namespace=self.CYBER_NAMESPACE,
                knowledge_namespace=self.KNOWLEDGE_NAMESPACE,
                mapping_type=MappingType.ONTOLOGY,
                metadata=metadata or MappingMetadata(),
            )
            bindings.append(binding)
        
        return OntologyMappingResult(
            bindings=tuple(bindings),
            errors=tuple(errors),
        )
    
    def get_mapping_for_entity(self, entity_type: str) -> tuple[str, ...]:
        """Get knowledge ontology concepts for an entity type."""
        return self.CONCEPT_MAPPINGS.get(entity_type.lower(), ())
    
    def is_mapped(self, cyber_concept: str) -> bool:
        """Check if a cyber concept has mappings."""
        return cyber_concept.lower() in self.CONCEPT_MAPPINGS


class OntologyBindingRegistry:
    """
    Registry for ontology bindings.
    
    Maintains a collection of ontology bindings.
    """
    
    def __init__(self) -> None:
        """Initialize registry."""
        self._bindings: dict[str, list[OntologyBinding]] = {}
    
    def register(self, binding: OntologyBinding) -> None:
        """Register an ontology binding."""
        concept = binding.cyber_concept.lower()
        if concept not in self._bindings:
            self._bindings[concept] = []
        self._bindings[concept].append(binding)
    
    def get(self, cyber_concept: str) -> list[OntologyBinding]:
        """Get bindings for a cyber concept."""
        return self._bindings.get(cyber_concept.lower(), []).copy()
    
    def list_concepts(self) -> list[str]:
        """List all registered concepts."""
        return list(self._bindings.keys())
    
    def count(self) -> int:
        """Count total bindings."""
        return sum(len(bindings) for bindings in self._bindings.values())
    
    def clear(self) -> None:
        """Clear all bindings."""
        self._bindings.clear()


class OntologyBindingValidator:
    """
    Validates ontology bindings.
    """
    
    def validate(self, binding: OntologyBinding) -> tuple[bool, list[str]]:
        """
        Validate an ontology binding.
        
        Args:
            binding: Binding to validate
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        if not binding.cyber_concept:
            errors.append("cyber_concept is required")
        
        if not binding.knowledge_concept:
            errors.append("knowledge_concept is required")
        
        if not binding.cyber_namespace:
            errors.append("cyber_namespace is required")
        
        if not binding.knowledge_namespace:
            errors.append("knowledge_namespace is required")
        
        return len(errors) == 0, errors
    
    def validate_registry(self, registry: OntologyBindingRegistry) -> tuple[bool, list[str]]:
        """
        Validate all bindings in a registry.
        
        Args:
            registry: Registry to validate
            
        Returns:
            Tuple of (is_valid, all_errors)
        """
        all_errors = []
        
        for concept, bindings in registry._bindings.items():
            for binding in bindings:
                is_valid, errors = self.validate(binding)
                if not is_valid:
                    all_errors.extend([f"{concept}: {e}" for e in errors])
        
        return len(all_errors) == 0, all_errors
