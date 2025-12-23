"""Configuration settings for the Configurable Researcher Agent."""

from pydantic_settings import BaseSettings
from typing import Dict, List
from enum import Enum


class ResearchType(str, Enum):
    """Available research types."""
    FINANCIAL = "financial"
    SENTIMENT = "sentiment"
    NEWS = "news"
    PERSONALITY = "personality"
    HOBBIES = "hobbies"
    CAREER = "career"
    SOCIAL_MEDIA = "social_media"
    MARKET_ANALYSIS = "market_analysis"
    COMPETITOR = "competitor"
    TRENDS = "trends"


class Settings(BaseSettings):
    """Application settings."""
    
    APP_NAME: str = "Configurable Researcher Agent"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Research Settings
    MAX_SEARCH_RESULTS: int = 10
    TIMEOUT_SECONDS: int = 30
    
    # Report Settings
    REPORTS_DIR: str = "./reports"
    
    # Search Configuration
    SEARCH_PROVIDERS: List[str] = ["google_news", "wikipedia", "linkedin"]

    class Config:
        env_file = ".env"


settings = Settings()


# Research Module Configuration
RESEARCH_MODULES: Dict[str, Dict] = {
    "financial": {
        "name": "Financial Analysis",
        "description": "Analyze financial data, stock performance, revenue, and market cap",
        "fields": ["revenue", "market_cap", "stock_price", "pe_ratio", "debt", "profitability"],
        "icon": "💰",
        "color": "#10b981"
    },
    "sentiment": {
        "name": "Sentiment Analysis",
        "description": "Analyze public sentiment, reviews, and opinions",
        "fields": ["positive_sentiment", "negative_sentiment", "neutral_sentiment", "overall_score"],
        "icon": "😊",
        "color": "#3b82f6"
    },
    "news": {
        "name": "News Analysis",
        "description": "Recent news, press releases, and media coverage",
        "fields": ["recent_news", "press_releases", "media_mentions", "trending_topics"],
        "icon": "📰",
        "color": "#f59e0b"
    },
    "personality": {
        "name": "Personality Analysis",
        "description": "Analyze personality traits, leadership style, and public image",
        "fields": ["traits", "leadership_style", "communication_style", "public_perception"],
        "icon": "🧠",
        "color": "#8b5cf6"
    },
    "hobbies": {
        "name": "Hobbies & Interests",
        "description": "Personal interests, hobbies, and activities",
        "fields": ["hobbies", "interests", "activities", "passions"],
        "icon": "🎨",
        "color": "#ec4899"
    },
    "career": {
        "name": "Career Analysis",
        "description": "Professional background, achievements, and career trajectory",
        "fields": ["work_history", "achievements", "education", "skills"],
        "icon": "💼",
        "color": "#06b6d4"
    },
    "social_media": {
        "name": "Social Media Presence",
        "description": "Social media activity, following, and engagement",
        "fields": ["platforms", "followers", "engagement", "content_themes"],
        "icon": "📱",
        "color": "#f97316"
    },
    "market_analysis": {
        "name": "Market Analysis",
        "description": "Market position, competition, and industry trends",
        "fields": ["market_share", "competitors", "industry_position", "growth_rate"],
        "icon": "📊",
        "color": "#14b8a6"
    },
    "competitor": {
        "name": "Competitor Analysis",
        "description": "Competitive landscape and market positioning",
        "fields": ["main_competitors", "competitive_advantages", "market_positioning"],
        "icon": "⚔️",
        "color": "#ef4444"
    },
    "trends": {
        "name": "Trends Analysis",
        "description": "Emerging trends and future predictions",
        "fields": ["emerging_trends", "predictions", "innovations", "future_outlook"],
        "icon": "📈",
        "color": "#84cc16"
    }
}
