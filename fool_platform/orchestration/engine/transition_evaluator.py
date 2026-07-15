"""
fool_platform/orchestration/engine/transition_evaluator.py

Transition evaluation for workflow steps.
"""
from dataclasses import dataclass
from typing import Any

from fool_platform.orchestration.models import WorkflowExecution
from fool_platform.orchestration.registry.workflow_registry import (
    TransitionDefinition,
    WorkflowDefinition,
)


ALLOWED_CONDITION_TYPES = frozenset({
    "step_completed",
    "step_failed",
    "step_skipped",
    "all_dependencies_completed",
    "any_dependency_failed",
    "always",
})


@dataclass
class TransitionDecision:
    """Result of transition evaluation."""
    transition: TransitionDefinition
    should_take: bool
    rationale: str


@dataclass
class TransitionEvaluation:
    """Result of evaluating all transitions."""
    available_transitions: list[TransitionDecision]
    selected_transition: TransitionDefinition | None
    rationale: str


class TransitionEvaluator:
    """
    Evaluates workflow transitions based on execution state.
    
    Only supports safe, declarative condition types.
    No eval() or exec().
    """

    def evaluate_transition(
        self,
        transition: TransitionDefinition,
        execution: WorkflowExecution,
    ) -> TransitionDecision:
        """
        Evaluate whether a transition should be taken.
        
        Args:
            transition: The transition definition
            execution: The current workflow execution
            
        Returns:
            TransitionDecision with evaluation result
        """
        condition_type = transition.condition_type
        
        if condition_type not in ALLOWED_CONDITION_TYPES:
            return TransitionDecision(
                transition=transition,
                should_take=False,
                rationale=f"Unknown condition type: {condition_type}",
            )
        
        result = self.evaluate_condition(
            condition_type,
            transition.condition_params,
            execution,
        )
        
        return TransitionDecision(
            transition=transition,
            should_take=result,
            rationale=self._explain_condition(condition_type, transition.condition_params, result),
        )

    def evaluate_condition(
        self,
        condition_type: str,
        params: dict[str, Any],
        execution: WorkflowExecution,
    ) -> bool:
        """
        Evaluate a declarative condition.
        
        Args:
            condition_type: Type of condition
            params: Condition parameters
            execution: Current workflow execution
            
        Returns:
            True if condition is met
        """
        if condition_type == "always":
            return True
        
        if condition_type == "step_completed":
            step_id = params.get("step_id") or params.get("from_step")
            if step_id:
                return step_id in execution.completed_steps
            return False
        
        if condition_type == "step_failed":
            step_id = params.get("step_id")
            if step_id:
                return step_id in execution.failed_steps
            return False
        
        if condition_type == "step_skipped":
            return False
        
        if condition_type == "all_dependencies_completed":
            to_step = params.get("to_step")
            if not to_step:
                return False
            return True
        
        if condition_type == "any_dependency_failed":
            return len(execution.failed_steps) > 0
        
        return False

    def find_available_transitions(
        self,
        workflow: WorkflowDefinition,
        execution: WorkflowExecution,
    ) -> TransitionEvaluation:
        """
        Find transitions that should be taken based on current state.
        
        Args:
            workflow: The workflow definition
            execution: The current workflow execution
            
        Returns:
            TransitionEvaluation with available transitions
        """
        decisions: list[TransitionDecision] = []
        
        for transition in workflow.transitions:
            decision = self.evaluate_transition(transition, execution)
            decisions.append(decision)
        
        available = [d for d in decisions if d.should_take]
        
        if not available:
            return TransitionEvaluation(
                available_transitions=decisions,
                selected_transition=None,
                rationale="No transitions available",
            )
        
        selected = available[0]
        return TransitionEvaluation(
            available_transitions=decisions,
            selected_transition=selected.transition,
            rationale=f"Taking transition: {selected.rationale}",
        )

    def _explain_condition(
        self,
        condition_type: str,
        params: dict[str, Any],
        result: bool,
    ) -> str:
        """Generate explanation for a condition evaluation."""
        status = "met" if result else "not met"
        
        if condition_type == "always":
            return f"Condition 'always' is always {status}"
        if condition_type == "step_completed":
            step_id = params.get("step_id") or params.get("from_step")
            return f"Step {step_id} completed check is {status}"
        if condition_type == "step_failed":
            step_id = params.get("step_id")
            return f"Step {step_id} failed check is {status}"
        if condition_type == "all_dependencies_completed":
            return f"All dependencies completed check is {status}"
        if condition_type == "any_dependency_failed":
            return f"Any dependency failed check is {status}"
        
        return f"Condition {condition_type} is {status}"
