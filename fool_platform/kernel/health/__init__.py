"""
platform/kernel/health/__init__.py

Health check system for the FOOL Platform kernel.
"""
from .checks import CompositeHealthCheck, LambdaHealthCheck, create_lambda_check
from .diagnostics import HealthDiagnostics, HealthDiagnosticsCollector, HealthReport
from .liveness import DIContainerLivenessCheck, KernelLivenessCheck, LivenessCheck
from .readiness import (
    KernelReadinessCheck,
    ReadinessCheck,
    RegistryReadinessCheck,
)
from .registry import HealthCheckRegistry
from .shutdown import (
    ResourcesReleasedCheck,
    ServicesDisposedCheck,
    ShutdownCheck,
)
from .startup import BootstrapCompleteCheck, ConfigValidCheck, StartupCheck
from .status import (
    HealthCheckResult,
    HealthCheckType,
    HealthStatus,
    OverallHealthStatus,
)

__all__ = [
    "BootstrapCompleteCheck",
    "CompositeHealthCheck",
    "ConfigValidCheck",
    "DIContainerLivenessCheck",
    "HealthCheckRegistry",
    "HealthCheckResult",
    "HealthCheckType",
    "HealthDiagnostics",
    "HealthDiagnosticsCollector",
    "HealthReport",
    "HealthStatus",
    "KernelLivenessCheck",
    "KernelReadinessCheck",
    "LambdaHealthCheck",
    "LivenessCheck",
    "OverallHealthStatus",
    "ReadinessCheck",
    "RegistryReadinessCheck",
    "ResourcesReleasedCheck",
    "ServicesDisposedCheck",
    "ShutdownCheck",
    "StartupCheck",
    "create_lambda_check",
]
