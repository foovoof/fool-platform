"""
platform/kernel/health/diagnostics.py

Health diagnostics and reporting.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .registry import HealthCheckRegistry
from .status import HealthCheckResult, HealthCheckType, HealthStatus, OverallHealthStatus


@dataclass(frozen=True)
class HealthDiagnostics:
    """
    Complete health diagnostics for the kernel.
    """
    overall_status: HealthStatus
    timestamp: str
    results: tuple[HealthCheckResult, ...]
    summary: dict
    metadata: dict = field(default_factory=dict)


class HealthDiagnosticsCollector:
    """
    Collects and aggregates health diagnostics.
    """
    
    def __init__(self, registry: HealthCheckRegistry) -> None:
        self._registry = registry
        self._history: list[HealthDiagnostics] = []
        self._max_history = 100
    
    def collect(self) -> HealthDiagnostics:
        """
        Collect complete health diagnostics.
        
        Returns:
            HealthDiagnostics with current health status
        """
        results = self._registry.run_all()
        
        # Determine overall status
        overall_status = self._determine_overall_status(results)
        
        # Build summary
        summary = self._build_summary(results)
        
        diagnostics = HealthDiagnostics(
            overall_status=overall_status,
            timestamp=datetime.now(timezone.utc).isoformat(),
            results=tuple(results),
            summary=summary,
        )
        
        # Store in history
        self._history.append(diagnostics)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        return diagnostics
    
    def _determine_overall_status(self, results: list[HealthCheckResult]) -> HealthStatus:
        """Determine overall health status from individual results."""
        if not results:
            return HealthStatus.UNKNOWN
        
        statuses = [r.status for r in results]
        
        if all(s == HealthStatus.HEALTHY for s in statuses):
            return HealthStatus.HEALTHY
        
        if any(s == HealthStatus.UNHEALTHY for s in statuses):
            return HealthStatus.UNHEALTHY
        
        if any(s == HealthStatus.DEGRADED for s in statuses):
            return HealthStatus.DEGRADED
        
        return HealthStatus.UNKNOWN
    
    def _build_summary(self, results: list[HealthCheckResult]) -> dict:
        """Build summary statistics from results."""
        total = len(results)
        healthy = sum(1 for r in results if r.status == HealthStatus.HEALTHY)
        degraded = sum(1 for r in results if r.status == HealthStatus.DEGRADED)
        unhealthy = sum(1 for r in results if r.status == HealthStatus.UNHEALTHY)
        
        # Group by type
        by_type: dict[str, dict] = {}
        for check_type in HealthCheckType:
            type_results = [r for r in results if r.check_type == check_type]
            if type_results:
                type_healthy = sum(1 for r in type_results if r.status == HealthStatus.HEALTHY)
                by_type[check_type.value] = {
                    "total": len(type_results),
                    "healthy": type_healthy,
                    "unhealthy": len(type_results) - type_healthy,
                }
        
        return {
            "total_checks": total,
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy,
            "by_type": by_type,
        }
    
    def get_history(self, limit: int | None = None) -> list[HealthDiagnostics]:
        """Get health diagnostics history."""
        if limit:
            return self._history[-limit:]
        return self._history.copy()
    
    def get_trend(self, limit: int = 10) -> list[HealthStatus]:
        """Get health status trend over recent history."""
        history = self._history[-limit:]
        return [h.overall_status for h in history]


@dataclass
class HealthReport:
    """
    Human-readable health report.
    """
    diagnostics: HealthDiagnostics
    include_details: bool = True
    
    def format_text(self) -> str:
        """Format report as plain text."""
        lines = []
        d = self.diagnostics
        
        lines.append("=" * 60)
        lines.append("FOOL Platform Kernel Health Report")
        lines.append("=" * 60)
        lines.append(f"Status: {d.overall_status.value.upper()}")
        lines.append(f"Timestamp: {d.timestamp}")
        lines.append("")
        
        lines.append("Summary:")
        lines.append(f"  Total Checks: {d.summary['total_checks']}")
        lines.append(f"  Healthy: {d.summary['healthy']}")
        lines.append(f"  Degraded: {d.summary['degraded']}")
        lines.append(f"  Unhealthy: {d.summary['unhealthy']}")
        lines.append("")
        
        if self.include_details:
            lines.append("Check Results:")
            for result in d.results:
                status_icon = "✓" if result.status == HealthStatus.HEALTHY else "✗"
                lines.append(f"  [{status_icon}] {result.name}: {result.status.value}")
                if result.message:
                    lines.append(f"       {result.message}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)


__all__ = [
    "HealthDiagnostics",
    "HealthDiagnosticsCollector",
    "HealthReport",
]
