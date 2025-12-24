"""Data models for the Configurable Researcher Agent."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class EntityType(str, Enum):
    """Type of entity to research."""
    INDIVIDUAL = "individual"
    COMPANY = "company"


class ResearchRequest(BaseModel):
    """Request model for research."""
    entity_name: str = Field(..., description="Name of the person or company to research")
    entity_type: EntityType = Field(..., description="Type of entity")
    research_types: List[str] = Field(..., description="List of research types to perform")
    selected_providers: Optional[List[str]] = Field(None, description="List of search providers to use")
    
    class Config:
        json_schema_extra = {
            "example": {
                "entity_name": "Tesla Inc",
                "entity_type": "company",
                "research_types": ["financial", "news", "sentiment"],
                "selected_providers": ["duckduckgo", "google_news", "linkedin"]
            }
        }


class ResearchResult(BaseModel):
    """Result model for a single research type."""
    research_type: str
    title: str
    data: Dict[str, Any]
    summary: str
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    timestamp: datetime = Field(default_factory=datetime.now)


class ResearchResponse(BaseModel):
    """Response model for research."""
    entity_name: str
    entity_type: EntityType
    results: List[ResearchResult]
    total_results: int
    timestamp: datetime = Field(default_factory=datetime.now)
    report_id: Optional[str] = None


class ModuleInfo(BaseModel):
    """Information about a research module."""
    id: str
    name: str
    description: str
    fields: List[str]
    icon: str
    color: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    app_name: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ReportRequest(BaseModel):
    """Request model for report generation."""
    entity_name: str
    entity_type: EntityType
    results: List[ResearchResult]
    format: str = Field(default="pdf", description="Report format (pdf or html)")


# ===== AGENTIC WORKFLOW MODELS (Per data-model.md) =====

class DepthLevel(str, Enum):
    """Research depth levels (per FR-004, User Story 4)."""
    QUICK = "quick"  # 3-5 sub-questions, 1 level recursion
    STANDARD = "standard"  # 5-7 sub-questions, 2 levels recursion
    COMPREHENSIVE = "comprehensive"  # 7-10 sub-questions, 3 levels recursion


class QuestionStatus(str, Enum):
    """Status of a sub-question in the research plan."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SubQuestion(BaseModel):
    """A specific research sub-question (per data-model.md).
    
    FR-001: System MUST deconstruct user queries into 3-10 structured sub-questions.
    """
    id: str = Field(..., description="Unique identifier (UUID)")
    text: str = Field(..., description="The sub-question text")
    priority: int = Field(..., ge=1, le=10, description="Priority ranking (1=highest)")
    parent_id: Optional[str] = Field(None, description="Parent question ID for recursive searches")
    depth: int = Field(default=0, ge=0, le=3, description="Recursion depth level")
    status: QuestionStatus = Field(default=QuestionStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)


class ResearchPlan(BaseModel):
    """Generated research plan with sub-questions (per data-model.md).
    
    The planner module generates this from a user query.
    """
    id: str = Field(..., description="Unique plan identifier (UUID)")
    request_id: str = Field(..., description="Reference to parent ResearchRequest")
    sub_questions: List[SubQuestion] = Field(default_factory=list)
    estimated_time_seconds: int = Field(default=60, description="Estimated completion time")
    created_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def total_questions(self) -> int:
        return len(self.sub_questions)
    
    @property
    def completed_questions(self) -> int:
        return sum(1 for q in self.sub_questions if q.status == QuestionStatus.COMPLETED)


class AgenticResearchRequest(BaseModel):
    """Extended research request for the agentic workflow (per data-model.md).
    
    This extends the basic ResearchRequest with depth control per User Story 4.
    """
    id: str = Field(..., description="Unique request identifier (UUID)")
    query: str = Field(..., min_length=10, max_length=500, description="User's research query")
    depth_level: DepthLevel = Field(default=DepthLevel.STANDARD, description="Research depth")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "query": "Research Tesla's Q4 2023 performance and market outlook",
                "depth_level": "standard"
            }
        }


class WorkflowStatus(str, Enum):
    """Status of the agentic research workflow."""
    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchProgress(BaseModel):
    """Progress tracking for an in-flight research request."""
    request_id: str
    status: WorkflowStatus = Field(default=WorkflowStatus.PENDING)
    current_stage: str = Field(default="initializing")
    progress_percent: int = Field(default=0, ge=0, le=100)
    questions_completed: int = Field(default=0)
    questions_total: int = Field(default=0)
    estimated_time_remaining_seconds: Optional[int] = None
    error_message: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


# ===== ADDITIONAL MODELS FOR RESEARCH PIPELINE (T019) =====

class SearchResultModel(BaseModel):
    """Search result with source tracking (per FR-006).
    
    Tracks source URL and timestamp for every piece of extracted information.
    """
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    url: str
    title: str
    snippet: str
    source_provider: str = Field(default="duckduckgo")
    extraction_timestamp: datetime = Field(default_factory=datetime.now)
    language: str = Field(default="en")
    relevance_score: float = Field(default=0.5, ge=0.0, le=1.0)


class Fact(BaseModel):
    """Extracted fact/claim with source citation (per FR-006).
    
    Every fact must be traceable to at least one source URL with timestamp.
    """
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    claim: str = Field(..., min_length=10, description="The factual claim text")
    source_urls: List[str] = Field(..., min_items=1, description="Source URLs (per SC-002)")
    source_timestamps: List[datetime] = Field(default_factory=list)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    verified: bool = Field(default=False)
    question_id: Optional[str] = None  # Link to SubQuestion


class DiscrepancyModel(BaseModel):
    """Conflicting information from multiple sources (per FR-009).
    
    When conflicting data exists, all sources are cited with discrepancy notes.
    """
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    topic: str
    conflicting_claims: List[Dict[str, Any]]
    resolution_notes: str
    preferred_claim: Optional[str] = None
    resolution_basis: str = Field(default="unknown")  # recency, credibility, consensus


class ReportSection(BaseModel):
    """A section of the narrative report (per FR-007).
    
    Each major section must have minimum 300 words.
    """
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    title: str
    content: str
    word_count: int = Field(ge=0)
    citation_ids: List[str] = Field(default_factory=list)
    category: str
    
    @property
    def meets_word_minimum(self) -> bool:
        """Check if section meets FR-007 minimum (300 words)."""
        return self.word_count >= 300


class NarrativeReportModel(BaseModel):
    """Complete narrative research report (per FR-007, FR-008).
    
    Professional journalism style with executive summary and tabbed sections.
    """
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    request_id: str
    query: str
    executive_summary: str
    sections: List[ReportSection] = Field(default_factory=list)
    discrepancies: List[DiscrepancyModel] = Field(default_factory=list)
    total_word_count: int = Field(default=0, ge=0)
    total_sources: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def meets_quality_thresholds(self) -> bool:
        """Validate report meets quality requirements (per FR-019)."""
        # FR-007: 300+ words per section
        sections_valid = all(s.meets_word_minimum for s in self.sections)
        # SC-004: 3+ sources per section
        sources_valid = self.total_sources >= (len(self.sections) * 3)
        return sections_valid and sources_valid


# ===== VALIDATORS (T020) =====

def validate_word_count(text: str, minimum: int = 300) -> bool:
    """Validate that text meets minimum word count (per FR-007).
    
    Args:
        text: The text to validate
        minimum: Minimum word count (default 300 per FR-007)
        
    Returns:
        True if text meets minimum word count
    """
    return len(text.split()) >= minimum


def validate_source_count(sources: List[str], minimum: int = 3) -> bool:
    """Validate that a section has minimum source count (per SC-004).
    
    Args:
        sources: List of source URLs
        minimum: Minimum sources required (default 3 per SC-004)
        
    Returns:
        True if minimum sources met
    """
    return len(set(sources)) >= minimum


