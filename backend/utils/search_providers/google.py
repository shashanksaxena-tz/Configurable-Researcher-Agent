import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseSearchProvider

class GoogleNewsProvider(BaseSearchProvider):
    """Search provider using Google News RSS."""

    @property
    def name(self) -> str:
        return "Google News"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Use the RSS feed for Google News
        rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"

        try:
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item", limit=limit)

            results = []
            for item in items:
                title = item.title.text if item.title else "No Title"
                link = item.link.text if item.link else "#"
                pub_date = item.pubDate.text if item.pubDate else ""

                results.append({
                    "title": title,
                    "link": link,
                    "published_date": pub_date,
                    "source": "Google News"
                })

            return results
        except Exception as e:
            print(f"Error searching Google News: {e}")
            return []
