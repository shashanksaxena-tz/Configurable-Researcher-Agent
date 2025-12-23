from typing import List, Dict, Any
from duckduckgo_search import DDGS
from .base import BaseSearchProvider

class DuckDuckGoProvider(BaseSearchProvider):
    """Search provider using DuckDuckGo."""

    @property
    def name(self) -> str:
        return "DuckDuckGo"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            with DDGS() as ddgs:
                # Use 'text' search for general web results
                search_results = list(ddgs.text(query, max_results=limit))

                for item in search_results:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("href", ""),
                        "published_date": "", # DDG text search often doesn't give date
                        "source": "DuckDuckGo",
                        "snippet": item.get("body", "")
                    })
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")

        return results
