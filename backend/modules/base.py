"""Base researcher module."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random


class BaseResearcher(ABC):
    """Base class for all researcher modules."""
    
    def __init__(self, entity_name: str, entity_type: str, search_provider: Optional[Any] = None):
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.search_provider = search_provider
    
    @abstractmethod
    async def research(self) -> Dict[str, Any]:
        """Perform research and return results."""
        pass
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary from the research data."""
        return f"Analysis completed for {self.entity_name}"
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for the research."""
        # In a real implementation, this would be based on data quality
        return round(random.uniform(0.75, 0.95), 2)
