"""
product_suite/contracts/contract.py

Cross Product Contracts Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from product_suite.registry.base import SuiteBase
from product_suite.registry.enums import ContractType, CompatibilityLevel


@dataclass(frozen=True)
class ContractInput:
    """Contract input definition."""
    name: str = ""
    type: str = ""
    required: bool = True
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "description": self.description,
        }


@dataclass(frozen=True)
class ContractOutput:
    """Contract output definition."""
    name: str = ""
    type: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
        }


@dataclass(frozen=True)
class ContractEvent:
    """Contract event definition."""
    event_type: str = ""
    source: str = ""
    target: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "target": self.target,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class ContractReference:
    """Contract reference definition."""
    ref_type: str = ""
    source: str = ""
    target: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_type": self.ref_type,
            "source": self.source,
            "target": self.target,
            "description": self.description,
        }


@dataclass(frozen=True)
class ReplayRule:
    """Contract replay rules."""
    rule_id: str = ""
    description: str = ""
    deterministic: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "description": self.description,
            "deterministic": self.deterministic,
        }


@dataclass(frozen=True)
class ProductContract(SuiteBase):
    """Cross product contract."""
    contract_type: str = ""
    name: str = ""
    description: str = ""
    source_product: str = ""
    target_product: str = ""
    version: str = "1.0"
    compatibility: str = "full"
    inputs: tuple[ContractInput, ...] = field(default_factory=tuple)
    outputs: tuple[ContractOutput, ...] = field(default_factory=tuple)
    events: tuple[ContractEvent, ...] = field(default_factory=tuple)
    references: tuple[ContractReference, ...] = field(default_factory=tuple)
    replay_rules: tuple[ReplayRule, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "contract_type": self.contract_type,
            "name": self.name,
            "description": self.description,
            "source_product": self.source_product,
            "target_product": self.target_product,
            "version": self.version,
            "compatibility": self.compatibility,
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [o.to_dict() for o in self.outputs],
            "events": [e.to_dict() for e in self.events],
            "references": [r.to_dict() for r in self.references],
            "replay_rules": [r.to_dict() for r in self.replay_rules],
            "metadata": self.metadata,
        })
        return base


@dataclass(frozen=True)
class ContractCompatibilityMatrix(SuiteBase):
    """Contract compatibility matrix."""
    contracts: tuple[ProductContract, ...] = field(default_factory=tuple)
    compatibility_matrix: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "contracts": [c.to_dict() for c in self.contracts],
            "compatibility_matrix": list(self.compatibility_matrix),
        })
        return base
