"""
workbench/runtime.py

Workbench Runtime.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from workbench.models import (
    IntelligenceProduct,
    IntelligenceCollection,
    ReviewCycle,
    ApprovalRecord,
    Publication,
    SourceAssessment,
    ConfidenceReview,
    GovernanceDecision,
    PublicationPolicy,
    AssertionReference,
    EvidencePackageReference,
    KnowledgeReference,
    Reviewer,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._products: dict[str, IntelligenceProduct] = {}
        self._collections: dict[str, IntelligenceCollection] = {}
        self._review_cycles: dict[str, ReviewCycle] = {}
        self._approval_records: dict[str, ApprovalRecord] = {}
        self._publications: dict[str, Publication] = {}
        self._source_assessments: dict[str, SourceAssessment] = {}
        self._confidence_reviews: dict[str, ConfidenceReview] = {}
        self._governance_decisions: dict[str, GovernanceDecision] = {}
        self._policies: dict[str, PublicationPolicy] = {}


_storage = InMemoryStorage()


class ProductManager:
    """Manages intelligence products - REFERENCES only."""
    
    def create(
        self,
        product_type: str,
        title: str,
        owner: str,
        description: str = "",
        author: str = "",
    ) -> IntelligenceProduct:
        """Create product governance wrapper."""
        product = IntelligenceProduct(
            id=str(uuid4()),
            product_type=product_type,
            title=title,
            description=description,
            owner=owner,
            status="draft",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._products[product.id] = product
        return product
    
    def get(self, product_id: str) -> IntelligenceProduct | None:
        """Get product by ID."""
        return _storage._products.get(product_id)
    
    def update(self, product: IntelligenceProduct) -> IntelligenceProduct:
        """Update product."""
        updated = IntelligenceProduct(
            id=product.id,
            product_type=product.product_type,
            title=product.title,
            description=product.description,
            status=product.status,
            owner=product.owner,
            assertion_refs=product.assertion_refs,
            evidence_refs=product.evidence_refs,
            knowledge_refs=product.knowledge_refs,
            collection_ids=product.collection_ids,
            review_cycle_id=product.review_cycle_id,
            publication_id=product.publication_id,
            superseded_by_id=product.superseded_by_id,
            parent_product_id=product.parent_product_id,
            tags=product.tags,
            classification=product.classification,
            tlp=product.tlp,
            created_at=product.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=product.version + 1,
            metadata=product.metadata,
            author=product.author,
            reason=product.reason,
            revision_history=product.revision_history,
        )
        _storage._products[updated.id] = updated
        return updated
    
    def list_all(self) -> list[IntelligenceProduct]:
        """List all products."""
        return list(_storage._products.values())
    
    def find_by_status(self, status: str) -> list[IntelligenceProduct]:
        """Find by status."""
        return [p for p in _storage._products.values() if p.status == status]
    
    def attach_assertion(
        self,
        product_id: str,
        assertion_ref: str,
        source_system: str,
    ) -> IntelligenceProduct | None:
        """Attach assertion reference - NEVER duplicates."""
        product = self.get(product_id)
        if not product:
            return None
        
        ref = AssertionReference(
            id=str(uuid4()),
            product_id=product_id,
            assertion_ref=assertion_ref,
            source_system=source_system,
            ref_id=assertion_ref,
            ref_type="assertion",
            ref_source=source_system,
        )
        
        return self.update(IntelligenceProduct(
            id=product.id,
            product_type=product.product_type,
            title=product.title,
            description=product.description,
            status=product.status,
            owner=product.owner,
            assertion_refs=product.assertion_refs + (ref,),
            evidence_refs=product.evidence_refs,
            knowledge_refs=product.knowledge_refs,
            collection_ids=product.collection_ids,
            review_cycle_id=product.review_cycle_id,
            publication_id=product.publication_id,
            superseded_by_id=product.superseded_by_id,
            parent_product_id=product.parent_product_id,
            tags=product.tags,
            classification=product.classification,
            tlp=product.tlp,
            created_at=product.created_at,
            modified_at=product.modified_at,
            version=product.version,
            metadata=product.metadata,
            author=product.author,
            reason=product.reason,
            revision_history=product.revision_history,
        ))
    
    def attach_evidence(
        self,
        product_id: str,
        evidence_ref: str,
        source_system: str,
    ) -> IntelligenceProduct | None:
        """Attach evidence reference - NEVER duplicates."""
        product = self.get(product_id)
        if not product:
            return None
        
        ref = EvidencePackageReference(
            id=str(uuid4()),
            product_id=product_id,
            evidence_ref=evidence_ref,
            source_system=source_system,
            ref_id=evidence_ref,
            ref_type="evidence",
            ref_source=source_system,
        )
        
        return self.update(IntelligenceProduct(
            id=product.id,
            product_type=product.product_type,
            title=product.title,
            description=product.description,
            status=product.status,
            owner=product.owner,
            assertion_refs=product.assertion_refs,
            evidence_refs=product.evidence_refs + (ref,),
            knowledge_refs=product.knowledge_refs,
            collection_ids=product.collection_ids,
            review_cycle_id=product.review_cycle_id,
            publication_id=product.publication_id,
            superseded_by_id=product.superseded_by_id,
            parent_product_id=product.parent_product_id,
            tags=product.tags,
            classification=product.classification,
            tlp=product.tlp,
            created_at=product.created_at,
            modified_at=product.modified_at,
            version=product.version,
            metadata=product.metadata,
            author=product.author,
            reason=product.reason,
            revision_history=product.revision_history,
        ))
    
    def transition_status(
        self,
        product_id: str,
        new_status: str,
        reason: str = "",
        actor: str = "",
    ) -> IntelligenceProduct | None:
        """Transition product status."""
        product = self.get(product_id)
        if not product:
            return None
        
        return self.update(IntelligenceProduct(
            id=product.id,
            product_type=product.product_type,
            title=product.title,
            description=product.description,
            status=new_status,
            owner=product.owner,
            assertion_refs=product.assertion_refs,
            evidence_refs=product.evidence_refs,
            knowledge_refs=product.knowledge_refs,
            collection_ids=product.collection_ids,
            review_cycle_id=product.review_cycle_id,
            publication_id=product.publication_id,
            superseded_by_id=product.superseded_by_id,
            parent_product_id=product.parent_product_id,
            tags=product.tags,
            classification=product.classification,
            tlp=product.tlp,
            created_at=product.created_at,
            modified_at=product.modified_at,
            version=product.version,
            metadata=product.metadata,
            author=actor,
            reason=reason,
            revision_history=product.revision_history,
        ))


class CollectionManager:
    """Manages intelligence collections."""
    
    def create(
        self,
        name: str,
        owner: str,
        description: str = "",
        author: str = "",
    ) -> IntelligenceCollection:
        """Create collection."""
        collection = IntelligenceCollection(
            id=str(uuid4()),
            name=name,
            description=description,
            owner=owner,
            status="active",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._collections[collection.id] = collection
        return collection
    
    def get(self, collection_id: str) -> IntelligenceCollection | None:
        """Get collection by ID."""
        return _storage._collections.get(collection_id)
    
    def add_product(
        self,
        collection_id: str,
        product_id: str,
    ) -> IntelligenceCollection | None:
        """Add product reference to collection."""
        collection = self.get(collection_id)
        if not collection:
            return None
        
        if product_id in collection.product_refs:
            return collection
        
        updated = IntelligenceCollection(
            id=collection.id,
            name=collection.name,
            description=collection.description,
            owner=collection.owner,
            status=collection.status,
            product_refs=collection.product_refs + (product_id,),
            collection_policy=collection.collection_policy,
            created_at=collection.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=collection.version + 1,
            metadata=collection.metadata,
            author=collection.author,
            reason=collection.reason,
            revision_history=collection.revision_history,
        )
        _storage._collections[updated.id] = updated
        return updated


class ReviewManager:
    """Manages review cycles."""
    
    def create_review(
        self,
        product_id: str,
        reviewers: list[Reviewer],
        author: str = "",
    ) -> ReviewCycle:
        """Create review cycle."""
        review = ReviewCycle(
            id=str(uuid4()),
            product_id=product_id,
            status="pending",
            reviewers=tuple(reviewers),
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._review_cycles[review.id] = review
        return review
    
    def get(self, review_id: str) -> ReviewCycle | None:
        """Get review by ID."""
        return _storage._review_cycles.get(review_id)
    
    def complete_review(
        self,
        review_id: str,
        notes: str = "",
    ) -> ReviewCycle | None:
        """Complete review."""
        review = self.get(review_id)
        if not review:
            return None
        
        updated = ReviewCycle(
            id=review.id,
            product_id=review.product_id,
            status="completed",
            reviewers=review.reviewers,
            started_at=review.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            review_notes=notes,
            created_at=review.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=review.version + 1,
            metadata=review.metadata,
            author=review.author,
            reason=review.reason,
        )
        _storage._review_cycles[updated.id] = updated
        return updated


class ApprovalManager:
    """Manages approval workflows."""
    
    def create_approval(
        self,
        product_id: str,
        approval_type: str,
        author: str = "",
    ) -> ApprovalRecord:
        """Create approval record."""
        approval = ApprovalRecord(
            id=str(uuid4()),
            product_id=product_id,
            approval_type=approval_type,
            status="pending",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._approval_records[approval.id] = approval
        return approval
    
    def get(self, approval_id: str) -> ApprovalRecord | None:
        """Get approval by ID."""
        return _storage._approval_records.get(approval_id)
    
    def approve(
        self,
        approval_id: str,
        approver: Reviewer,
        notes: str = "",
    ) -> ApprovalRecord | None:
        """Approve."""
        approval = self.get(approval_id)
        if not approval:
            return None
        
        updated = ApprovalRecord(
            id=approval.id,
            product_id=approval.product_id,
            approval_type=approval.approval_type,
            status="approved",
            approver=approver,
            decision_at=datetime.now(timezone.utc).isoformat(),
            decision_notes=notes,
            approval_chain=approval.approval_chain,
            created_at=approval.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=approval.version + 1,
            metadata=approval.metadata,
            author=approval.author,
            reason=approval.reason,
        )
        _storage._approval_records[updated.id] = updated
        return updated


class PublicationManager:
    """Manages publications."""
    
    def create(
        self,
        product_id: str,
        author: str = "",
    ) -> Publication:
        """Create publication."""
        publication = Publication(
            id=str(uuid4()),
            product_id=product_id,
            status="draft",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._publications[publication.id] = publication
        return publication
    
    def get(self, publication_id: str) -> Publication | None:
        """Get publication by ID."""
        return _storage._publications.get(publication_id)
    
    def publish(
        self,
        publication_id: str,
        published_by: str,
    ) -> Publication | None:
        """Publish."""
        publication = self.get(publication_id)
        if not publication:
            return None
        
        updated = Publication(
            id=publication.id,
            product_id=publication.product_id,
            status="published",
            published_at=datetime.now(timezone.utc).isoformat(),
            published_by=published_by,
            publication_channels=publication.publication_channels,
            access_level=publication.access_level,
            history=publication.history,
            created_at=publication.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=publication.version + 1,
            metadata=publication.metadata,
            author=publication.author,
            reason=publication.reason,
        )
        _storage._publications[updated.id] = updated
        return updated


class GovernanceManager:
    """Manages governance decisions."""
    
    def create_decision(
        self,
        product_id: str,
        decision_type: str,
        decision: str,
        decision_made_by: Reviewer,
        notes: str = "",
        author: str = "",
    ) -> GovernanceDecision:
        """Create governance decision."""
        decision_record = GovernanceDecision(
            id=str(uuid4()),
            product_id=product_id,
            decision_type=decision_type,
            decision=decision,
            decision_made_by=decision_made_by,
            decision_at=datetime.now(timezone.utc).isoformat(),
            decision_notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._governance_decisions[decision_record.id] = decision_record
        return decision_record
    
    def get(self, decision_id: str) -> GovernanceDecision | None:
        """Get decision by ID."""
        return _storage._governance_decisions.get(decision_id)


class SourceAssessmentManager:
    """Manages source assessments - HUMAN GOVERNANCED ONLY."""
    
    def create_assessment(
        self,
        source_id: str,
        source_name: str,
        reliability: str,
        assessor: Reviewer,
        notes: str = "",
        author: str = "",
    ) -> SourceAssessment:
        """Create source assessment."""
        assessment = SourceAssessment(
            id=str(uuid4()),
            source_id=source_id,
            source_name=source_name,
            reliability=reliability,
            reliability_notes=notes,
            assessor=assessor,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._source_assessments[assessment.id] = assessment
        return assessment


class ConfidenceReviewManager:
    """Manages confidence reviews - HUMAN GOVERNANCED ONLY."""
    
    def create_review(
        self,
        product_id: str,
        assertion_id: str,
        confidence_level: str,
        reviewer: Reviewer,
        notes: str = "",
        author: str = "",
    ) -> ConfidenceReview:
        """Create confidence review."""
        review = ConfidenceReview(
            id=str(uuid4()),
            product_id=product_id,
            assertion_id=assertion_id,
            confidence_level=confidence_level,
            reviewer=reviewer,
            review_notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            author=author,
        )
        _storage._confidence_reviews[review.id] = review
        return review
