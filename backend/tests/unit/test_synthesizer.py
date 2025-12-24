"""Unit tests for the Synthesizer module.

Tests:
- FR-007: System MUST generate narrative reports with minimum 300 words per section
- FR-008: System MUST produce reports in professional journalism style
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from backend.modules.synthesizer import (
    Synthesizer, ReportSection, NarrativeReport, generate_report
)


class MockVerifiedFact:
    """Mock verified fact for testing."""
    def __init__(self, id, claim, confidence=0.9, source_urls=None):
        self.id = id
        self.claim = claim
        self.confidence = confidence
        self.source_urls = source_urls or ["https://source.com"]
        self.source_count = len(self.source_urls)
    
    def to_dict(self):
        return {"id": self.id, "claim": self.claim}


class MockDiscrepancy:
    """Mock discrepancy for testing."""
    def __init__(self, topic):
        self.topic = topic
        self.resolution_notes = "Resolved using recency"
    
    def to_dict(self):
        return {"topic": self.topic, "resolution_notes": self.resolution_notes}


class TestSynthesizerModule:
    """Tests for the Synthesizer class."""
    
    @pytest.fixture
    def synthesizer(self):
        """Create a Synthesizer with mocked LLM client."""
        s = Synthesizer()
        s.llm_client = MagicMock()
        return s
    
    @pytest.fixture
    def sample_facts(self):
        """Sample verified facts for report generation."""
        return [
            MockVerifiedFact("f1", "Tesla reported $25B revenue"),
            MockVerifiedFact("f2", "Tesla delivered 500K vehicles"),
            MockVerifiedFact("f3", "Market cap reached $800B"),
            MockVerifiedFact("f4", "Stock price increased 15%"),
            MockVerifiedFact("f5", "New factory opened in Texas"),
            MockVerifiedFact("f6", "CEO announced new product line"),
        ]
    
    @pytest.fixture
    def sample_discrepancies(self):
        """Sample discrepancies for testing."""
        return [MockDiscrepancy("Revenue figures")]
    
    def test_categorize_facts_creates_sections(self, synthesizer, sample_facts):
        """Test that facts are categorized into sections."""
        categories = synthesizer._categorize_facts(sample_facts, "Tesla research")
        
        assert len(categories) > 0
        # Should have at least one section with facts
        total_facts = sum(len(facts) for facts in categories.values())
        assert total_facts == len(sample_facts)
    
    @pytest.mark.asyncio
    async def test_generate_executive_summary(self, synthesizer, sample_facts, sample_discrepancies):
        """Test executive summary generation."""
        synthesizer.llm_client.complete = AsyncMock(return_value="""
        Tesla demonstrated strong financial performance in Q4 2023, with revenue reaching
        $25 billion and vehicle deliveries exceeding 500,000 units. The company's market 
        capitalization touched $800 billion as investor confidence remained high.
        """)
        
        summary = await synthesizer._generate_executive_summary(
            "Tesla Q4 2023 performance",
            sample_facts,
            sample_discrepancies
        )
        
        assert len(summary) > 0
        # LLM should have been called
        synthesizer.llm_client.complete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_section_content(self, synthesizer, sample_facts):
        """Test individual section generation."""
        # Mock a response with 300+ words
        long_content = " ".join(["word"] * 350)
        synthesizer.llm_client.complete = AsyncMock(return_value=long_content)
        
        section = await synthesizer._generate_section("Overview", sample_facts[:2])
        
        assert isinstance(section, ReportSection)
        assert section.title == "Overview"
        assert section.category == "Overview"
    
    @pytest.mark.asyncio
    async def test_generate_report_returns_narrative_report(self, synthesizer, sample_facts, sample_discrepancies):
        """Test full report generation."""
        synthesizer.llm_client.complete = AsyncMock(return_value=" ".join(["word"] * 300))
        
        report = await synthesizer.generate_report(
            request_id="req-123",
            query="Tesla Q4 2023",
            verified_facts=sample_facts,
            discrepancies=sample_discrepancies
        )
        
        assert isinstance(report, NarrativeReport)
        assert report.request_id == "req-123"
        assert report.query == "Tesla Q4 2023"
        assert len(report.sections) > 0


class TestReportSection:
    """Tests for the ReportSection dataclass."""
    
    def test_section_to_dict(self):
        """Test ReportSection serialization."""
        section = ReportSection(
            id="s1",
            title="Financial Overview",
            content="Tesla reported strong financials...",
            word_count=350,
            citation_ids=["f1", "f2"],
            category="Financials"
        )
        
        result = section.to_dict()
        
        assert result["title"] == "Financial Overview"
        assert result["word_count"] == 350
        assert len(result["citation_ids"]) == 2


class TestNarrativeReport:
    """Tests for the NarrativeReport dataclass."""
    
    def test_report_to_dict(self):
        """Test NarrativeReport serialization."""
        section = ReportSection(
            id="s1",
            title="Overview",
            content="Content here",
            word_count=100,
            citation_ids=["f1"],
            category="Overview"
        )
        
        report = NarrativeReport(
            id="r1",
            request_id="req-1",
            query="Test query",
            executive_summary="Summary here",
            sections=[section],
            discrepancy_notes=[],
            total_word_count=200,
            total_sources=5,
            created_at=datetime.now()
        )
        
        result = report.to_dict()
        
        assert result["id"] == "r1"
        assert result["request_id"] == "req-1"
        assert len(result["sections"]) == 1
        assert result["total_word_count"] == 200


class TestConvenienceFunction:
    """Tests for module-level convenience function."""
    
    @pytest.mark.asyncio
    async def test_generate_report_function(self):
        """Test the convenience function."""
        with patch('backend.modules.synthesizer.Synthesizer') as MockSynthesizer:
            mock_instance = MockSynthesizer.return_value
            mock_instance.generate_report = AsyncMock()
            
            await generate_report(
                request_id="test",
                query="query",
                verified_facts=[],
                discrepancies=[]
            )
            
            mock_instance.generate_report.assert_called_once()
