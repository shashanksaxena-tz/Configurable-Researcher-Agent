"""Hobbies and interests researcher module."""

from typing import Dict, Any
from .base import BaseResearcher
import random


class HobbiesResearcher(BaseResearcher):
    """Researcher for hobbies and interests."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform hobbies research."""
        # In a real implementation, this would gather from social media, interviews, etc.
        
        hobbies_list = random.sample([
            "Travel", "Photography", "Reading", "Sports", "Music",
            "Art", "Cooking", "Technology", "Gaming", "Fitness",
            "Golf", "Skiing", "Sailing", "Collecting"
        ], 5)
        
        interests_list = random.sample([
            "Innovation", "Sustainability", "Education", "Philanthropy",
            "Space exploration", "AI and technology", "Climate change",
            "Healthcare", "Arts and culture", "Science"
        ], 4)
        
        data = {
            "hobbies": hobbies_list,
            "interests": interests_list,
            "activities": random.sample([
                "Public speaking",
                "Mentoring",
                "Volunteering",
                "Board games",
                "Outdoor activities"
            ], 3),
            "passions": random.sample([
                "Innovation and technology",
                "Social impact",
                "Environmental conservation",
                "Education reform",
                "Healthcare advancement"
            ], 2),
            "lifestyle": random.choice([
                "Active and adventurous",
                "Intellectual and curious",
                "Balanced and mindful"
            ])
        }
        
        return data
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of hobbies analysis."""
        hobbies_str = ", ".join(data.get('hobbies', [])[:3])
        return f"{self.entity_name} enjoys {hobbies_str} and is passionate about {', '.join(data.get('passions', [])[:2])}."
