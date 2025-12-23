"""Base researcher module."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random
import json
from backend.utils.search import get_search_results
from backend.utils.llm import llm_service


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
    
    async def perform_ai_research(self, query_suffix: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper to perform search + AI extraction loop.

        Args:
            query_suffix: Suffix to append to entity name for search (e.g. "financial revenue").
            schema: Expected JSON schema for the output.

        Returns:
            Dict containing the extracted data.
        """
        # 1. Search
        query = f"{self.entity_name} {query_suffix}"

        # Use a mix of providers for broad coverage.
        # DDG is good for general queries, Google News for news.
        providers = ["duckduckgo", "google_news", "wikipedia"]
        search_results = get_search_results(query, limit=5, providers=providers)

        # 2. Prepare Context
        context = ""
        for item in search_results:
            context += f"Source: {item.get('source')} - Title: {item.get('title')}\n"
            context += f"Snippet: {item.get('snippet', 'No snippet')}\n\n"

        if not context:
            context = "No search results found."

        # 3. Call LLM
        prompt = f"Analyze the following search results for {self.entity_name} ({self.entity_type}) and extract the requested information."

        data = await llm_service.generate_json(prompt, context, schema)

        return data

    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary from the research data."""
        return f"Analysis completed for {self.entity_name}"
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for the research."""
        # Simple confidence based on data completeness
        if not data:
            return 0.0

        filled_fields = sum(1 for v in data.values() if v and v != "N/A" and v != [])
        total_fields = len(data)

        if total_fields == 0:
            return 0.0

        return round(filled_fields / total_fields, 2)
