"""
platform/kernel/config/environment.py

Environment profile management for configuration.
"""
from enum import Enum, auto


class EnvironmentProfile(Enum):
    """
    Environment profiles for configuration.
    
    Each profile may have different default values and behavior.
    """
    LOCAL = auto()
    """Local development environment."""
    DEVELOPMENT = auto()
    """Shared development environment."""
    TESTING = auto()
    """Automated testing environment."""
    PRODUCTION = auto()
    """Production environment."""
    
    @classmethod
    def from_string(cls, value: str) -> "EnvironmentProfile":
        """
        Parse an environment string to profile.
        
        Args:
            value: String value (e.g., "local", "dev", "test", "prod")
            
        Returns:
            Corresponding EnvironmentProfile
        """
        mapping = {
            "local": cls.LOCAL,
            "development": cls.DEVELOPMENT,
            "dev": cls.DEVELOPMENT,
            "test": cls.TESTING,
            "testing": cls.TESTING,
            "prod": cls.PRODUCTION,
            "production": cls.PRODUCTION,
        }
        lower = value.lower().strip()
        if lower not in mapping:
            raise ValueError(f"Unknown environment: {value}")
        return mapping[lower]
    
    @property
    def is_production(self) -> bool:
        """Returns True if this is a production environment."""
        return self == EnvironmentProfile.PRODUCTION
    
    @property
    def is_development(self) -> bool:
        """Returns True if this is a development environment."""
        return self == EnvironmentProfile.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Returns True if this is a testing environment."""
        return self == EnvironmentProfile.TESTING
    
    @property
    def is_local(self) -> bool:
        """Returns True if this is a local environment."""
        return self == EnvironmentProfile.LOCAL


class EnvironmentDetector:
    """
    Detects the current environment from various sources.
    """
    
    @staticmethod
    def detect_from_env() -> EnvironmentProfile:
        """
        Detect environment from environment variables.
        
        Checks FOOL_ENVIRONMENT, NODE_ENV, and ENV variables.
        """
        import os
        
        # Check FOOL_ENVIRONMENT first
        fool_env = os.environ.get("FOOL_ENVIRONMENT")
        if fool_env:
            return EnvironmentProfile.from_string(fool_env)
        
        # Check NODE_ENV
        node_env = os.environ.get("NODE_ENV")
        if node_env:
            return EnvironmentProfile.from_string(node_env)
        
        # Check ENV
        env = os.environ.get("ENV")
        if env:
            return EnvironmentProfile.from_string(env)
        
        # Default to local
        return EnvironmentProfile.LOCAL


__all__ = [
    "EnvironmentDetector",
    "EnvironmentProfile",
]
