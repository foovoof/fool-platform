"""
fool_platform/orchestration/planner/workflow_planner.py

Workflow planning - dependency analysis and step ordering.
"""
from dataclasses import dataclass, field
from typing import Any

from fool_platform.orchestration.orchestration_exceptions import WorkflowPlanningError
from fool_platform.orchestration.registry.workflow_registry import (
    StepDefinition,
    WorkflowDefinition,
)


@dataclass
class WorkflowPlan:
    """Plan for executing a workflow."""
    workflow_id: str
    workflow_version: str
    entry_steps: list[str] = field(default_factory=list)
    terminal_steps: list[str] = field(default_factory=list)
    step_order: list[str] = field(default_factory=list)
    dependencies: dict[str, set[str]] = field(default_factory=dict)
    reverse_dependencies: dict[str, set[str]] = field(default_factory=dict)


class WorkflowPlanner:
    """
    Creates execution plans for workflows.
    
    Analyzes step dependencies, detects cycles, and determines execution order.
    """

    def create_plan(self, workflow: WorkflowDefinition) -> WorkflowPlan:
        """
        Create an execution plan for a workflow.
        
        Args:
            workflow: The workflow definition
            
        Returns:
            WorkflowPlan with execution order and dependencies
            
        Raises:
            WorkflowPlanningError: If workflow planning fails
        """
        self.validate_step_dependencies(workflow)
        
        entry_steps = self.identify_entry_steps(workflow)
        terminal_steps = self.identify_terminal_steps(workflow)
        step_order = self.topologically_order_steps(workflow)
        dependencies = self._build_dependency_map(workflow)
        reverse_deps = self._build_reverse_dependency_map(workflow)
        
        return WorkflowPlan(
            workflow_id=workflow.workflow_id,
            workflow_version=workflow.version,
            entry_steps=entry_steps,
            terminal_steps=terminal_steps,
            step_order=step_order,
            dependencies=dependencies,
            reverse_dependencies=reverse_deps,
        )

    def validate_step_dependencies(self, workflow: WorkflowDefinition) -> bool:
        """
        Validate that all step dependencies are satisfied.
        
        Args:
            workflow: The workflow definition
            
        Returns:
            True if all dependencies are valid
            
        Raises:
            WorkflowPlanningError: If dependencies are invalid
        """
        step_ids = {step.step_id for step in workflow.steps}
        errors: list[str] = []
        
        for step in workflow.steps:
            for dep in step.depends_on:
                if dep not in step_ids:
                    errors.append(f"Step {step.step_id} depends on unknown step {dep}")
        
        if self.detect_cycles(workflow):
            errors.append("Workflow contains cyclic dependencies")
        
        if errors:
            raise WorkflowPlanningError(
                workflow_id=workflow.workflow_id,
                reason="Dependency validation failed",
                details=errors,
            )
        
        return True

    def topologically_order_steps(self, workflow: WorkflowDefinition) -> list[str]:
        """
        Order steps topologically based on dependencies.
        
        Args:
            workflow: The workflow definition
            
        Returns:
            List of step IDs in execution order
            
        Raises:
            WorkflowPlanningError: If cycles detected
        """
        if self.detect_cycles(workflow):
            raise WorkflowPlanningError(
                workflow_id=workflow.workflow_id,
                reason="Cannot order steps with cyclic dependencies",
            )
        
        dependencies = self._build_dependency_map(workflow)
        in_degree = {step_id: len(deps) for step_id, deps in dependencies.items()}
        
        ordered = []
        queue = [sid for sid, deg in in_degree.items() if deg == 0]
        
        while queue:
            current = queue.pop(0)
            ordered.append(current)
            
            for step in workflow.steps:
                if current in step.depends_on:
                    in_degree[step.step_id] -= 1
                    if in_degree[step.step_id] == 0 and step.step_id not in ordered:
                        queue.append(step.step_id)
        
        return ordered

    def detect_cycles(self, workflow: WorkflowDefinition) -> bool:
        """
        Detect cyclic dependencies in workflow.
        
        Args:
            workflow: The workflow definition
            
        Returns:
            True if cycles are detected
        """
        dependencies = self._build_dependency_map(workflow)
        visited: set[str] = set()
        rec_stack: set[str] = set()
        
        def has_cycle(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)
            
            for dep in dependencies.get(step_id, set()):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(step_id)
            return False
        
        for step in workflow.steps:
            if step.step_id not in visited:
                if has_cycle(step.step_id):
                    return True
        
        return False

    def identify_entry_steps(self, workflow: WorkflowDefinition) -> list[str]:
        """
        Identify steps with no dependencies (entry points).
        
        Args:
            workflow: The workflow definition
            
        Returns:
            List of entry step IDs
        """
        dependencies = self._build_dependency_map(workflow)
        entry_steps = []
        
        for step in workflow.steps:
            if not dependencies.get(step.step_id):
                entry_steps.append(step.step_id)
        
        return entry_steps

    def identify_terminal_steps(self, workflow: WorkflowDefinition) -> list[str]:
        """
        Identify steps that no other step depends on.
        
        Args:
            workflow: The workflow definition
            
        Returns:
            List of terminal step IDs
        """
        reverse_deps = self._build_reverse_dependency_map(workflow)
        terminal_steps = []
        
        for step in workflow.steps:
            if not reverse_deps.get(step.step_id):
                terminal_steps.append(step.step_id)
        
        return terminal_steps

    def _build_dependency_map(
        self,
        workflow: WorkflowDefinition,
    ) -> dict[str, set[str]]:
        """Build a map from step to its dependencies."""
        dependencies: dict[str, set[str]] = {}
        
        for step in workflow.steps:
            dependencies[step.step_id] = set(step.depends_on)
        
        return dependencies

    def _build_reverse_dependency_map(
        self,
        workflow: WorkflowDefinition,
    ) -> dict[str, set[str]]:
        """Build a map from step to steps that depend on it."""
        reverse_deps: dict[str, set[str]] = {step.step_id: set() for step in workflow.steps}
        
        for step in workflow.steps:
            for dep in step.depends_on:
                if dep in reverse_deps:
                    reverse_deps[dep].add(step.step_id)
        
        return reverse_deps
