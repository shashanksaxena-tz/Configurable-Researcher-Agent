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
    
    class Config:
        json_schema_extra = {
            "example": {
                "entity_name": "Tesla Inc",
                "entity_type": "company",
                "research_types": ["financial", "news", "sentiment"]
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
