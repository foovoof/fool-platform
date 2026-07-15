"""
platform/kernel/config/validator.py

Configuration validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from ..kernel_exceptions import ConfigurationValidationError

T = TypeVar("T")


@dataclass
class ValidationError:
    """A single configuration validation error."""
    path: str
    message: str
    value: Any = None


@dataclass
class ValidationResult:
    """Result of configuration validation."""
    valid: bool
    errors: list[ValidationError]
    
    def raise_if_invalid(self) -> None:
        """Raise ConfigurationValidationError if validation failed."""
        if not self.valid:
            messages = [f"{e.path}: {e.message}" for e in self.errors]
            raise ConfigurationValidationError(
                f"Configuration validation failed: {'; '.join(messages)}"
            )


class ConfigValidator:
    """
    Validates configuration against defined rules.
    """
    
    def __init__(self) -> None:
        self._rules: list[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self._rules.append(rule)
    
    def validate(self, config: dict) -> ValidationResult:
        """
        Validate configuration against all rules.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            ValidationResult with errors if any
        """
        errors: list[ValidationError] = []
        
        for rule in self._rules:
            error = rule.validate(config)
            if error:
                errors.append(error)
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
        )
    
    def add_required(self, path: str) -> "ConfigValidator":
        """Add a required field rule."""
        self._rules.append(RequiredRule(path))
        return self
    
    def add_type(self, path: str, expected_type: type) -> "ConfigValidator":
        """Add a type check rule."""
        self._rules.append(TypeRule(path, expected_type))
        return self
    
    def add_range(
        self, path: str, min_value: Any = None, max_value: Any = None
    ) -> "ConfigValidator":
        """Add a range validation rule."""
        self._rules.append(RangeRule(path, min_value, max_value))
        return self
    
    def add_pattern(self, path: str, pattern: str) -> "ConfigValidator":
        """Add a pattern match rule."""
        self._rules.append(PatternRule(path, pattern))
        return self


class ValidationRule:
    """
    Base class for validation rules.
    """
    
    def __init__(self, path: str) -> None:
        self._path = path
    
    @property
    def path(self) -> str:
        """The configuration path this rule applies to."""
        return self._path
    
    def validate(self, config: dict) -> ValidationError | None:
        """Validate the configuration. Returns error or None."""
        raise NotImplementedError


class RequiredRule(ValidationRule):
    """Rule that requires a field to be present."""
    
    def validate(self, config: dict) -> ValidationError | None:
        value = self._get_value(config)
        if value is None:
            return ValidationError(
                path=self._path,
                message="Required field is missing",
            )
        return None
    
    def _get_value(self, config: dict) -> Any:
        keys = self._path.split(".")
        value = config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value


class TypeRule(ValidationRule):
    """Rule that validates a field's type."""
    
    def __init__(self, path: str, expected_type: type) -> None:
        super().__init__(path)
        self._expected_type = expected_type
    
    def validate(self, config: dict) -> ValidationError | None:
        value = self._get_value(config)
        if value is not None and not isinstance(value, self._expected_type):
            return ValidationError(
                path=self._path,
                message=f"Expected type {self._expected_type.__name__}, got {type(value).__name__}",
                value=value,
            )
        return None
    
    def _get_value(self, config: dict) -> Any:
        keys = self._path.split(".")
        value = config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value


class RangeRule(ValidationRule):
    """Rule that validates a value is within a range."""
    
    def __init__(
        self, path: str, min_value: Any = None, max_value: Any = None
    ) -> None:
        super().__init__(path)
        self._min_value = min_value
        self._max_value = max_value
    
    def validate(self, config: dict) -> ValidationError | None:
        value = self._get_value(config)
        if value is None:
            return None  # Skip if not present
        
        if self._min_value is not None and value < self._min_value:
            return ValidationError(
                path=self._path,
                message=f"Value {value} is less than minimum {self._min_value}",
                value=value,
            )
        
        if self._max_value is not None and value > self._max_value:
            return ValidationError(
                path=self._path,
                message=f"Value {value} is greater than maximum {self._max_value}",
                value=value,
            )
        
        return None
    
    def _get_value(self, config: dict) -> Any:
        keys = self._path.split(".")
        value = config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value


class PatternRule(ValidationRule):
    """Rule that validates a string matches a pattern."""
    
    def __init__(self, path: str, pattern: str) -> None:
        super().__init__(path)
        self._pattern = pattern
    
    def validate(self, config: dict) -> ValidationError | None:
        value = self._get_value(config)
        if value is None:
            return None  # Skip if not present
        
        if not isinstance(value, str):
            return ValidationError(
                path=self._path,
                message=f"Expected string for pattern matching, got {type(value).__name__}",
                value=value,
            )
        
        import re
        if not re.match(self._pattern, value):
            return ValidationError(
                path=self._path,
                message=f"Value does not match pattern {self._pattern}",
                value=value,
            )
        
        return None
    
    def _get_value(self, config: dict) -> Any:
        keys = self._path.split(".")
        value = config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value


__all__ = [
    "ConfigValidator",
    "PatternRule",
    "RangeRule",
    "RequiredRule",
    "TypeRule",
    "ValidationError",
    "ValidationResult",
    "ValidationRule",
]
