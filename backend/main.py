"""Main FastAPI application for the Configurable Researcher Agent."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os

from backend.config import settings, RESEARCH_MODULES
from backend.models import (
    ResearchRequest, ResearchResponse, HealthResponse,
    ModuleInfo, ReportRequest, EntityType
)
from backend.modules import ResearcherManager
from backend.utils.report_generator import ReportGenerator
from backend.utils.search import PROVIDER_MAP

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A highly configurable AI-powered researcher agent that performs multiple types of searches and generates beautiful reports."
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize report generator
report_generator = ReportGenerator(settings.REPORTS_DIR)

# Serve reports directory
if os.path.exists(settings.REPORTS_DIR):
    app.mount("/reports", StaticFiles(directory=settings.REPORTS_DIR), name="reports")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Configurable Researcher Agent API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/api/health", tags=["System"])
async def health_check():
    """Detailed system health check."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": settings.VERSION,
        "services": {
            "api": "ok",
            "llm": "unknown"
        }
    }
    
    # Check LLM configuration
    try:
        from backend.utils.llm_utils import get_llm_client, TaskType
        client = get_llm_client()
        if not (client.openai_client or client.google_client):
            health_status["services"]["llm"] = "configured_but_missing_key"
            health_status["status"] = "degraded"
        else:
             health_status["services"]["llm"] = "ok"
    except Exception as e:
        health_status["services"]["llm"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    return health_status

@app.get("/api/v1/health")
async def health_check_v1():
    """Legacy health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.now()
    }

@app.get(f"{settings.API_PREFIX}/modules", response_model=List[ModuleInfo])
async def get_modules():
    """Get all available research modules."""
    modules = []
    for module_id, module_data in RESEARCH_MODULES.items():
        modules.append(ModuleInfo(
            id=module_id,
            name=module_data["name"],
            description=module_data["description"],
            fields=module_data["fields"],
            icon=module_data["icon"],
            color=module_data["color"]
        ))
    return modules


@app.get(f"{settings.API_PREFIX}/providers", response_model=List[str])
async def get_providers():
    """Get all available search providers."""
    return list(PROVIDER_MAP.keys())


@app.post(f"{settings.API_PREFIX}/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """Perform research on an entity."""
    try:
        # Validate research types
        invalid_types = [rt for rt in request.research_types if rt not in RESEARCH_MODULES]
        if invalid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid research types: {invalid_types}"
            )
        
        # Perform research
        manager = ResearcherManager(request.entity_name, request.entity_type.value)
        results = await manager.perform_research(request.research_types, request.selected_providers)
        
        # Generate report
        report_id = None
        if results:
            try:
                report_id = report_generator.generate_pdf_report(
                    request.entity_name,
                    request.entity_type,
                    results
                )
            except Exception as e:
                print(f"Report generation failed: {e}")
        
        return ResearchResponse(
            entity_name=request.entity_name,
            entity_type=request.entity_type,
            results=results,
            total_results=len(results),
            report_id=report_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_PREFIX}/generate-report")
async def generate_report(request: ReportRequest):
    """Generate a report from research results."""
    try:
        if request.format == "pdf":
            report_id = report_generator.generate_pdf_report(
                request.entity_name,
                request.entity_type,
                request.results
            )
        elif request.format == "html":
            report_id = report_generator.generate_html_report(
                request.entity_name,
                request.entity_type,
                request.results
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use 'pdf' or 'html'")
        
        filename = f"{report_id}_{request.entity_name.replace(' ', '_')}_report.{request.format}"
        
        return {
            "report_id": report_id,
            "filename": filename,
            "url": f"/reports/{filename}",
            "format": request.format
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== AGENTIC RESEARCH ENDPOINTS (Per contracts/research-api.yaml) =====
# T021-T025: Integrated with actual workflow modules

from backend.models import (
    AgenticResearchRequest, ResearchPlan, ResearchProgress,
    DepthLevel, WorkflowStatus
)
from backend.modules.planner import Planner
from backend.modules.agentic_workflow import get_workflow, AgenticWorkflow
from backend.utils.logging_utils import get_logger, log_workflow_event
import uuid
import asyncio
from datetime import datetime

# Structured logging per NFR-003 to NFR-006 (T025)
api_logger = get_logger("research_api")

# In-memory storage for research sessions (extend to database later per FR-020)
_research_sessions = {}
_workflow = None


def _get_workflow() -> AgenticWorkflow:
    """Get or create the workflow instance."""
    global _workflow
    if _workflow is None:
        _workflow = AgenticWorkflow()
    return _workflow


@app.post("/api/research/plan", response_model=ResearchPlan)
async def generate_research_plan(query: str, depth_level: DepthLevel = DepthLevel.STANDARD):
    """Generate a research plan by deconstructing a query into sub-questions.
    
    Per FR-001: System MUST deconstruct user queries into 3-10 structured sub-questions.
    
    This is a preview endpoint - returns plan without executing searches.
    """
    # T021: Integrated with Planner module
    request_id = str(uuid.uuid4())
    
    log_workflow_event(api_logger, "plan_request", request_id, "planning", query=query[:50])
    
    # Create request for planner
    request = AgenticResearchRequest(
        id=request_id,
        query=query,
        depth_level=depth_level
    )
    
    planner = Planner()
    plan = await planner.create_plan(request)
    
    log_workflow_event(
        api_logger, "plan_created", request_id, "planning",
        num_questions=len(plan.sub_questions)
    )
    
    return plan


async def _run_research_async(request: AgenticResearchRequest, session_id: str):
    """Background task to run the full research workflow."""
    workflow = _get_workflow()
    
    try:
        async def progress_callback(progress):
            _research_sessions[session_id].update(progress)
        
        report = await workflow.execute(request, progress_callback)
        
        # Store completed report
        _research_sessions[session_id]["report"] = report.to_dict()
        _research_sessions[session_id]["status"] = WorkflowStatus.COMPLETED.value
        _research_sessions[session_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        _research_sessions[session_id]["status"] = WorkflowStatus.FAILED.value
        _research_sessions[session_id]["error_message"] = str(e)


@app.post("/api/research/execute")
async def execute_research(request: AgenticResearchRequest):
    """Execute the full research workflow (Plan-Execute-Verify-Synthesize).
    
    Returns immediately with request_id for async polling.
    Use GET /api/research/{id}/status to poll progress.
    Use GET /api/research/{id}/report to retrieve completed report.
    """
    # T022: Integrated with workflow orchestrator
    request_id = request.id if request.id else str(uuid.uuid4())
    request.id = request_id
    
    log_workflow_event(
        api_logger, "research_started", request_id, "init",
        query=request.query[:50], depth_level=request.depth_level.value
    )
    
    # Initialize session in storage
    _research_sessions[request_id] = {
        "request": request.model_dump(),
        "status": WorkflowStatus.PLANNING.value,
        "current_stage": "initializing",
        "progress_percent": 0,
        "questions_completed": 0,
        "questions_total": 0,
        "plan": None,
        "report": None,
        "started_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    # Start async task (fire and forget for now)
    asyncio.create_task(_run_research_async(request, request_id))
    
    # Return immediately for async polling
    return {
        "request_id": request_id,
        "status": "planning",
        "message": "Research started. Poll /api/research/{id}/status for updates.",
        "estimated_completion_seconds": 60
    }


@app.get("/api/research/{request_id}/status", response_model=ResearchProgress)
async def get_research_status(request_id: str):
    """Get the current status and progress of a research request.
    
    Per SC-010: Research completion time must be under 3 minutes.
    """
    # T023: Returns actual progress from workflow
    if request_id not in _research_sessions:
        raise HTTPException(status_code=404, detail=f"Research request {request_id} not found")
    
    session = _research_sessions[request_id]
    
    # Check if workflow has progress
    workflow = _get_workflow()
    workflow_progress = workflow.get_progress(request_id)
    
    if workflow_progress:
        return workflow_progress
    
    # Fall back to session data
    return ResearchProgress(
        request_id=request_id,
        status=WorkflowStatus(session.get("status", "pending")),
        current_stage=session.get("current_stage", "initializing"),
        progress_percent=session.get("progress_percent", 0),
        questions_completed=session.get("questions_completed", 0),
        questions_total=session.get("questions_total", 0),
        started_at=datetime.fromisoformat(session["started_at"]),
        completed_at=datetime.fromisoformat(session["completed_at"]) if session.get("completed_at") else None
    )


@app.get("/api/research/{request_id}/report")
async def get_research_report(request_id: str):
    """Retrieve the completed narrative report.
    
    Per FR-007: Reports must have minimum 300 words per major section.
    Per FR-008: Reports must be in professional journalism style.
    """
    # T024: Returns actual report from synthesizer
    if request_id not in _research_sessions:
        raise HTTPException(status_code=404, detail=f"Research request {request_id} not found")
    
    session = _research_sessions[request_id]
    status = session.get("status", "pending")
    
    if status != WorkflowStatus.COMPLETED.value and status != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Research not complete. Current status: {status}"
        )
    
    report = session.get("report")
    if not report:
        raise HTTPException(
            status_code=500,
            detail="Report not found - workflow may have failed"
        )
    
    log_workflow_event(api_logger, "report_retrieved", request_id, "complete")
    return report


@app.get("/api/research/{request_id}/citations")
async def get_research_citations(request_id: str):
    """Get all citations/sources for a research report.
    
    Per FR-006: System MUST track source URL and timestamp for every fact.
    Per FR-013: System MUST provide complete bibliography/source list.
    """
    # TODO: Implement in T046 (US3)
    if request_id not in _research_sessions:
        raise HTTPException(status_code=404, detail=f"Research request {request_id} not found")
    
    return {
        "request_id": request_id,
        "citations": [],
        "total_sources": 0
    }


@app.get("/api/citations/fact/{fact_id}")
async def get_fact_citation(fact_id: str):
    """Get the source details for a specific fact/claim.
    
    Per FR-012: System MUST render claims with clickable inline citations.
    """
    # TODO: Implement in T047 (US3)
    raise HTTPException(status_code=404, detail=f"Fact {fact_id} not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

