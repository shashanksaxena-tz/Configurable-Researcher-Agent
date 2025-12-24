"""Base researcher module."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
import asyncio
from backend.utils.search import get_search_results
from backend.utils.llm import llm_service


class BaseResearcher(ABC):
    """Base class for all researcher modules."""
    
    def __init__(self, entity_name: str, entity_type: str, search_provider: Optional[Any] = None):
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.search_provider = search_provider
        self.selected_providers: Optional[List[str]] = None
    
    @abstractmethod
    async def research(self) -> Dict[str, Any]:
        """Perform research and return results."""
        pass
    
    async def _plan_research(self, topic: str) -> List[str]:
        """
        Step 1: Plan.
        Generate specific search queries based on the entity and topic.
        """
        prompt = (
            f"I need to research '{topic}' for the entity '{self.entity_name}' ({self.entity_type}). "
            "Generate 3 specific, targeted search queries to find high-quality, up-to-date information. "
            "Return them as a JSON list of strings."
        )
        try:
            # We treat the prompt as the 'context' for the LLM to generate just the JSON list
            response = await llm_service.generate_json(
                prompt=prompt,
                context=f"Entity: {self.entity_name}, Topic: {topic}",
                schema={"queries": ["string"]}
            )
            return response.get("queries", [f"{self.entity_name} {topic}"])
        except Exception as e:
            print(f"Planning failed: {e}")
            return [f"{self.entity_name} {topic}"]

    async def _synthesize_report(self, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Synthesize.
        Generate a narrative report and extract structured data.
        """
        prompt = (
            f"You are an expert analyst. Analyze the provided research data for '{self.entity_name}' "
            "and write a professional, comprehensive executive summary (approx. 200 words) in Markdown format. "
            "Also extract the specific structured data requested."
        )

        # Extend the schema to include the narrative summary and sources
        full_schema = schema.copy()
        full_schema["narrative_summary"] = "string (Markdown format)"
        full_schema["confidence_score"] = "float (0.0 to 1.0)"
        full_schema["key_sources"] = ["string (URL or Source Name)"]

        return await llm_service.generate_json(prompt, context, full_schema)

    async def perform_ai_research(self, query_suffix: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrated Research Flow: Plan -> Search -> Synthesize.
        """
        # 1. Plan
        queries = await self._plan_research(query_suffix)
        print(f"Research Plan for {self.entity_name} [{query_suffix}]: {queries}")

        # 2. Execute Search (Parallel)
        if self.selected_providers:
            providers = self.selected_providers
        else:
            providers = ["duckduckgo", "google_news", "wikipedia"]

        # Limit total results to avoid overwhelming context window, but gather from multiple queries
        all_results = []
        for query in queries:
            results = get_search_results(query, limit=3, providers=providers)
            all_results.extend(results)

        # Deduplicate results by URL or Title
        seen = set()
        unique_results = []
        for res in all_results:
            identifier = res.get('url') or res.get('title')
            if identifier and identifier not in seen:
                seen.add(identifier)
                unique_results.append(res)

        # 3. Prepare Context
        context = ""
        for item in unique_results:
            context += f"Source: {item.get('source')} - Title: {item.get('title')}\n"
            context += f"URL: {item.get('url', 'N/A')}\n"
            context += f"Snippet: {item.get('snippet', 'No snippet')}\n"
            context += "---\n"

        if not context:
            context = "No search results found."

        # 4. Synthesize
        data = await self._synthesize_report(context, schema)

        # Ensure we return the raw results for the frontend source list
        data["_raw_search_results"] = unique_results

        return data

    def generate_summary(self, data: Dict[str, Any]) -> str:
        """
        Generate a summary from the research data.
        Now prefers the LLM-generated narrative if available.
        """
        if "narrative_summary" in data:
            return data["narrative_summary"]
        return f"Analysis completed for {self.entity_name}"
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for the research."""
        # Prefer the LLM's assessment if available
        if "confidence_score" in data:
            return float(data["confidence_score"])

        # Fallback to simple confidence based on data completeness
        if not data:
            return 0.0

        filled_fields = sum(1 for v in data.values() if v and v != "N/A" and v != [])
        total_fields = len(data)

        if total_fields == 0:
            return 0.0

        return round(filled_fields / total_fields, 2)
