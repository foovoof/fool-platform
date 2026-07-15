"""
domain/tests/test_domain.py

Tests for Python domain models.
"""
import pytest

from domain import (
    Case,
    CasePriority,
    ClassificationLevel,
    ClassificationLevelValue,
    ConfidenceLevel,
    ConfidenceMethod,
    ConfidenceMethods,
    ConfidenceScore,
    DomainInvariantError,
    Entity,
    EntityType,
    Identity,
    Identifier,
    IdentifierType,
    Provenance,
    Reference,
    Status,
    create_provenance,
    freeze_refs,
    freeze_tags,
    make_reference,
    new_id,
    utc_now,
)


class TestCommonTypes:
    """Tests for common types."""
    
    def test_new_id(self):
        """Test ID generation."""
        id1 = new_id()
        id2 = new_id()
        assert id1 != id2
        assert len(id1) == 36  # UUID format
    
    def test_utc_now(self):
        """Test timestamp generation."""
        ts = utc_now()
        assert "T" in ts  # ISO format
        # UTC timezone indicator - either Z or +00:00
        assert ts.endswith("Z") or ts.endswith("+00:00")
    
    def test_create_provenance(self):
        """Test provenance creation."""
        prov = create_provenance("test-origin")
        assert prov.origin == "test-origin"
        assert prov.recorded_at is not None
        assert len(prov.lineage) == 0
    
    def test_create_provenance_requires_origin(self):
        """Test provenance requires non-empty origin."""
        with pytest.raises(ValueError):
            create_provenance("")
    
    def test_make_reference(self):
        """Test reference creation."""
        ref = make_reference("id-123", "entity")
        assert ref.ref_id == "id-123"
        assert ref.ref_type == "entity"
        assert ref.ref_version is None
    
    def test_freeze_tags(self):
        """Test tag freezing."""
        tags = freeze_tags(["a", "b", "a"])
        assert tags == frozenset({"a", "b"})
    
    def test_freeze_refs(self):
        """Test reference freezing."""
        refs = [make_reference("1", "t"), make_reference("2", "t")]
        frozen = freeze_refs(refs)
        assert isinstance(frozen, frozenset)
        assert len(frozen) == 2


class TestClassificationLevel:
    """Tests for ClassificationLevel."""
    
    def test_create_classification_level(self):
        """Test classification level creation."""
        cl = ClassificationLevel(ClassificationLevelValue.INTERNAL)
        assert cl.value == ClassificationLevelValue.INTERNAL
    
    def test_preset_classification_levels(self):
        """Test preset classification level methods."""
        assert ClassificationLevel.public().value == ClassificationLevelValue.PUBLIC
        assert ClassificationLevel.internal().value == ClassificationLevelValue.INTERNAL
        assert ClassificationLevel.restricted().value == ClassificationLevelValue.RESTRICTED
        assert ClassificationLevel.confidential().value == ClassificationLevelValue.CONFIDENTIAL
    
    def test_requires_access_control(self):
        """Test access control requirement check."""
        assert not ClassificationLevel.public().requires_access_control()
        assert ClassificationLevel.internal().requires_access_control()
        assert ClassificationLevel.restricted().requires_access_control()
        assert ClassificationLevel.confidential().requires_access_control()


class TestConfidenceScore:
    """Tests for ConfidenceScore."""
    
    def test_create_confidence_score(self):
        """Test confidence score creation."""
        score = ConfidenceScore.create(
            score=0.75,
            method=ConfidenceMethods.MANUAL_REVIEW,
        )
        assert score.score == 0.75
        assert score.level == ConfidenceLevel.HIGH
        assert score.method == ConfidenceMethods.MANUAL_REVIEW
    
    def test_level_derivation(self):
        """Test confidence level derivation from score."""
        assert ConfidenceScore.create(0.1, ConfidenceMethods.MANUAL_REVIEW).level == ConfidenceLevel.VERY_LOW
        assert ConfidenceScore.create(0.3, ConfidenceMethods.MANUAL_REVIEW).level == ConfidenceLevel.LOW
        assert ConfidenceScore.create(0.5, ConfidenceMethods.MANUAL_REVIEW).level == ConfidenceLevel.MODERATE
        assert ConfidenceScore.create(0.7, ConfidenceMethods.MANUAL_REVIEW).level == ConfidenceLevel.HIGH
        assert ConfidenceScore.create(0.9, ConfidenceMethods.MANUAL_REVIEW).level == ConfidenceLevel.VERY_HIGH
    
    def test_score_validation(self):
        """Test score validation."""
        with pytest.raises(DomainInvariantError):
            ConfidenceScore.create(-0.1, ConfidenceMethods.MANUAL_REVIEW)
        with pytest.raises(DomainInvariantError):
            ConfidenceScore.create(1.1, ConfidenceMethods.MANUAL_REVIEW)
    
    def test_is_high_confidence(self):
        """Test high confidence check."""
        assert ConfidenceScore.create(0.75, ConfidenceMethods.MANUAL_REVIEW).is_high_confidence()
        assert not ConfidenceScore.create(0.3, ConfidenceMethods.MANUAL_REVIEW).is_high_confidence()


class TestIdentity:
    """Tests for Identity domain model."""
    
    def test_create_identity(self):
        """Test identity creation."""
        prov = create_provenance("test-origin")
        identifier = Identifier(
            identifier_type=IdentifierType.EMAIL,
            value="test@example.com",
            confidence=ConfidenceScore.create(0.9, ConfidenceMethods.MANUAL_REVIEW),
        )
        
        identity = Identity.create(
            identifiers=[identifier],
            provenance=prov,
        )
        
        assert identity.id is not None
        assert len(identity.identifiers) == 1
        assert identity.status == Status.ACTIVE
        assert identity.classification == ClassificationLevel(ClassificationLevelValue.INTERNAL)
    
    def test_identity_requires_at_least_one_identifier(self):
        """Test identity creation requires at least one identifier."""
        prov = create_provenance("test-origin")
        with pytest.raises(DomainInvariantError):
            Identity.create(
                identifiers=[],
                provenance=prov,
            )
    
    def test_identity_with_identifier(self):
        """Test adding identifier to identity."""
        prov = create_provenance("test-origin")
        id1 = Identifier(
            identifier_type=IdentifierType.EMAIL,
            value="test@example.com",
            confidence=ConfidenceScore.create(0.9, ConfidenceMethods.MANUAL_REVIEW),
        )
        id2 = Identifier(
            identifier_type=IdentifierType.PHONE,
            value="1234567890",
            confidence=ConfidenceScore.create(0.8, ConfidenceMethods.MANUAL_REVIEW),
        )
        
        identity = Identity.create(identifiers=[id1], provenance=prov)
        new_identity = identity.with_identifier(id2)
        
        assert len(identity.identifiers) == 1
        assert len(new_identity.identifiers) == 2
    
    def test_identity_has_identifier_value(self):
        """Test checking identifier value."""
        prov = create_provenance("test-origin")
        identifier = Identifier(
            identifier_type=IdentifierType.EMAIL,
            value="test@example.com",
            confidence=ConfidenceScore.create(0.9, ConfidenceMethods.MANUAL_REVIEW),
        )
        
        identity = Identity.create(identifiers=[identifier], provenance=prov)
        assert identity.has_identifier_value("test@example.com")
        assert not identity.has_identifier_value("other@example.com")


class TestEntity:
    """Tests for Entity domain model."""
    
    def test_create_entity(self):
        """Test entity creation."""
        prov = create_provenance("test-origin")
        entity = Entity.create(
            entity_type=EntityType.PERSON,
            name="John Doe",
            provenance=prov,
        )
        
        assert entity.id is not None
        assert entity.name == "John Doe"
        assert entity.entity_type == EntityType.PERSON
    
    def test_entity_requires_name(self):
        """Test entity creation requires name."""
        prov = create_provenance("test-origin")
        with pytest.raises(DomainInvariantError):
            Entity.create(
                entity_type=EntityType.PERSON,
                name="",
                provenance=prov,
            )


class TestCase:
    """Tests for Case domain model."""
    
    def test_create_case(self):
        """Test case creation."""
        prov = create_provenance("test-origin")
        case = Case.create(
            title="Test Case",
            description="A test case",
            owner="investigator@example.com",
            provenance=prov,
        )
        
        assert case.id is not None
        assert case.title == "Test Case"
        assert case.owner == "investigator@example.com"
        assert case.status == Status.DRAFT
    
    def test_case_requires_owner(self):
        """Test case creation requires owner."""
        prov = create_provenance("test-origin")
        with pytest.raises(ValueError):
            Case.create(
                title="Test Case",
                description="A test case",
                owner="",
                provenance=prov,
            )
    
    def test_case_with_investigation_ref(self):
        """Test adding investigation reference."""
        prov = create_provenance("test-origin")
        case = Case.create(
            title="Test Case",
            description="A test case",
            owner="owner@example.com",
            provenance=prov,
        )
        
        ref = make_reference("inv-123", "investigation")
        new_case = case.with_investigation_ref(ref)
        
        assert len(case.investigation_refs) == 0
        assert len(new_case.investigation_refs) == 1
