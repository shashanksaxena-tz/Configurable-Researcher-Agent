"""Sentiment analysis researcher module."""

from typing import Dict, Any
from .base import BaseResearcher

class SentimentResearcher(BaseResearcher):
    """Researcher for sentiment analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform sentiment research."""
        
        schema = {
            "positive_sentiment": "string (e.g. 60%)",
            "negative_sentiment": "string",
            "neutral_sentiment": "string",
            "overall_score": "float (0-10)",
            "sentiment_trend": "string (Improving/Stable/Declining)",
            "key_topics": ["string"],
            "sources_analyzed": "integer (estimated)",
        }
        
        # We rely on the BaseResearcher to generate the narrative summary now.
        return await self.perform_ai_research("reviews sentiment opinions public perception", schema)
    
    # Removed the override for generate_summary to use the BaseResearcher's narrative logic.
