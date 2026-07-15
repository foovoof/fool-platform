"""
fool_platform/orchestration/registry/workflow_registry.py

Workflow registry for managing workflow definitions.
"""
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any

from fool_platform.orchestration.orchestration_exceptions import (
    WorkflowNotFoundError,
    WorkflowValidationError,
)


@dataclass
class StepDefinition:
    """Definition of a workflow step."""
    step_id: str
    name: str
    agent_type: str | None = None
    capability: str | None = None
    input_schema_ref: str | None = None
    output_schema_ref: str | None = None
    depends_on: list[str] = field(default_factory=list)
    retry_policy: dict[str, Any] | None = None
    timeout_policy: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransitionDefinition:
    """Definition of a workflow transition."""
    from_step: str
    to_step: str
    condition_type: str
    condition_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDefinition:
    """Definition of a workflow."""
    workflow_id: str
    name: str
    version: str
    description: str | None = None
    required_agents: list[str] = field(default_factory=list)
    required_capabilities: list[str] = field(default_factory=list)
    steps: list[StepDefinition] = field(default_factory=list)
    transitions: list[TransitionDefinition] = field(default_factory=list)
    failure_policy: dict[str, Any] | None = None
    termination_conditions: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkflowRegistry:
    """
    Registry for workflow definitions.
    
    Loads workflows from YAML files.
    Validates workflow structure and references.
    """

    def __init__(self, workflows_path: Path | None = None) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._lock = Lock()
        self._loaded = False
        self._workflows_path = workflows_path
        if workflows_path and workflows_path.exists():
            self.load_workflows(workflows_path)

    def load_workflows(self, workflows_path: Path | None = None) -> None:
        """
        Load workflow definitions from YAML files.
        
        Args:
            workflows_path: Path to workflows directory (uses default if None)
        """
        path = workflows_path or self._workflows_path
        if not path or not path.exists():
            return

        with self._lock:
            try:
                import yaml
                
                for yaml_file in path.glob("*.yaml"):
                    try:
                        with open(yaml_file, "r") as f:
                            data = yaml.safe_load(f)
                        
                        if data:
                            workflow = self._parse_workflow(data)
                            self._workflows[workflow.workflow_id] = workflow
                    except Exception:
                        continue
                
                self._loaded = True
            except ImportError:
                self._load_simple_yaml(path)
            except Exception as e:
                raise WorkflowValidationError(
                    workflow_id="unknown",
                    errors=[f"Failed to load workflows: {e}"],
                )

    def _load_simple_yaml(self, path: Path) -> None:
        """Simple YAML fallback without PyYAML."""
        pass

    def _parse_workflow(self, data: dict) -> WorkflowDefinition:
        """Parse workflow data into WorkflowDefinition."""
        steps = []
        for step_data in data.get("steps", []):
            steps.append(StepDefinition(
                step_id=step_data["step_id"],
                name=step_data.get("name", step_data["step_id"]),
                agent_type=step_data.get("agent_type"),
                capability=step_data.get("capability"),
                input_schema_ref=step_data.get("input_schema_ref"),
                output_schema_ref=step_data.get("output_schema_ref"),
                depends_on=step_data.get("depends_on", []),
                retry_policy=step_data.get("retry_policy"),
                timeout_policy=step_data.get("timeout_policy"),
            ))

        transitions = []
        for trans_data in data.get("transitions", []):
            transitions.append(TransitionDefinition(
                from_step=trans_data.get("from_step", ""),
                to_step=trans_data.get("to_step", ""),
                condition_type=trans_data.get("condition_type", "always"),
                condition_params=trans_data.get("condition_params", {}),
            ))

        return WorkflowDefinition(
            workflow_id=data["workflow_id"],
            name=data.get("name", data["workflow_id"]),
            version=data.get("version", "1.0.0"),
            description=data.get("description"),
            required_agents=data.get("required_agents", []),
            required_capabilities=data.get("required_capabilities", []),
            steps=steps,
            transitions=transitions,
            failure_policy=data.get("failure_policy"),
            termination_conditions=data.get("termination_conditions", []),
        )

    def list_workflows(self) -> list[str]:
        """List all registered workflow IDs."""
        with self._lock:
            return list(self._workflows.keys())

    def get_workflow(self, workflow_id: str) -> WorkflowDefinition | None:
        """Get workflow definition by ID."""
        with self._lock:
            return self._workflows.get(workflow_id)

    def has_workflow(self, workflow_id: str) -> bool:
        """Check if workflow is registered."""
        with self._lock:
            return workflow_id in self._workflows

    def validate_workflow(
        self,
        workflow: WorkflowDefinition,
        agent_registry: "AgentRegistry | None" = None,
        capability_registry: "CapabilityRegistry | None" = None,
    ) -> list[str]:
        """
        Validate a workflow definition.
        
        Args:
            workflow: The workflow to validate
            agent_registry: Optional agent registry for reference validation
            capability_registry: Optional capability registry for reference validation
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors: list[str] = []

        if not workflow.workflow_id:
            errors.append("workflow_id is required")

        if not workflow.steps:
            errors.append("At least one step is required")

        step_ids = {step.step_id for step in workflow.steps}
        for step in workflow.steps:
            for dep in step.depends_on:
                if dep not in step_ids:
                    errors.append(f"Step {step.step_id} depends on unknown step {dep}")

        if agent_registry:
            errors.extend(self.validate_required_agents(workflow, agent_registry))
        
        if capability_registry:
            errors.extend(self.validate_required_capabilities(workflow, capability_registry))

        errors.extend(self.validate_steps(workflow))
        errors.extend(self.validate_transitions(workflow))

        return errors

    def validate_required_agents(
        self,
        workflow: WorkflowDefinition,
        agent_registry: "AgentRegistry",
    ) -> list[str]:
        """Validate that required agents exist."""
        errors = []
        for agent_id in workflow.required_agents:
            if not agent_registry.has_agent(agent_id):
                errors.append(f"Required agent {agent_id} not found in registry")
        return errors

    def validate_required_capabilities(
        self,
        workflow: WorkflowDefinition,
        capability_registry: "CapabilityRegistry",
    ) -> list[str]:
        """Validate that required capabilities exist."""
        errors = []
        for cap_id in workflow.required_capabilities:
            if not capability_registry.has_capability(cap_id):
                errors.append(f"Required capability {cap_id} not found in registry")
        return errors

    def validate_steps(self, workflow: WorkflowDefinition) -> list[str]:
        """Validate workflow steps."""
        errors = []
        step_ids = {step.step_id for step in workflow.steps}

        for step in workflow.steps:
            if not step.step_id:
                errors.append("Step step_id is required")
            if not step.name:
                errors.append(f"Step {step.step_id} must have a name")

        return errors

    def validate_transitions(self, workflow: WorkflowDefinition) -> list[str]:
        """Validate workflow transitions."""
        errors = []
        step_ids = {step.step_id for step in workflow.steps}
        step_ids.add("")  # Allow terminal transitions

        for trans in workflow.transitions:
            if trans.from_step and trans.from_step not in step_ids:
                errors.append(f"Transition from unknown step {trans.from_step}")
            if trans.to_step and trans.to_step not in step_ids:
                errors.append(f"Transition to unknown step {trans.to_step}")

        return errors

    def is_loaded(self) -> bool:
        """Check if workflows have been loaded."""
        with self._lock:
            return self._loaded

    def clear(self) -> None:
        """Clear all registered workflows."""
        with self._lock:
            self._workflows.clear()
            self._loaded = False
