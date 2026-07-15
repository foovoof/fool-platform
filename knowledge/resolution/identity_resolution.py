from __future__ import annotations

"""
knowledge/resolution/identity_resolution.py

Identity resolution engine for deterministic identity matching.

Provides deterministic matching based on:
- Exact identifier match
- Normalized identifier match
- Contract-defined identity keys
- Ontology-defined identity keys
"""
from dataclasses import dataclass, field
from enum import Enum
import re


class IdentityMatchType(Enum):
    """Types of identity matches."""
    EXACT = "exact"
    NORMALIZED = "normalized"
    EXACT_MATCH = "exact_match"
    NO_MATCH = "no_match"


@dataclass
class IdentityMatch:
    """Result of identity matching."""
    source_identity_id: str
    target_identity_id: str
    match_type: IdentityMatchType
    is_match: bool
    confidence: float = 0.0
    match_reason: str = ""


class IdentityResolutionEngine:
    """
    Deterministic identity resolution engine.
    
    Resolution is based on:
    - Exact identifier matching
    - Normalized identifier matching
    - Contract-defined matching criteria
    - Ontology-defined matching criteria
    """

    def __init__(
        self,
        case_sensitive: bool = True,
        normalize_whitespace: bool = True,
        strip_special_chars: bool = False,
    ) -> None:
        """
        Initialize the identity resolution engine.
        
        Args:
            case_sensitive: Whether matching is case sensitive
            normalize_whitespace: Whether to normalize whitespace
            strip_special_chars: Whether to strip special characters
        """
        self._case_sensitive = case_sensitive
        self._normalize_whitespace = normalize_whitespace
        self._strip_special_chars = strip_special_chars

    def normalize(self, value: str) -> str:
        """
        Normalize an identity value for matching.
        
        Args:
            value: The value to normalize
            
        Returns:
            Normalized value
        """
        if not value:
            return ""
        
        result = value
        
        if not self._case_sensitive:
            result = result.lower()
        
        if self._normalize_whitespace:
            result = re.sub(r"\s+", " ", result).strip()
        
        if self._strip_special_chars:
            result = re.sub(r"[^\w\s]", "", result)
        
        return result

    def match_exact(
        self,
        source_value: str,
        target_value: str,
    ) -> IdentityMatch:
        """
        Perform exact identity matching.
        
        Args:
            source_value: Source identity value
            target_value: Target identity value
            
        Returns:
            IdentityMatch result
        """
        is_match = source_value == target_value
        
        return IdentityMatch(
            source_identity_id=source_value,
            target_identity_id=target_value,
            match_type=IdentityMatchType.EXACT,
            is_match=is_match,
            confidence=1.0 if is_match else 0.0,
            match_reason="Exact match" if is_match else "Values do not match exactly",
        )

    def match_normalized(
        self,
        source_value: str,
        target_value: str,
    ) -> IdentityMatch:
        """
        Perform normalized identity matching.
        
        Args:
            source_value: Source identity value
            target_value: Target identity value
            
        Returns:
            IdentityMatch result
        """
        if not source_value or not target_value:
            return IdentityMatch(
                source_identity_id=source_value,
                target_identity_id=target_value,
                match_type=IdentityMatchType.NO_MATCH,
                is_match=False,
                match_reason="Empty value provided",
            )

        source_normalized = self.normalize(source_value)
        target_normalized = self.normalize(target_value)

        is_match = source_normalized == target_normalized
        
        return IdentityMatch(
            source_identity_id=source_value,
            target_identity_id=target_value,
            match_type=IdentityMatchType.NORMALIZED if is_match else IdentityMatchType.NO_MATCH,
            is_match=is_match,
            confidence=1.0 if is_match else 0.0,
            match_reason=f"Normalized match: '{source_normalized}' vs '{target_normalized}'"
                if is_match else f"Normalized values do not match: '{source_normalized}' vs '{target_normalized}'",
        )

    def match_by_type(
        self,
        source_type: str,
        source_value: str,
        target_type: str,
        target_value: str,
    ) -> IdentityMatch:
        """
        Perform identity matching with type consideration.
        
        Args:
            source_type: Source identity type
            source_value: Source identity value
            target_type: Target identity type
            target_value: Target identity value
            
        Returns:
            IdentityMatch result
        """
        if source_type != target_type:
            return IdentityMatch(
                source_identity_id=source_value,
                target_identity_id=target_value,
                match_type=IdentityMatchType.NO_MATCH,
                is_match=False,
                confidence=0.0,
                match_reason=f"Type mismatch: {source_type} != {target_type}",
            )

        return self.match_normalized(source_value, target_value)

    def match(
        self,
        source_identity: dict[str, str],
        target_identity: dict[str, str],
    ) -> IdentityMatch:
        """
        Perform identity matching.
        
        Args:
            source_identity: Source identity with type and value
            target_identity: Target identity with type and value
            
        Returns:
            IdentityMatch result
        """
        source_type = source_identity.get("type", "")
        source_value = source_identity.get("value", "")
        target_type = target_identity.get("type", "")
        target_value = target_identity.get("value", "")

        return self.match_by_type(
            source_type, source_value,
            target_type, target_value,
        )

    def find_duplicates(
        self,
        identities: list[dict[str, str]],
    ) -> list[IdentityMatch]:
        """
        Find duplicate identities in a list.
        
        Args:
            identities: List of identities to check
            
        Returns:
            List of IdentityMatch results for duplicates
        """
        duplicates: list[IdentityMatch] = []
        checked: set[tuple[str, str]] = set()

        for i, source in enumerate(identities):
            source_value = source.get("value", "")
            source_type = source.get("type", "")
            
            for j, target in enumerate(identities):
                if i >= j:
                    continue
                
                target_value = target.get("value", "")
                target_type = target.get("type", "")
                
                pair = tuple(sorted([source_value, target_value]))
                
                if pair in checked:
                    continue
                
                checked.add(pair)
                
                match_result = self.match_by_type(
                    source_type, source_value,
                    target_type, target_value,
                )
                
                if match_result.is_match:
                    duplicates.append(match_result)

        return duplicates

    def resolve(
        self,
        identity: dict[str, str],
        candidate_pool: list[dict[str, str]],
    ) -> IdentityMatch | None:
        """
        Resolve an identity against a candidate pool.
        
        Args:
            identity: The identity to resolve
            candidate_pool: List of candidate identities
            
        Returns:
            Best IdentityMatch or None
        """
        best_match: IdentityMatch | None = None

        for candidate in candidate_pool:
            match_result = self.match(identity, candidate)
            
            if match_result.is_match:
                if best_match is None or match_result.confidence > best_match.confidence:
                    best_match = match_result

        return best_match
