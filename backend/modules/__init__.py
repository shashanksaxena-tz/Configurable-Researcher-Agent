"""Module manager for the researcher."""

from typing import Dict, Any, List
from modules.base import BaseResearcher
from typing import Dict, Any
from config import RESEARCH_MODULES
from models import ResearchResult
from datetime import datetime


class ResearcherManager:
    """Manager for all research modules."""
    
    MODULE_MAP = {}
    
    def __init__(self, entity_name: str, entity_type: str):
        self.entity_name = entity_name
        self.entity_type = entity_type
        
        # Lazy import to avoid circular dependencies
        if not self.MODULE_MAP:
            from modules.financial import FinancialResearcher
            from modules.sentiment import SentimentResearcher
            from modules.news import NewsResearcher
            from modules.personality import PersonalityResearcher
            from modules.hobbies import HobbiesResearcher
            from modules.career import CareerResearcher
            from modules.social_media import SocialMediaResearcher
            from modules.market_analysis import MarketAnalysisResearcher
            from modules.competitor import CompetitorResearcher
            from modules.trends import TrendsResearcher
            
            ResearcherManager.MODULE_MAP = {
                "financial": FinancialResearcher,
                "sentiment": SentimentResearcher,
                "news": NewsResearcher,
                "personality": PersonalityResearcher,
                "hobbies": HobbiesResearcher,
                "career": CareerResearcher,
                "social_media": SocialMediaResearcher,
                "market_analysis": MarketAnalysisResearcher,
                "competitor": CompetitorResearcher,
                "trends": TrendsResearcher,
            }
    
    async def perform_research(self, research_types: List[str], selected_providers: List[str] = None) -> List[ResearchResult]:
        """Perform research for the specified types."""
        results = []
        
        for research_type in research_types:
            if research_type not in self.MODULE_MAP:
                continue
            
            researcher_class = self.MODULE_MAP[research_type]
            researcher = researcher_class(self.entity_name, self.entity_type)
            
            if selected_providers:
                # If specific providers are selected, we can pass them to the researcher
                # However, BaseResearcher.research() signature might not accept it directly
                # We should update BaseResearcher to store it or pass it.
                # For now, let's inject it into the researcher instance if it supports it.
                researcher.selected_providers = selected_providers

            data = await researcher.research()
            summary = researcher.generate_summary(data)
            confidence = researcher.calculate_confidence(data)
            
            module_info = RESEARCH_MODULES.get(research_type, {})
            
            result = ResearchResult(
                research_type=research_type,
                title=module_info.get("name", research_type.title()),
                data=data,
                summary=summary,
                confidence=confidence,
                timestamp=datetime.now()
            )
            
            results.append(result)
        
        return results
    
    @staticmethod
    def get_available_modules() -> Dict[str, Any]:
        """Get information about all available research modules."""
        return RESEARCH_MODULES
