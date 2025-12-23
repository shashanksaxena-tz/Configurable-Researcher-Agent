"""Personality analysis researcher module."""

from typing import Dict, Any
from .base import BaseResearcher

class PersonalityResearcher(BaseResearcher):
    """Researcher for personality analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform personality research."""
        
        schema = {
            "traits": ["string"],
            "leadership_style": "string",
            "communication_style": "string",
            "public_perception": "string",
            "strengths": ["string"],
            "work_style": "string"
        }
        
        return await self.perform_ai_research("personality leadership style traits interviews", schema)
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of personality analysis."""
        traits = data.get('traits', [])
        traits_str = ", ".join(traits[:3]) if traits else "N/A"
        return f"{self.entity_name} exhibits {traits_str} characteristics with a {data.get('leadership_style', 'N/A')} leadership approach."
