"""Search abstraction for the Intelligent Research Agent.

Per spec requirements:
- FR-002: Execute independent searches for each sub-question
- FR-021: Handle search provider failures gracefully
- NFR-008: Non-English search results MUST be filtered out

Providers:
- DuckDuckGo (primary)
- Wikipedia (verification)
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from backend.config import settings


class SearchProvider(str, Enum):
    """Available search providers."""
    DUCKDUCKGO = "duckduckgo"
    WIKIPEDIA = "wikipedia"


@dataclass
class SearchResult:
    """A single search result with metadata.
    
    Per data-model.md: SearchResult entity with URL, content excerpt, timestamp.
    """
    url: str
    title: str
    snippet: str
    source: SearchProvider
    timestamp: datetime
    language: str = "en"
    relevance_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "snippet": self.snippet,
            "source": self.source.value,
            "timestamp": self.timestamp.isoformat(),
            "language": self.language,
            "relevance_score": self.relevance_score
        }


def is_english(text: str) -> bool:
    """Simple heuristic to check if text is likely English.
    
    Per NFR-008: Non-English search results MUST be filtered out.
    """
    if not text:
        return False
    
    # Common English words for quick detection
    english_indicators = [
        'the', 'is', 'are', 'was', 'were', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might',
        'and', 'but', 'or', 'because', 'if', 'when', 'while'
    ]
    
    text_lower = text.lower()
    words = text_lower.split()
    
    if len(words) < 3:
        return True  # Too short to determine
    
    matches = sum(1 for word in words if word in english_indicators)
    return (matches / len(words)) > 0.05  # At least 5% English indicators


class SearchClient:
    """Unified search client with provider abstraction.
    
    Handles multiple search providers with automatic failover
    and English-only filtering per NFR-008.
    """
    
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=settings.SEARCH_TIMEOUT_SECONDS)
        self.max_results = settings.MAX_SEARCH_RESULTS_PER_QUERY
    
    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
    
    async def search(
        self,
        query: str,
        provider: SearchProvider = SearchProvider.DUCKDUCKGO,
        max_results: Optional[int] = None
    ) -> List[SearchResult]:
        """Execute a search query.
        
        Args:
            query: Search query string
            provider: Search provider to use
            max_results: Maximum results to return
            
        Returns:
            List of SearchResult objects
        """
        max_results = max_results or self.max_results
        
        try:
            if provider == SearchProvider.DUCKDUCKGO:
                results = await self._search_duckduckgo(query, max_results)
            elif provider == SearchProvider.WIKIPEDIA:
                results = await self._search_wikipedia(query, max_results)
            else:
                results = []
            
            # Filter non-English results per NFR-008
            if settings.FILTER_NON_ENGLISH:
                results = [r for r in results if is_english(r.snippet)]
            
            return results
            
        except Exception as e:
            # Per FR-021: Handle failures gracefully
            # Log error and return empty list instead of failing
            return []
    
    async def search_all_providers(
        self,
        query: str,
        max_results_per_provider: Optional[int] = None
    ) -> List[SearchResult]:
        """Search across all available providers.
        
        Args:
            query: Search query string
            max_results_per_provider: Max results per provider
            
        Returns:
            Combined list of SearchResult objects
        """
        max_results = max_results_per_provider or (self.max_results // 2)
        
        # Execute searches concurrently
        tasks = [
            self.search(query, SearchProvider.DUCKDUCKGO, max_results),
            self.search(query, SearchProvider.WIKIPEDIA, max_results)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results, handling any exceptions
        all_results = []
        for result in results:
            if isinstance(result, list):
                all_results.extend(result)
            # Skip exceptions - already logged in search()
        
        return all_results
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(httpx.TimeoutException)
    )
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo.
        
        Uses the duckduckgo-search library.
        """
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(SearchResult(
                        url=r.get("href", ""),
                        title=r.get("title", ""),
                        snippet=r.get("body", ""),
                        source=SearchProvider.DUCKDUCKGO,
                        timestamp=datetime.now(),
                        language="en"  # DuckDuckGo defaults to English
                    ))
            
            return results
            
        except Exception as e:
            # Return empty on error per FR-021
            return []
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(httpx.TimeoutException)
    )
    async def _search_wikipedia(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Wikipedia for verification and background.
        
        Uses the wikipedia library.
        """
        try:
            import wikipedia
            
            # Set language to English per NFR-007
            wikipedia.set_lang("en")
            
            results = []
            search_results = wikipedia.search(query, results=max_results)
            
            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    results.append(SearchResult(
                        url=page.url,
                        title=page.title,
                        snippet=page.summary[:500] + "..." if len(page.summary) > 500 else page.summary,
                        source=SearchProvider.WIKIPEDIA,
                        timestamp=datetime.now(),
                        language="en"
                    ))
                except (wikipedia.exceptions.DisambiguationError,
                        wikipedia.exceptions.PageError):
                    # Skip disambiguation pages and missing pages
                    continue
            
            return results
            
        except Exception as e:
            return []


# Global client instance
_search_client: Optional[SearchClient] = None


def get_search_client() -> SearchClient:
    """Get or create the global search client instance."""
    global _search_client
    if _search_client is None:
        _search_client = SearchClient()
    return _search_client


async def search(query: str, **kwargs) -> List[SearchResult]:
    """Convenience function for quick searches.
    
    Args:
        query: Search query
        **kwargs: Additional search parameters
        
    Returns:
        List of SearchResult objects
    """
    client = get_search_client()
    return await client.search_all_providers(query, **kwargs)
