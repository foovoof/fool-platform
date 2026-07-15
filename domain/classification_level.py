"""
domain/classification_level.py

ClassificationLevel domain model.
Mirrors contracts/common/common-defs.schema.json field-for-field.
"""
from .common import ClassificationLevelValue


class ClassificationLevel:
    """
    Sensitivity classification level for domain objects.
    
    Classification controls access and handling requirements:
    - public: No restrictions
    - internal: Internal use only
    - restricted: Need-to-know access
    - confidential: Strict access controls
    """
    
    def __init__(self, value: ClassificationLevelValue) -> None:
        self._value = value
    
    @classmethod
    def public(cls) -> "ClassificationLevel":
        return cls(ClassificationLevelValue.PUBLIC)
    
    @classmethod
    def internal(cls) -> "ClassificationLevel":
        return cls(ClassificationLevelValue.INTERNAL)
    
    @classmethod
    def restricted(cls) -> "ClassificationLevel":
        return cls(ClassificationLevelValue.RESTRICTED)
    
    @classmethod
    def confidential(cls) -> "ClassificationLevel":
        return cls(ClassificationLevelValue.CONFIDENTIAL)
    
    @property
    def value(self) -> ClassificationLevelValue:
        return self._value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassificationLevel):
            return NotImplemented
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __repr__(self) -> str:
        return f"ClassificationLevel({self._value.value})"
    
    def requires_access_control(self) -> bool:
        """Returns True if this classification requires access control."""
        return self._value != ClassificationLevelValue.PUBLIC


__all__ = ["ClassificationLevel"]
