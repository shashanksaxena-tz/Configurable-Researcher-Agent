"""Agentic Workflow Orchestrator - Coordinates Plan-Execute-Verify-Synthesize.

This is the main orchestrator that ties together all agentic modules
to execute the full research workflow.

Flow:
1. PLAN: Planner deconstructs query into sub-questions
2. EXECUTE: DeepResearcher performs searches with recursion
3. VERIFY: Verifier cross-references and detects discrepancies  
4. SYNTHESIZE: Synthesizer generates narrative report
"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

from backend.models import (
    AgenticResearchRequest, ResearchPlan, ResearchProgress,
    DepthLevel, WorkflowStatus
)
from backend.modules.planner import Planner, create_research_plan
from backend.modules.deep_researcher import DeepResearcher, execute_research
from backend.modules.verifier import Verifier, verify_findings
from backend.modules.synthesizer import Synthesizer, generate_report, NarrativeReport
from backend.utils.logging_utils import get_logger, StageTimer, log_workflow_event


logger = get_logger(__name__)


class AgenticWorkflow:
    """Orchestrates the full Plan-Execute-Verify-Synthesize workflow.
    
    This class manages the complete research lifecycle and provides
    progress updates throughout the process.
    """
    
    def __init__(self):
        self.planner = Planner()
        self.researcher = DeepResearcher()
        self.verifier = Verifier()
        self.synthesizer = Synthesizer()
        
        # Progress tracking
        self.progress: Dict[str, Any] = {}
    
    async def execute(
        self,
        request: AgenticResearchRequest,
        progress_callback: Optional[callable] = None
    ) -> NarrativeReport:
        """Execute the complete agentic research workflow.
        
        Args:
            request: The research request
            progress_callback: Optional callback for progress updates
            
        Returns:
            NarrativeReport with complete research results
        """
        request_id = request.id
        
        # Initialize progress
        self._update_progress(request_id, WorkflowStatus.PENDING, "initializing", 0)
        
        log_workflow_event(
            logger, "workflow_started", request_id, "init",
            query=request.query[:50], depth_level=request.depth_level.value
        )
        
        try:
            # ===== PHASE 1: PLANNING =====
            self._update_progress(request_id, WorkflowStatus.PLANNING, "creating research plan", 5)
            if progress_callback:
                await progress_callback(self.progress[request_id])
            
            plan = await self.planner.create_plan(request)
            
            self._update_progress(
                request_id, WorkflowStatus.PLANNING, "plan created",
                10, questions_total=len(plan.sub_questions)
            )
            
            log_workflow_event(
                logger, "planning_complete", request_id, "planning",
                num_questions=len(plan.sub_questions)
            )
            
            # ===== PHASE 2: EXECUTING =====
            self._update_progress(request_id, WorkflowStatus.EXECUTING, "searching and extracting", 15)
            if progress_callback:
                await progress_callback(self.progress[request_id])
            
            findings = await self.researcher.execute_research(plan, request.depth_level)
            
            self._update_progress(
                request_id, WorkflowStatus.EXECUTING, "search complete",
                50, questions_completed=plan.completed_questions
            )
            
            log_workflow_event(
                logger, "execution_complete", request_id, "executing",
                num_findings=len(findings)
            )
            
            # ===== PHASE 3: VERIFYING =====
            self._update_progress(request_id, WorkflowStatus.VERIFYING, "cross-referencing sources", 60)
            if progress_callback:
                await progress_callback(self.progress[request_id])
            
            verified_facts, discrepancies = await self.verifier.verify_findings(
                findings, request_id
            )
            
            self._update_progress(
                request_id, WorkflowStatus.VERIFYING, "verification complete", 75
            )
            
            log_workflow_event(
                logger, "verification_complete", request_id, "verifying",
                verified_facts=len(verified_facts), discrepancies=len(discrepancies)
            )
            
            # ===== PHASE 4: SYNTHESIZING =====
            self._update_progress(request_id, WorkflowStatus.SYNTHESIZING, "generating report", 80)
            if progress_callback:
                await progress_callback(self.progress[request_id])
            
            report = await self.synthesizer.generate_report(
                request_id=request_id,
                query=request.query,
                verified_facts=verified_facts,
                discrepancies=discrepancies
            )
            
            self._update_progress(
                request_id, WorkflowStatus.COMPLETED, "complete", 100
            )
            
            log_workflow_event(
                logger, "workflow_completed", request_id, "complete",
                sections=len(report.sections), word_count=report.total_word_count
            )
            
            return report
            
        except Exception as e:
            self._update_progress(
                request_id, WorkflowStatus.FAILED, 
                f"error: {str(e)[:50]}", 
                self.progress.get(request_id, {}).get("progress_percent", 0)
            )
            
            log_workflow_event(
                logger, "workflow_failed", request_id, "error",
                error=str(e)
            )
            raise
    
    def _update_progress(
        self,
        request_id: str,
        status: WorkflowStatus,
        stage: str,
        percent: int,
        **kwargs
    ):
        """Update the progress tracking for a request.
        
        Args:
            request_id: The research request ID
            status: Current workflow status
            stage: Current stage description
            percent: Progress percentage (0-100)
            **kwargs: Additional fields to update
        """
        if request_id not in self.progress:
            self.progress[request_id] = {
                "request_id": request_id,
                "started_at": datetime.now().isoformat(),
                "questions_total": 0,
                "questions_completed": 0
            }
        
        self.progress[request_id].update({
            "status": status.value,
            "current_stage": stage,
            "progress_percent": percent,
            **kwargs
        })
        
        if status == WorkflowStatus.COMPLETED:
            self.progress[request_id]["completed_at"] = datetime.now().isoformat()
    
    def get_progress(self, request_id: str) -> Optional[ResearchProgress]:
        """Get the current progress for a request.
        
        Args:
            request_id: The research request ID
            
        Returns:
            ResearchProgress or None if not found
        """
        if request_id not in self.progress:
            return None
        
        p = self.progress[request_id]
        return ResearchProgress(
            request_id=request_id,
            status=WorkflowStatus(p.get("status", "pending")),
            current_stage=p.get("current_stage", "unknown"),
            progress_percent=p.get("progress_percent", 0),
            questions_completed=p.get("questions_completed", 0),
            questions_total=p.get("questions_total", 0),
            started_at=datetime.fromisoformat(p["started_at"]),
            completed_at=datetime.fromisoformat(p["completed_at"]) if p.get("completed_at") else None
        )


# Global workflow instance
_workflow: Optional[AgenticWorkflow] = None


def get_workflow() -> AgenticWorkflow:
    """Get or create the global workflow instance."""
    global _workflow
    if _workflow is None:
        _workflow = AgenticWorkflow()
    return _workflow


async def run_research(request: AgenticResearchRequest) -> NarrativeReport:
    """Convenience function to run the complete research workflow.
    
    Args:
        request: The research request
        
    Returns:
        NarrativeReport with complete results
    """
    workflow = get_workflow()
    return await workflow.execute(request)
