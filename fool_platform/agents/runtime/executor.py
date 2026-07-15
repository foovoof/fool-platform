"""
fool_platform/agents/runtime/executor.py

Agent Executor for FOOL Platform.

Provides deterministic agent execution with capability selection.
"""
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fool_platform.agents.base.agent import BaseAgent
from fool_platform.agents.base.agent_exceptions import (
    AgentCapabilityError,
    AgentError,
    AgentExecutionError,
    AgentValidationError,
)
from fool_platform.agents.base.context import AgentContext
from fool_platform.agents.base.events import AgentEventEmitter
from fool_platform.agents.base.models import (
    AgentExecutionRecord,
    AgentResult,
    AgentResultStatus,
    AgentStatus,
    AgentTask,
    AgentTaskStatus,
)
from fool_platform.agents.base.policies import AgentPolicyEvaluator


class AgentExecutor:
    """
    Executes agent tasks with deterministic behavior.
    
    Features:
    - Deterministic execution
    - Deterministic capability selection
    - Optional Event Bus support
    - Optional Policy Evaluator support
    - Execution record maintenance
    
    Rules:
    - No tools
    - No connectors
    - No AI
    """

    def __init__(
        self,
        event_emitter: AgentEventEmitter | None = None,
        policy_evaluator: AgentPolicyEvaluator | None = None,
    ) -> None:
        """
        Initialize the executor.
        
        Args:
            event_emitter: Optional event emitter
            policy_evaluator: Optional policy evaluator
        """
        self._agents: dict[str, BaseAgent] = {}
        self._capability_index: dict[str, str] = {}
        self._execution_records: dict[str, AgentExecutionRecord] = {}
        self._event_emitter = event_emitter or AgentEventEmitter()
        self._policy_evaluator = policy_evaluator

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the executor.
        
        Args:
            agent: The agent to register
            
        Raises:
            AgentError: If agent is already registered
        """
        if agent.agent_id in self._agents:
            raise AgentError(
                f"Agent {agent.agent_id} is already registered",
                agent_id=agent.agent_id,
            )

        self._agents[agent.agent_id] = agent

        for capability in agent.capabilities:
            self._capability_index[capability.capability_id] = agent.agent_id

    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent.
        
        Args:
            agent_id: The agent ID to unregister
            
        Returns:
            True if unregistered
        """
        if agent_id not in self._agents:
            return False

        agent = self._agents[agent_id]
        for capability in agent.capabilities:
            cap_id = capability.capability_id
            if self._capability_index.get(cap_id) == agent_id:
                del self._capability_index[cap_id]

        del self._agents[agent_id]
        return True

    def get_agent(self, agent_id: str) -> BaseAgent | None:
        """
        Get an agent by ID.
        
        Args:
            agent_id: The agent ID
            
        Returns:
            The agent or None if not found
        """
        return self._agents.get(agent_id)

    def list_agents(self) -> list[str]:
        """
        List all registered agent IDs.
        
        Returns:
            List of agent IDs
        """
        return list(self._agents.keys())

    def execute(
        self,
        task: AgentTask,
        agent_id: str,
        context: AgentContext | None = None,
    ) -> AgentResult:
        """
        Execute a task with a specific agent.
        
        Args:
            task: The task to execute
            agent_id: The agent to use
            context: Optional execution context
            
        Returns:
            AgentResult from execution
            
        Raises:
            AgentValidationError: If task validation fails
            AgentCapabilityError: If agent cannot handle task
            AgentExecutionError: If execution fails
        """
        validation_errors = self.validate_task(task)
        if validation_errors:
            raise AgentValidationError(
                "Task validation failed",
                validation_errors=validation_errors,
            )

        agent = self._agents.get(agent_id)
        if not agent:
            raise AgentCapabilityError(
                f"Agent {agent_id} not found",
                agent_id=agent_id,
            )

        if not agent.can_handle(task):
            raise AgentCapabilityError(
                f"Agent {agent_id} cannot handle task type {task.task_type}",
                agent_id=agent_id,
                capability_id=task.task_type,
            )

        if self._policy_evaluator:
            policy_result = self._policy_evaluator.evaluate_task(
                task, context or AgentContext.create(agent_id=agent_id)
            )
            if policy_result.is_denied:
                raise AgentExecutionError(
                    f"Policy {policy_result.policy_name} denied execution: {policy_result.reason}",
                    agent_id=agent_id,
                    task_id=task.task_id,
                )

        execution_record = AgentExecutionRecord(
            task_id=task.task_id,
            agent_id=agent_id,
            status=AgentTaskStatus.RUNNING,
        )
        self._execution_records[execution_record.execution_record_id] = execution_record

        ctx = context or AgentContext.create(
            agent_id=agent_id,
            task_id=task.task_id,
        )

        if agent.status != AgentStatus.RUNNING:
            try:
                agent.start()
            except Exception as e:
                execution_record = execution_record.mark_failed([str(e)])
                raise AgentExecutionError(
                    str(e),
                    agent_id=agent_id,
                    task_id=task.task_id,
                    cause=e,
                )

        try:
            result = agent.execute(task, ctx)

            execution_record = self._execution_records[
                execution_record.execution_record_id
            ].mark_completed(result.result_id)

            return result

        except Exception as e:
            execution_record = self._execution_records[
                execution_record.execution_record_id
            ].mark_failed([str(e)])

            raise AgentExecutionError(
                str(e),
                agent_id=agent_id,
                task_id=task.task_id,
                cause=e,
            )

    def execute_with_capability(
        self,
        task: AgentTask,
        capability_id: str,
        context: AgentContext | None = None,
    ) -> AgentResult:
        """
        Execute a task with the first agent that has the capability.
        
        Uses deterministic capability selection.
        
        Args:
            task: The task to execute
            capability_id: The required capability
            context: Optional execution context
            
        Returns:
            AgentResult from execution
            
        Raises:
            AgentCapabilityError: If no agent has the capability
        """
        agent_id = self._capability_index.get(capability_id)
        if not agent_id:
            raise AgentCapabilityError(
                f"No agent found with capability {capability_id}",
                capability_id=capability_id,
            )

        return self.execute(task, agent_id, context)

    def validate_agent(self, agent: BaseAgent) -> list[str]:
        """
        Validate an agent.
        
        Args:
            agent: The agent to validate
            
        Returns:
            List of validation errors
        """
        errors: list[str] = []

        if not agent.agent_id:
            errors.append("Agent must have an agent_id")

        if not agent.name:
            errors.append("Agent must have a name")

        if not agent.capabilities:
            errors.append("Agent must have at least one capability")

        if not agent.health_check() and agent.status != AgentStatus.CREATED:
            errors.append(f"Agent health check failed: status={agent.status.value}")

        return errors

    def validate_task(self, task: AgentTask) -> list[str]:
        """
        Validate a task.
        
        Args:
            task: The task to validate
            
        Returns:
            List of validation errors
        """
        errors: list[str] = []

        if not task.task_id:
            errors.append("Task must have a task_id")

        if not task.objective:
            errors.append("Task must have an objective")

        if not task.task_type:
            errors.append("Task must have a task_type")

        return errors

    def get_execution_record(
        self, execution_record_id: str
    ) -> AgentExecutionRecord | None:
        """
        Get an execution record.
        
        Args:
            execution_record_id: The record ID
            
        Returns:
            The record or None if not found
        """
        return self._execution_records.get(execution_record_id)

    def list_execution_records(
        self, task_id: str | None = None, agent_id: str | None = None
    ) -> list[AgentExecutionRecord]:
        """
        List execution records.
        
        Args:
            task_id: Optional task ID to filter by
            agent_id: Optional agent ID to filter by
            
        Returns:
            List of matching records
        """
        records = list(self._execution_records.values())

        if task_id:
            records = [r for r in records if r.task_id == task_id]

        if agent_id:
            records = [r for r in records if r.agent_id == agent_id]

        return records
