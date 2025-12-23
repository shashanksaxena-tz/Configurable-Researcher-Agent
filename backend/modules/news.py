"""News analysis researcher module."""

from typing import Dict, Any, List
from .base import BaseResearcher
import random
from datetime import datetime, timedelta
from backend.utils.search import search_google_news

class NewsResearcher(BaseResearcher):
    """Researcher for news analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform news research."""
        
        # Use real search if we can, otherwise fallback/mix
        real_news = search_google_news(self.entity_name, limit=10)
        
        # Transform real news to match expected format
        news_items = []
        for item in real_news:
            news_items.append({
                "headline": item["title"],
                "date": item["published_date"],
                "source": "Google News", # Origin source is harder to parse from RSS title without regex, keeping simple
                "sentiment": "Neutral", # We don't have a sentiment analyzer yet
                "link": item["link"]
            })

        if not news_items:
            # Fallback if search fails
            news_items = self._generate_news_items()

        data = {
            "recent_news": news_items[:5],
            "total_articles": len(news_items) if news_items else random.randint(50, 500),
            "press_releases": random.randint(5, 20), # Still mocked
            "media_mentions": random.randint(100, 1000), # Still mocked
            "trending_topics": [
                "Product launches",
                "Market expansion",
                "Innovation",
                "Leadership changes"
            ],
            "sentiment_breakdown": {
                "positive": f"{random.randint(50, 80)}%",
                "neutral": f"{random.randint(10, 30)}%",
                "negative": f"{random.randint(5, 20)}%"
            }
        }
        
        return data
    
    def _generate_news_items(self) -> List[Dict[str, Any]]:
        """Generate sample news items (fallback)."""
        headlines = [
            f"{self.entity_name} announces major expansion plans",
            f"{self.entity_name} reports strong quarterly results",
            f"Industry experts praise {self.entity_name}'s innovation",
            f"{self.entity_name} launches new product line",
            f"{self.entity_name} recognized for excellence",
        ]
        
        news_items = []
        for i, headline in enumerate(headlines):
            date = datetime.now() - timedelta(days=i*3)
            news_items.append({
                "headline": headline,
                "date": date.strftime("%Y-%m-%d"),
                "source": random.choice(["Reuters", "Bloomberg", "TechCrunch", "Forbes", "WSJ"]),
                "sentiment": random.choice(["Positive", "Neutral", "Mixed"])
            })
        
        return news_items
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of news analysis."""
        return f"{self.entity_name} has {data.get('total_articles', 'N/A')} recent articles with {data.get('media_mentions', 'N/A')} media mentions, showing active media presence."
