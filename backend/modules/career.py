"""Career analysis researcher module."""

from typing import Dict, Any
from .base import BaseResearcher

class CareerResearcher(BaseResearcher):
    """Researcher for career analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform career research."""
        
        if self.entity_type == "company":
            schema = {
                "company_age": "string (e.g., '15 years')",
                "founding_year": "integer",
                "key_milestones": ["string"],
                "growth_stages": "string (e.g., 'Rapid Expansion')",
                "employee_count": "string (e.g., '1000+')",
            }
            return await self.perform_ai_research("history founding employees milestones", schema)
        else:
            schema = {
                "work_history": [
                    {
                        "company": "string",
                        "position": "string",
                        "years": "string"
                    }
                ],
                "achievements": ["string"],
                "education": [
                    {
                        "degree": "string",
                        "institution": "string",
                        "field": "string"
                    }
                ],
                "skills": ["string"],
                "certifications": "integer",
            }
            return await self.perform_ai_research("career history education resume", schema)
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of career analysis."""
        if self.entity_type == "company":
            return f"{self.entity_name} has been operating for {data.get('company_age', 'N/A')} with {data.get('employee_count', 'N/A')} employees."
        else:
            return f"{self.entity_name} has diverse professional experience with notable achievements in the industry."
