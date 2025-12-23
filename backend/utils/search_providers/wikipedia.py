import wikipedia
from typing import List, Dict, Any
from .base import BaseSearchProvider

class WikipediaProvider(BaseSearchProvider):
    """Search provider using Wikipedia API."""

    @property
    def name(self) -> str:
        return "Wikipedia"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            # Search for page titles
            titles = wikipedia.search(query, results=limit)

            results = []
            for title in titles:
                try:
                    # Get summary (limiting chars to avoid huge payload)
                    summary = wikipedia.summary(title, sentences=2)
                    url = wikipedia.page(title).url

                    results.append({
                        "title": f"Wikipedia: {title}",
                        "link": url,
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": summary
                    })
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue

            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
