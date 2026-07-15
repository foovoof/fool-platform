"""
domain/confidence_score.py

ConfidenceScore domain model with scoring and level derivation.
Mirrors contracts/confidence/scoring-model.schema.json and
contracts/confidence/confidence-model.schema.json.
"""
from dataclasses import dataclass
from .common import ConfidenceLevel, DomainInvariantError, new_id, utc_now


@dataclass(frozen=True)
class ConfidenceMethod:
    """Named method used to assess confidence."""
    name: str


# Predefined confidence methods
class ConfidenceMethods:
    MANUAL_REVIEW = ConfidenceMethod("manual_review")
    AUTOMATED_ANALYSIS = ConfidenceMethod("automated_analysis")
    IDENTIFIER_RESOLUTION = ConfidenceMethod("identifier_resolution")
    SOURCE_RELIABILITY = ConfidenceMethod("source_reliability")
    INFERENCE = ConfidenceMethod("inference")
    DERIVED = ConfidenceMethod("derived")


def _derive_level(score: float) -> ConfidenceLevel:
    """Derive confidence level from score using standard buckets."""
    if score < 0.2:
        return ConfidenceLevel.VERY_LOW
    elif score < 0.4:
        return ConfidenceLevel.LOW
    elif score < 0.6:
        return ConfidenceLevel.MODERATE
    elif score < 0.8:
        return ConfidenceLevel.HIGH
    else:
        return ConfidenceLevel.VERY_HIGH


@dataclass(frozen=True)
class ConfidenceScore:
    """
    A scored assessment with derived level and method metadata.
    
    Every assessed field in the domain carries a ConfidenceScore rather
    than a bare boolean, per the Confidence Everywhere principle.
    """
    score: float
    level: ConfidenceLevel
    method: ConfidenceMethod
    assessed_at: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise DomainInvariantError(
                f"ConfidenceScore.score must be between 0.0 and 1.0, got {self.score}"
            )

    @classmethod
    def create(
        cls,
        score: float,
        method: ConfidenceMethod,
        evidence_refs: tuple[str, ...] | None = None,
        assessed_at: str | None = None,
    ) -> "ConfidenceScore":
        """
        Factory method to create a ConfidenceScore with derived level.
        
        Args:
            score: Numeric confidence between 0.0 and 1.0
            method: Named assessment method
            evidence_refs: Optional tuple of evidence reference IDs
            assessed_at: Optional timestamp, defaults to now
            
        Returns:
            ConfidenceScore with derived level
        """
        return cls(
            score=score,
            level=_derive_level(score),
            method=method,
            assessed_at=assessed_at or utc_now(),
            evidence_refs=evidence_refs or (),
        )
    
    def with_evidence(self, *refs: str) -> "ConfidenceScore":
        """Return a new ConfidenceScore with additional evidence references."""
        return ConfidenceScore(
            score=self.score,
            level=self.level,
            method=self.method,
            assessed_at=self.assessed_at,
            evidence_refs=(*self.evidence_refs, *refs),
        )
    
    def is_high_confidence(self) -> bool:
        """Returns True if confidence is high or very high."""
        return self.level in (ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH)


__all__ = [
    "ConfidenceLevel",
    "ConfidenceMethod",
    "ConfidenceMethods",
    "ConfidenceScore",
]
