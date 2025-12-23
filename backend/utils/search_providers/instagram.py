from typing import List, Dict, Any
from duckduckgo_search import DDGS
from .base import BaseSearchProvider

class InstagramProvider(BaseSearchProvider):
    """Search provider using Instagram via DuckDuckGo."""

    @property
    def name(self) -> str:
        return "Instagram"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            with DDGS() as ddgs:
                search_query = f"site:instagram.com {query}"
                search_results = list(ddgs.text(search_query, max_results=limit))

                for item in search_results:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("href", ""),
                        "published_date": "",
                        "source": "Instagram",
                        "snippet": item.get("body", "")
                    })
        except Exception as e:
            print(f"Error searching Instagram: {e}")

        return results
