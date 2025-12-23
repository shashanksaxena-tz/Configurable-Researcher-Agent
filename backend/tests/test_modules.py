import pytest
from backend.modules.financial import FinancialResearcher

@pytest.mark.asyncio
async def test_financial_researcher_mock():
    researcher = FinancialResearcher("Tesla", "company")
    data = await researcher.research()

    assert data is not None
    assert "revenue" in data
    # Check that mock data generation works as expected (it's random, but keys should exist)
    assert isinstance(data["market_cap"], str)
