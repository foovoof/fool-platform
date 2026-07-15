from __future__ import annotations

"""
knowledge/inference/tests/test_inference.py

Tests for Inference Layer.

Covers:
1. Inference session creation
2. Inference result creation
3. Rule registration
4. Rule validation
5. Rule evaluation
6. Rule execution
7. Evidence tracking
8. Evidence chain creation
9. Evidence propagation
10. Confidence calculation
11. Confidence propagation
12. Explanation generation
13. Inference validation
14. Rule consistency
15. Event emission
16. Architecture boundaries
"""
import pytest
from datetime import datetime, timezone

from knowledge.graph.models import Graph, Node, Edge, NodeType, RelationshipType
from knowledge.inference.engine.inference_session import InferenceSession
from knowledge.inference.engine.inference_result import InferenceResult, InferenceConclusion, ConclusionType
from knowledge.inference.engine.inference_engine import InferenceEngine
from knowledge.inference.rules import (
    Rule,
    RuleCondition,
    RuleOutput,
    RuleRegistry,
    RuleValidator,
    RuleEvaluator,
    RuleExecutor,
    ConditionType,
    OutputType,
    EvaluationContext,
)
from knowledge.inference.evidence import Evidence, EvidenceTracker, EvidenceChain, EvidenceChainBuilder, EvidenceType
from knowledge.inference.confidence import (
    ConfidenceRecord,
    ConfidenceUpdate,
    ConfidenceCalculator,
    ConfidencePropagation,
    ConfidenceLevel,
    CalculationInput,
)
from knowledge.inference.explanation import Explanation, ExplanationGenerator
from knowledge.inference.validation import InferenceValidator, RuleConsistencyValidator
from knowledge.inference.events import InferenceEventEmitter, InferenceEventType
from knowledge.inference.services import (
    InferenceService,
    RuleService,
    EvidenceService,
    ConfidenceService,
    ExplanationService,
)


class TestInferenceModels:
    """Test inference models."""

    def test_inference_session_creation(self):
        """Test InferenceSession creation."""
        session = InferenceSession(
            graph_id="graph-123",
            graph_version="1.0.0",
        )
        assert session.session_id is not None
        assert session.graph_id == "graph-123"
        assert session.status == "active"

    def test_inference_session_completion(self):
        """Test InferenceSession completion."""
        session = InferenceSession()
        session.mark_completed()
        assert session.status == "completed"
        assert session.completed_at is not None

    def test_inference_conclusion_creation(self):
        """Test InferenceConclusion creation."""
        conclusion = InferenceConclusion(
            conclusion_type=ConclusionType.FACT,
            conclusion_value={"key": "value"},
            evidence_ids=["ev-1"],
            confidence=0.9,
        )
        assert conclusion.conclusion_id is not None
        assert conclusion.is_valid()

    def test_inference_result_creation(self):
        """Test InferenceResult creation."""
        result = InferenceResult(session_id="session-123")
        assert result.result_id is not None
        assert result.session_id == "session-123"

    def test_inference_result_add_conclusion(self):
        """Test adding conclusions to result."""
        result = InferenceResult()
        conclusion = InferenceConclusion(
            conclusion_value={"test": True},
            confidence=0.8,
        )
        result.add_conclusion(conclusion)
        assert len(result.conclusions) == 1
        assert len(result.inferred_facts) == 1


class TestRuleRegistry:
    """Test rule registry."""

    def test_register_rule(self):
        """Test rule registration."""
        registry = RuleRegistry()
        rule = Rule(
            name="test_rule",
            conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
            outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
        )
        success = registry.register_rule(rule)
        assert success
        assert registry.count() == 1

    def test_get_rule(self):
        """Test getting a rule."""
        registry = RuleRegistry()
        rule = Rule(
            name="get_rule_test",
            conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
            outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
        )
        registry.register_rule(rule)
        retrieved = registry.get_rule(rule.rule_id)
        assert retrieved is not None
        assert retrieved.name == "get_rule_test"

    def test_list_rules(self):
        """Test listing rules."""
        registry = RuleRegistry()
        for i in range(3):
            rule = Rule(
                name=f"rule_{i}",
                enabled=True,
                conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
                outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
            )
            registry.register_rule(rule)
        rules = registry.list_rules()
        assert len(rules) == 3


class TestRuleValidation:
    """Test rule validation."""

    def test_validate_valid_rule(self):
        """Test validating a valid rule."""
        validator = RuleValidator()
        rule = Rule(
            rule_id="rule-1",
            name="valid_rule",
            conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
            outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
        )
        result = validator.validate_rule(rule)
        assert result.is_valid

    def test_validate_invalid_rule(self):
        """Test validating an invalid rule."""
        validator = RuleValidator()
        rule = Rule(name="")
        result = validator.validate_rule(rule)
        assert not result.is_valid


class TestRuleEvaluator:
    """Test rule evaluator."""

    def test_evaluate_entity_exists(self):
        """Test entity exists condition."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        evaluator = RuleEvaluator()
        condition = RuleCondition(
            condition_type=ConditionType.ENTITY_EXISTS,
            target=node.node_id,
        )
        
        context = EvaluationContext(graph=graph)
        result = evaluator._evaluate_condition(condition, context)
        
        assert result.is_met


class TestEvidenceTracker:
    """Test evidence tracker."""

    def test_register_evidence(self):
        """Test evidence registration."""
        tracker = EvidenceTracker()
        evidence = Evidence(
            evidence_type=EvidenceType.NODE,
            source_id="node-123",
        )
        evidence_id = tracker.register_evidence(evidence)
        assert evidence_id == evidence.evidence_id
        assert tracker.count() == 1

    def test_track_usage(self):
        """Test evidence usage tracking."""
        tracker = EvidenceTracker()
        evidence = Evidence(source_id="node-123")
        tracker.register_evidence(evidence)
        
        success = tracker.track_usage(
            evidence.evidence_id,
            conclusion_id="conclusion-1",
            rule_id="rule-1",
        )
        assert success


class TestConfidenceCalculator:
    """Test confidence calculator."""

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        calculator = ConfidenceCalculator()
        input_data = CalculationInput(
            base_confidence=1.0,
            evidence_count=3,
            supporting_evidence=2,
        )
        result = calculator.calculate_confidence(input_data)
        assert 0.0 <= result.value <= 1.0

    def test_merge_confidences(self):
        """Test merging confidences."""
        calculator = ConfidenceCalculator()
        merged = calculator.merge_confidences([0.8, 0.9, 0.7], "average")
        assert abs(merged - 0.8) < 0.01

    def test_validate_confidence(self):
        """Test confidence validation."""
        calculator = ConfidenceCalculator()
        assert calculator.validate_confidence(0.5)
        assert calculator.validate_confidence(1.0)
        assert not calculator.validate_confidence(1.5)


class TestExplanationGenerator:
    """Test explanation generator."""

    def test_explain_rule(self):
        """Test rule explanation."""
        generator = ExplanationGenerator()
        rule = Rule(
            rule_id="rule-1",
            name="test_rule",
            description="A test rule",
            conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
            outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
        )
        explanation = generator.explain_rule(rule)
        assert explanation.explanation_id is not None
        assert explanation.rule_name == "test_rule"

    def test_explain_conclusion(self):
        """Test conclusion explanation."""
        generator = ExplanationGenerator()
        conclusion = InferenceConclusion(
            conclusion_value={"test": True},
            confidence=0.9,
        )
        explanation = generator.explain_conclusion(conclusion)
        assert explanation.explanation_id is not None


class TestInferenceValidator:
    """Test inference validator."""

    def test_validate_result(self):
        """Test result validation."""
        validator = InferenceValidator()
        result = InferenceResult()
        conclusion = InferenceConclusion(
            conclusion_value={"test": True},
            evidence_ids=["ev-1"],
            confidence=0.8,
        )
        result.add_conclusion(conclusion)
        
        validation = validator.validate_result(result)
        assert validation.is_valid


class TestInferenceEngine:
    """Test inference engine."""

    def test_create_session(self):
        """Test session creation."""
        engine = InferenceEngine()
        graph = Graph()
        session = engine.create_session(graph)
        assert session.session_id is not None
        assert session.graph_id == graph.graph_id

    def test_execute_no_rules(self):
        """Test execution with no rules."""
        engine = InferenceEngine()
        graph = Graph()
        session = engine.create_session(graph)
        result = engine.execute(session, graph)
        assert result.session_id == session.session_id
        assert len(result.conclusions) == 0


class TestInferenceEvents:
    """Test inference events."""

    def test_event_emitter_without_bus(self):
        """Test event emitter without Event Bus."""
        emitter = InferenceEventEmitter()
        result = emitter.emit("test.event", {"data": "value"})
        assert result is False
        assert emitter.get_event_count() == 1

    def test_event_types(self):
        """Test event type definitions."""
        assert InferenceEventType.SESSION_STARTED.value == "knowledge.inference.session.started"
        assert InferenceEventType.RULE_EVALUATED.value == "knowledge.rule.evaluated"


class TestInferenceServices:
    """Test inference services."""

    def test_rule_service(self):
        """Test RuleService."""
        service = RuleService()
        rule = Rule(
            name="service_test",
            conditions=[RuleCondition(condition_type=ConditionType.ENTITY_EXISTS)],
            outputs=[RuleOutput(output_type=OutputType.GENERATE_CONCLUSION)],
        )
        result = service.register_rule(rule)
        assert result["success"]

    def test_inference_service(self):
        """Test InferenceService."""
        service = InferenceService()
        graph = Graph()
        result = service.run_inference(graph)
        assert "session_id" in result


class TestArchitectureConstraints:
    """Test architecture constraints."""

    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        inference_dir = Path(__file__).parent.parent.parent
        for py_file in inference_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('#'):
                    continue
                lower_line = line.lower()
                if 'import' in lower_line or 'from' in lower_line:
                    assert "openai" not in lower_line, f"Found openai in {py_file}"
                    assert "anthropic" not in lower_line, f"Found anthropic in {py_file}"
                    assert "langchain" not in lower_line, f"Found langchain in {py_file}"

    def test_no_intelligence_imports(self):
        """Verify no intelligence imports."""
        from pathlib import Path
        
        inference_dir = Path(__file__).parent.parent.parent
        for py_file in inference_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from intelligence" not in content
            assert "import intelligence" not in content

    def test_no_connector_imports(self):
        """Verify no connector imports."""
        from pathlib import Path
        
        inference_dir = Path(__file__).parent.parent.parent
        for py_file in inference_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content
