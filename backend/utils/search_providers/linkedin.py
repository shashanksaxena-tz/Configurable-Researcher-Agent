import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseSearchProvider

class LinkedInProvider(BaseSearchProvider):
    """Search provider for LinkedIn via Google Search Proxy."""

    @property
    def name(self) -> str:
        return "LinkedIn"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # We use a DuckDuckGo HTML search proxy or similar to find LinkedIn profiles
        # Note: Scraping Google/DDG results directly can be fragile.
        # This is a best-effort implementation without an API key.

        search_query = f"site:linkedin.com/in/ OR site:linkedin.com/company/ {query}"
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            # DDG 403s often on cloud IPs, but let's try.
            # If it fails, we return empty list (graceful degradation).
            if response.status_code != 200:
                print(f"LinkedIn Proxy Search failed: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, "html.parser")
            results = []

            # DDG HTML structure selectors
            links = soup.find_all("a", class_="result__a", limit=limit)

            for link in links:
                title = link.text
                url = link['href']

                results.append({
                    "title": title,
                    "link": url,
                    "published_date": "",
                    "source": "LinkedIn"
                })

            return results
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
            return []
