from typing import List, Dict, Any
from duckduckgo_search import DDGS
from .base import BaseSearchProvider

class GitHubProvider(BaseSearchProvider):
    """Search provider using GitHub via DuckDuckGo."""

    @property
    def name(self) -> str:
        return "GitHub"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            with DDGS() as ddgs:
                search_query = f"site:github.com {query}"
                search_results = list(ddgs.text(search_query, max_results=limit))

                for item in search_results:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("href", ""),
                        "published_date": "",
                        "source": "GitHub",
                        "snippet": item.get("body", "")
                    })
        except Exception as e:
            print(f"Error searching GitHub: {e}")

        return results
