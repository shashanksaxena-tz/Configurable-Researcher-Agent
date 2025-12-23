"""News analysis researcher module."""

from typing import Dict, Any, List
from .base import BaseResearcher
from backend.utils.search import get_search_results
from backend.utils.llm import llm_service

class NewsResearcher(BaseResearcher):
    """Researcher for news analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform news research."""
        
        # 1. Get real news
        # We prefer google_news for this specific module
        news_results = get_search_results(self.entity_name, limit=10, providers=["google_news"])
        
        # Transform basic news items
        news_items = []
        for item in news_results:
            news_items.append({
                "headline": item.get("title"),
                "date": item.get("published_date", ""),
                "source": item.get("source", "Unknown"),
                "link": item.get("link")
            })

        # 2. Use AI to analyze the news content for aggregate metrics
        # (sentiment, topics, press releases count estimation)
        context = ""
        for item in news_results:
            context += f"Headline: {item.get('title')}\nSource: {item.get('source')}\n\n"

        if not context:
            context = "No news found."

        schema = {
            "press_releases": "integer (estimate count)",
            "media_mentions": "integer (estimate count)",
            "trending_topics": ["string"],
            "sentiment_breakdown": {
                "positive": "string (percentage)",
                "neutral": "string (percentage)",
                "negative": "string (percentage)"
            }
        }
        
        ai_data = await llm_service.generate_json(
            f"Analyze the news headlines for {self.entity_name} to estimate sentiment and identify topics.",
            context,
            schema
        )
        
        # Merge data
        data = {
            "recent_news": news_items,
            "total_articles": len(news_items),
            "press_releases": ai_data.get("press_releases", 0),
            "media_mentions": ai_data.get("media_mentions", 0),
            "trending_topics": ai_data.get("trending_topics", []),
            "sentiment_breakdown": ai_data.get("sentiment_breakdown", {
                "positive": "0%", "neutral": "0%", "negative": "0%"
            })
        }
        
        return data
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of news analysis."""
        return f"{self.entity_name} has {data.get('total_articles', 0)} recent articles analyzed."
