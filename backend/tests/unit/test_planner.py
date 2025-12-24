"""Unit tests for the Planner module.

Tests FR-001: System MUST deconstruct user queries into 3-10 structured sub-questions.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from backend.modules.planner import Planner, DEPTH_CONFIG, create_research_plan
from backend.models import AgenticResearchRequest, DepthLevel, SubQuestion, QuestionStatus


class TestPlannerModule:
    """Tests for the Planner class."""
    
    @pytest.fixture
    def planner(self):
        """Create a Planner instance with mocked LLM client."""
        p = Planner()
        p.llm_client = MagicMock()
        return p
    
    @pytest.fixture
    def sample_request(self):
        """Sample research request for testing."""
        return AgenticResearchRequest(
            id="test-123",
            query="Research Tesla's Q4 2023 performance",
            depth_level=DepthLevel.STANDARD
        )
    
    def test_depth_config_values(self):
        """Test that depth configurations have correct ranges."""
        assert DEPTH_CONFIG[DepthLevel.QUICK]["min_questions"] == 3
        assert DEPTH_CONFIG[DepthLevel.QUICK]["max_questions"] == 5
        assert DEPTH_CONFIG[DepthLevel.QUICK]["max_recursion"] == 1
        
        assert DEPTH_CONFIG[DepthLevel.STANDARD]["min_questions"] == 5
        assert DEPTH_CONFIG[DepthLevel.STANDARD]["max_questions"] == 7
        assert DEPTH_CONFIG[DepthLevel.STANDARD]["max_recursion"] == 2
        
        assert DEPTH_CONFIG[DepthLevel.COMPREHENSIVE]["min_questions"] == 7
        assert DEPTH_CONFIG[DepthLevel.COMPREHENSIVE]["max_questions"] == 10
        assert DEPTH_CONFIG[DepthLevel.COMPREHENSIVE]["max_recursion"] == 3
    
    @pytest.mark.asyncio
    async def test_create_plan_returns_research_plan(self, planner, sample_request):
        """Test that create_plan returns a valid ResearchPlan."""
        # Mock LLM response
        planner.llm_client.complete_json = AsyncMock(return_value={
            "sub_questions": [
                {"text": "What were Tesla's Q4 2023 revenue figures?", "priority": 1},
                {"text": "How did Tesla's stock perform in Q4 2023?", "priority": 2},
                {"text": "What production numbers did Tesla achieve?", "priority": 3}
            ],
            "estimated_time_seconds": 45
        })
        
        plan = await planner.create_plan(sample_request)
        
        assert plan is not None
        assert plan.request_id == sample_request.id
        assert len(plan.sub_questions) >= 3
        assert all(isinstance(q, SubQuestion) for q in plan.sub_questions)
    
    @pytest.mark.asyncio
    async def test_sub_questions_have_correct_status(self, planner, sample_request):
        """Test that generated sub-questions start with PENDING status."""
        planner.llm_client.complete_json = AsyncMock(return_value={
            "sub_questions": [
                {"text": "Question 1", "priority": 1},
            ]
        })
        
        plan = await planner.create_plan(sample_request)
        
        for question in plan.sub_questions:
            assert question.status == QuestionStatus.PENDING
            assert question.depth == 0
            assert question.parent_id is None
    
    @pytest.mark.asyncio
    async def test_fallback_questions_on_llm_failure(self, planner, sample_request):
        """Test that fallback questions are generated if LLM fails."""
        planner.llm_client.complete_json = AsyncMock(side_effect=Exception("LLM Error"))
        
        plan = await planner.create_plan(sample_request)
        
        # Should still get a plan with fallback questions
        assert plan is not None
        assert len(plan.sub_questions) >= 3
    
    def test_estimate_time_calculation(self, planner):
        """Test time estimation logic."""
        # More questions = more time
        time_5_q = planner._estimate_time(5, 2)
        time_10_q = planner._estimate_time(10, 2)
        
        assert time_10_q > time_5_q
        assert time_10_q <= 180  # Never exceeds 3 minutes (SC-010)
    
    @pytest.mark.asyncio
    async def test_comprehensive_depth_generates_more_questions(self):
        """Test that comprehensive mode generates more sub-questions than quick."""
        planner = Planner()
        planner.llm_client = MagicMock()
        
        # Quick mode
        quick_request = AgenticResearchRequest(
            id="quick-test",
            query="Test query",
            depth_level=DepthLevel.QUICK
        )
        
        comprehensive_request = AgenticResearchRequest(
            id="comp-test",
            query="Test query",
            depth_level=DepthLevel.COMPREHENSIVE
        )
        
        # Mock returns different counts based on depth config
        quick_config = DEPTH_CONFIG[DepthLevel.QUICK]
        comp_config = DEPTH_CONFIG[DepthLevel.COMPREHENSIVE]
        
        assert comp_config["max_questions"] > quick_config["max_questions"]


class TestPlannerConvenienceFunction:
    """Tests for the module-level convenience function."""
    
    @pytest.mark.asyncio
    async def test_create_research_plan_function(self):
        """Test the convenience function creates a plan."""
        request = AgenticResearchRequest(
            id="func-test",
            query="Research Apple stock performance",
            depth_level=DepthLevel.QUICK
        )
        
        with patch('backend.modules.planner.Planner') as MockPlanner:
            mock_instance = MockPlanner.return_value
            mock_instance.create_plan = AsyncMock()
            
            await create_research_plan(request)
            
            mock_instance.create_plan.assert_called_once_with(request)
