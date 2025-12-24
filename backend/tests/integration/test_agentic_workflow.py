"""Integration test for the full agentic workflow.

Tests the complete Plan-Execute-Verify-Synthesize pipeline.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from backend.modules.agentic_workflow import AgenticWorkflow, get_workflow, run_research
from backend.models import AgenticResearchRequest, DepthLevel, WorkflowStatus


class TestAgenticWorkflowIntegration:
    """Integration tests for the complete workflow."""
    
    @pytest.fixture
    def workflow(self):
        """Create a workflow with all mocked components."""
        w = AgenticWorkflow()
        w.planner = MagicMock()
        w.researcher = MagicMock()
        w.verifier = MagicMock()
        w.synthesizer = MagicMock()
        return w
    
    @pytest.fixture
    def sample_request(self):
        """Sample research request."""
        return AgenticResearchRequest(
            id="integration-test-123",
            query="Research Tesla Q4 2023 financial performance",
            depth_level=DepthLevel.STANDARD
        )
    
    @pytest.mark.asyncio
    async def test_workflow_executes_all_stages(self, workflow, sample_request):
        """Test that all 4 stages are executed in order."""
        # Mock planner
        mock_plan = MagicMock()
        mock_plan.sub_questions = []
        mock_plan.completed_questions = 0
        workflow.planner.create_plan = AsyncMock(return_value=mock_plan)
        
        # Mock researcher
        workflow.researcher.execute_research = AsyncMock(return_value=[])
        
        # Mock verifier
        workflow.verifier.verify_findings = AsyncMock(return_value=([], []))
        
        # Mock synthesizer
        mock_report = MagicMock()
        mock_report.sections = []
        mock_report.total_word_count = 100
        workflow.synthesizer.generate_report = AsyncMock(return_value=mock_report)
        
        result = await workflow.execute(sample_request)
        
        # All stages should have been called
        workflow.planner.create_plan.assert_called_once()
        workflow.researcher.execute_research.assert_called_once()
        workflow.verifier.verify_findings.assert_called_once()
        workflow.synthesizer.generate_report.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_workflow_progress_tracking(self, workflow, sample_request):
        """Test that progress is tracked throughout execution."""
        # Mock all components to return immediately
        mock_plan = MagicMock()
        mock_plan.sub_questions = []
        mock_plan.completed_questions = 0
        
        workflow.planner.create_plan = AsyncMock(return_value=mock_plan)
        workflow.researcher.execute_research = AsyncMock(return_value=[])
        workflow.verifier.verify_findings = AsyncMock(return_value=([], []))
        
        mock_report = MagicMock()
        mock_report.sections = []
        mock_report.total_word_count = 100
        workflow.synthesizer.generate_report = AsyncMock(return_value=mock_report)
        
        progress_updates = []
        
        async def capture_progress(progress):
            progress_updates.append(progress.copy())
        
        await workflow.execute(sample_request, progress_callback=capture_progress)
        
        # Should have progress updates
        assert len(progress_updates) >= 3  # At least planning, executing, verifying
    
    @pytest.mark.asyncio
    async def test_workflow_handles_failure(self, workflow, sample_request):
        """Test that workflow handles stage failures correctly."""
        workflow.planner.create_plan = AsyncMock(side_effect=Exception("Planning failed"))
        
        with pytest.raises(Exception) as exc_info:
            await workflow.execute(sample_request)
        
        assert "Planning failed" in str(exc_info.value)
        
        # Status should be FAILED
        progress = workflow.get_progress(sample_request.id)
        assert progress.status == WorkflowStatus.FAILED
    
    def test_get_progress_for_unknown_request(self, workflow):
        """Test that get_progress returns None for unknown requests."""
        progress = workflow.get_progress("unknown-id")
        assert progress is None


class TestWorkflowFactory:
    """Tests for workflow factory functions."""
    
    def test_get_workflow_returns_singleton(self):
        """Test that get_workflow returns the same instance."""
        w1 = get_workflow()
        w2 = get_workflow()
        
        assert w1 is w2
    
    @pytest.mark.asyncio
    async def test_run_research_convenience_function(self):
        """Test the run_research convenience function."""
        request = AgenticResearchRequest(
            id="convenience-test",
            query="Test query",
            depth_level=DepthLevel.QUICK
        )
        
        with patch('backend.modules.agentic_workflow.get_workflow') as mock_get:
            mock_workflow = MagicMock()
            mock_workflow.execute = AsyncMock()
            mock_get.return_value = mock_workflow
            
            await run_research(request)
            
            mock_workflow.execute.assert_called_once_with(request)


class TestEndToEndFlow:
    """End-to-end tests (optional, require actual LLM keys)."""
    
    @pytest.mark.skip(reason="Requires LLM API keys - manual test only")
    @pytest.mark.asyncio
    async def test_real_research_flow(self):
        """Test a real research request (requires API keys)."""
        workflow = AgenticWorkflow()
        
        request = AgenticResearchRequest(
            id="e2e-test",
            query="What is the current price of Bitcoin?",
            depth_level=DepthLevel.QUICK
        )
        
        report = await workflow.execute(request)
        
        assert report is not None
        assert len(report.sections) > 0
        assert report.total_word_count > 0
