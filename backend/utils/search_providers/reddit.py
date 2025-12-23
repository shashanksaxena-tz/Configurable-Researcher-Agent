from typing import List, Dict, Any
from duckduckgo_search import DDGS
from .base import BaseSearchProvider

class RedditProvider(BaseSearchProvider):
    """Search provider using Reddit via DuckDuckGo."""

    @property
    def name(self) -> str:
        return "Reddit"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            with DDGS() as ddgs:
                search_query = f"site:reddit.com {query}"
                search_results = list(ddgs.text(search_query, max_results=limit))

                for item in search_results:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("href", ""),
                        "published_date": "",
                        "source": "Reddit",
                        "snippet": item.get("body", "")
                    })
        except Exception as e:
            print(f"Error searching Reddit: {e}")

        return results
