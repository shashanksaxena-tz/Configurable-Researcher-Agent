"""Configuration settings for the Configurable Researcher Agent."""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Dict, List, Union
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
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:3001", "http://127.0.0.1:3001"]
    
    # Research Settings
    MAX_SEARCH_RESULTS: int = 10
    TIMEOUT_SECONDS: int = 30
    
    # Report Settings
    REPORTS_DIR: str = "./reports"
    
    # Search Configuration
    SEARCH_PROVIDERS: Union[List[str], str] = ["google_news", "wikipedia", "linkedin"]
    
    # Validators for parsing comma-separated strings from .env
    @field_validator('CORS_ORIGINS', 'SEARCH_PROVIDERS', mode='before')
    @classmethod
    def parse_list(cls, v):
        if isinstance(v, str):
            # Handle comma-separated string
            return [s.strip() for s in v.split(',') if s.strip()]
        return v
    
    # ===== AGENTIC WORKFLOW CONFIGURATION =====
    # Per spec: Plan-Execute-Verify-Synthesize model
    
    # LLM Configuration (multi-model approach per research.md)
    LLM_PROVIDER: str = "openai"  # openai, google, or both
    OPENAI_API_KEY: Union[str, None] = None
    GOOGLE_API_KEY: Union[str, None] = None
    
    PLANNING_MODEL: str = "gpt-4"  # Complex reasoning for query deconstruction
    EXTRACTION_MODEL: str = "gpt-3.5-turbo"  # Fast model for information extraction
    VERIFICATION_MODEL: str = "gpt-4"  # Complex reasoning for cross-referencing
    SYNTHESIS_MODEL: str = "gpt-4"  # Complex reasoning for narrative generation
    
    # Research Depth Settings (per FR-001, FR-004)
    # quick: 3-5 sub-questions, 1 level recursion
    # standard: 5-7 sub-questions, 2 levels recursion
    # comprehensive: 7-10 sub-questions, 3 levels recursion
    DEFAULT_DEPTH_LEVEL: str = "standard"
    MIN_SUB_QUESTIONS: int = 3
    MAX_SUB_QUESTIONS: int = 10
    MAX_RECURSION_DEPTH: int = 2  # Default for standard mode (per FR-004: 2-3 levels)
    
    # Performance Targets (per Success Criteria)
    MAX_RESEARCH_TIME_SECONDS: int = 180  # SC-010: Under 3 minutes
    MAX_RENDER_TIME_SECONDS: int = 2  # SC-011: Under 2 seconds
    MAX_CITATION_LOOKUP_MS: int = 1000  # SC-006: Within 1 second
    
    # Quality Thresholds (per FR-007, FR-019)
    MIN_WORDS_PER_SECTION: int = 300  # FR-007: Minimum 300 words per major section
    MIN_SOURCES_PER_SECTION: int = 3  # SC-004: At least 3 sources per section
    
    # Rate Limiting (LLM and Search providers)
    LLM_RATE_LIMIT_RPM: int = 60  # Requests per minute
    MAX_CONCURRENT_SEARCHES: int = 3  # Balance speed vs rate limits
    SEARCH_TIMEOUT_SECONDS: int = 30  # Per search request
    MAX_SEARCH_RESULTS_PER_QUERY: int = 5  # Results to process per sub-question
    
    # Logging (per NFR-003 to NFR-006)
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = True
    LOG_FILE_PATH: str = "./logs/research.log"
    
    # Language Settings (per NFR-007, NFR-008)
    TARGET_LANGUAGE: str = "en"  # English only for MVP
    FILTER_NON_ENGLISH: bool = True

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
