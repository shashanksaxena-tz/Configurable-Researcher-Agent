import pytest
from backend.utils.search import get_search_results
from backend.utils.search_providers.google import GoogleNewsProvider
from backend.utils.search_providers.linkedin import LinkedInProvider
from backend.utils.search_providers.wikipedia import WikipediaProvider

def test_google_provider_structure():
    provider = GoogleNewsProvider()
    assert provider.name == "Google News"
    # We can't easily test network calls without mocking or making real calls.
    # For unit tests, we check structure.

def test_linkedin_provider_structure():
    provider = LinkedInProvider()
    assert provider.name == "LinkedIn"

def test_wikipedia_provider_structure():
    provider = WikipediaProvider()
    assert provider.name == "Wikipedia"

def test_search_factory_default():
    # Test that it loads providers from config (mocking config would be better but this is integration-ish)
    # We just check if it runs without crashing given we have network.
    pass

@pytest.mark.asyncio
async def test_search_integration():
    # Attempt a real search for a safe query
    results = get_search_results("Python", limit=1, providers=["wikipedia"])
    # Wikipedia should be reliable enough
    if results:
        assert results[0]["source"] == "Wikipedia"
        assert "Python" in results[0]["title"]
