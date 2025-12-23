"""Search factory and utility."""
from typing import List, Dict, Any, Type
from config import settings
from .search_providers.base import BaseSearchProvider
from .search_providers.google import GoogleNewsProvider
from .search_providers.linkedin import LinkedInProvider
from .search_providers.wikipedia import WikipediaProvider
from .search_providers.ddg import DuckDuckGoProvider
from .search_providers.reddit import RedditProvider
from .search_providers.github import GitHubProvider
from .search_providers.instagram import InstagramProvider
from .search_providers.youtube import YouTubeProvider
from .search_providers.medium import MediumProvider

# Registry of available providers
PROVIDER_MAP: Dict[str, Type[BaseSearchProvider]] = {
    "google_news": GoogleNewsProvider,
    "linkedin": LinkedInProvider,
    "wikipedia": WikipediaProvider,
    "duckduckgo": DuckDuckGoProvider,
    "reddit": RedditProvider,
    "github": GitHubProvider,
    "instagram": InstagramProvider,
    "youtube": YouTubeProvider,
    "medium": MediumProvider
}

def get_search_results(query: str, limit: int = 5, providers: List[str] = None) -> List[Dict[str, Any]]:
    """
    Perform search across multiple configured providers.

    Args:
        query: The search term.
        limit: Max results per provider.
        providers: List of provider names to use. If None, uses defaults from settings.

    Returns:
        Combined list of results.
    """
    if providers is None:
        providers = settings.SEARCH_PROVIDERS

    all_results = []

    for provider_name in providers:
        if provider_name in PROVIDER_MAP:
            try:
                provider_class = PROVIDER_MAP[provider_name]
                provider_instance = provider_class()
                # print(f"Searching {provider_name} for '{query}'...")
                results = provider_instance.search(query, limit=limit)
                all_results.extend(results)
            except Exception as e:
                print(f"Failed to search {provider_name}: {e}")

    return all_results
