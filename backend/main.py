"""Main FastAPI application for the Configurable Researcher Agent."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os

from config import settings, RESEARCH_MODULES
from models import (
    ResearchRequest, ResearchResponse, HealthResponse,
    ModuleInfo, ReportRequest, EntityType
)
from modules import ResearcherManager
from utils.report_generator import ReportGenerator

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


@app.get(f"{settings.API_PREFIX}/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.VERSION
    )


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
        results = await manager.perform_research(request.research_types)
        
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
