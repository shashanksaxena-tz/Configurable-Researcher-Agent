import pytest
from backend.modules.financial import FinancialResearcher
from backend.modules.news import NewsResearcher
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_financial_researcher_structure():
    """Test that financial researcher returns the expected structure even if empty."""
    # We patch the LLM service to return a dummy response so we don't hit the API
    with patch("backend.modules.base.llm_service.generate_json") as mock_llm:
        mock_llm.return_value = {
            "revenue": "$100B",
            "market_cap": "$500B",
            "stock_price": "$200",
            "pe_ratio": 50.5,
            "debt": "$10B",
            "profitability": "High",
            "growth_rate": "20%",
            "earnings": "$5B"
        }

        researcher = FinancialResearcher("Tesla", "company")
        data = await researcher.research()

        assert data is not None
        assert "revenue" in data
        assert data["revenue"] == "$100B"

@pytest.mark.asyncio
async def test_news_researcher_structure():
    with patch("backend.modules.news.get_search_results") as mock_search:
        mock_search.return_value = [
            {"title": "Test News 1", "source": "Source A", "link": "http://a.com"},
            {"title": "Test News 2", "source": "Source B", "link": "http://b.com"}
        ]

        with patch("backend.modules.news.llm_service.generate_json") as mock_llm:
            mock_llm.return_value = {
                "press_releases": 5,
                "media_mentions": 100,
                "trending_topics": ["EV", "Tech"],
                "sentiment_breakdown": {"positive": "80%", "neutral": "10%", "negative": "10%"}
            }

            researcher = NewsResearcher("Tesla", "company")
            data = await researcher.research()

            assert data["total_articles"] == 2
            assert data["press_releases"] == 5
