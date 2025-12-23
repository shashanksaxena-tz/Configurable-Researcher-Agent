"""Hobbies and interests researcher module."""

from typing import Dict, Any
from .base import BaseResearcher

class HobbiesResearcher(BaseResearcher):
    """Researcher for hobbies and interests."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform hobbies research."""
        
        schema = {
            "hobbies": ["string"],
            "interests": ["string"],
            "activities": ["string"],
            "passions": ["string"],
            "lifestyle": "string"
        }
        
        return await self.perform_ai_research("hobbies interests personal life activities", schema)
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of hobbies analysis."""
        hobbies = data.get('hobbies', [])
        hobbies_str = ", ".join(hobbies[:3]) if hobbies else "N/A"
        passions = data.get('passions', [])
        passions_str = ", ".join(passions[:2]) if passions else "N/A"
        return f"{self.entity_name} enjoys {hobbies_str} and is passionate about {passions_str}."
