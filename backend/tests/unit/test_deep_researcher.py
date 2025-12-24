"""Unit tests for the DeepResearcher module.

Tests:
- FR-002: System MUST execute independent searches for each sub-question
- FR-003: System MUST perform recursive searches for relevant new topics
- FR-004: System MUST implement recursion depth limit
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from backend.modules.deep_researcher import DeepResearcher, ResearchFinding, execute_research
from backend.models import ResearchPlan, SubQuestion, DepthLevel, QuestionStatus


class TestDeepResearcherModule:
    """Tests for the DeepResearcher class."""
    
    @pytest.fixture
    def researcher(self):
        """Create a DeepResearcher with mocked clients."""
        r = DeepResearcher()
        r.llm_client = MagicMock()
        r.search_client = MagicMock()
        return r
    
    @pytest.fixture
    def sample_plan(self):
        """Sample research plan with sub-questions."""
        return ResearchPlan(
            id="plan-123",
            request_id="req-123",
            sub_questions=[
                SubQuestion(
                    id="q1",
                    text="What is Tesla's revenue?",
                    priority=1,
                    parent_id=None,
                    depth=0,
                    status=QuestionStatus.PENDING
                ),
                SubQuestion(
                    id="q2",
                    text="What is Tesla's market cap?",
                    priority=2,
                    parent_id=None,
                    depth=0,
                    status=QuestionStatus.PENDING
                )
            ],
            estimated_time_seconds=60
        )
    
    def test_max_depth_initialization(self, researcher):
        """Test that max recursion depth is initialized correctly."""
        assert researcher.max_depth >= 1
        assert researcher.max_depth <= 3
    
    def test_max_depth_by_depth_level(self):
        """Test max depth configuration for different depth levels."""
        quick_researcher = DeepResearcher(max_depth=1)
        standard_researcher = DeepResearcher(max_depth=2)
        comprehensive_researcher = DeepResearcher(max_depth=3)
        
        assert quick_researcher.max_depth == 1
        assert standard_researcher.max_depth == 2
        assert comprehensive_researcher.max_depth == 3
    
    @pytest.mark.asyncio
    async def test_execute_research_returns_findings(self, researcher, sample_plan):
        """Test that execute_research returns ResearchFinding objects."""
        # Mock search results
        mock_search_result = MagicMock()
        mock_search_result.url = "https://example.com"
        mock_search_result.title = "Tesla Revenue 2023"
        mock_search_result.snippet = "Tesla reported $25B revenue"
        
        researcher.search_client.search_all_providers = AsyncMock(return_value=[mock_search_result])
        
        # Mock LLM extraction
        researcher.llm_client.complete_json = AsyncMock(return_value={
            "extracted_facts": ["Tesla reported $25 billion in revenue for Q4 2023"],
            "confidence": 0.85,
            "new_topics_to_research": []
        })
        
        findings = await researcher.execute_research(sample_plan, DepthLevel.QUICK)
        
        assert isinstance(findings, list)
        # Should have processed the questions
        assert sample_plan.sub_questions[0].status in [QuestionStatus.COMPLETED, QuestionStatus.FAILED]
    
    @pytest.mark.asyncio
    async def test_visited_topics_prevents_duplicates(self, researcher):
        """Test that visited topics set prevents duplicate searches."""
        researcher.visited_topics.add("what is tesla's revenue?")
        
        question = SubQuestion(
            id="dup-q",
            text="What is Tesla's revenue?",  # Same normalized query
            priority=1,
            parent_id=None,
            depth=0
        )
        
        findings = await researcher._research_question(question, depth=0)
        
        # Should return empty - query already visited
        assert findings == []
    
    @pytest.mark.asyncio
    async def test_max_depth_stops_recursion(self, researcher):
        """Test that recursion stops at max depth (FR-004)."""
        researcher.max_depth = 2
        
        question = SubQuestion(
            id="deep-q",
            text="Deep question",
            priority=1,
            parent_id=None,
            depth=3  # Exceeds max_depth
        )
        
        findings = await researcher._research_question(question, depth=3)
        
        # Should return empty - depth limit reached
        assert findings == []
    
    @pytest.mark.asyncio
    async def test_no_search_results_returns_empty(self, researcher):
        """Test handling of queries with no search results."""
        researcher.search_client.search_all_providers = AsyncMock(return_value=[])
        
        question = SubQuestion(
            id="empty-q",
            text="Obscure topic with no results",
            priority=1,
            parent_id=None,
            depth=0
        )
        
        findings = await researcher._research_question(question, depth=0)
        
        assert findings == []


class TestResearchFinding:
    """Tests for the ResearchFinding dataclass."""
    
    def test_finding_to_dict(self):
        """Test ResearchFinding serialization."""
        finding = ResearchFinding(
            id="f1",
            question_id="q1",
            content="Test content",
            source_url="https://example.com",
            source_title="Example",
            extraction_timestamp=datetime.now(),
            confidence=0.9,
            triggers_recursion=True,
            recursion_topics=["topic1"]
        )
        
        result = finding.to_dict()
        
        assert result["id"] == "f1"
        assert result["content"] == "Test content"
        assert result["source_url"] == "https://example.com"
        assert result["triggers_recursion"] == True
        assert "topic1" in result["recursion_topics"]


class TestConvenienceFunction:
    """Tests for the module-level convenience function."""
    
    @pytest.mark.asyncio
    async def test_execute_research_function(self):
        """Test the convenience function."""
        plan = ResearchPlan(
            id="func-plan",
            request_id="func-req",
            sub_questions=[],
            estimated_time_seconds=30
        )
        
        with patch('backend.modules.deep_researcher.DeepResearcher') as MockResearcher:
            mock_instance = MockResearcher.return_value
            mock_instance.execute_research = AsyncMock(return_value=[])
            
            await execute_research(plan, DepthLevel.STANDARD)
            
            mock_instance.execute_research.assert_called_once()
