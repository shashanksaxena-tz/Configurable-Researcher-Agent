"""LLM abstraction layer for the Intelligent Research Agent.

Per research.md: Multi-model approach with:
- GPT-4 or Gemini Pro for complex reasoning (planning, verification, synthesis)
- GPT-3.5-turbo or Gemini Flash for extraction tasks

Features:
- Unified interface for OpenAI and Google Gemini
- Retry with exponential backoff (tenacity)
- Model selection based on task type
- Cost optimization through model routing
"""

import os
from typing import Optional, Dict, Any, List
from enum import Enum

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from backend.config import settings


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    GOOGLE = "google"


class TaskType(str, Enum):
    """Task types for model selection routing."""
    PLANNING = "planning"  # Query deconstruction
    EXTRACTION = "extraction"  # Information extraction from search results
    VERIFICATION = "verification"  # Cross-referencing and discrepancy detection
    SYNTHESIS = "synthesis"  # Narrative report generation


# Retry configuration for transient errors
RETRY_CONFIG = dict(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError))
)


def get_model_for_task(task_type: TaskType) -> str:
    """Get the appropriate model for a given task type.
    
    Per research.md: Use powerful models for complex reasoning,
    faster models for extraction.
    
    Args:
        task_type: The type of task to perform
        
    Returns:
        Model name string
    """
    model_map = {
        TaskType.PLANNING: settings.PLANNING_MODEL,
        TaskType.EXTRACTION: settings.EXTRACTION_MODEL,
        TaskType.VERIFICATION: settings.VERIFICATION_MODEL,
        TaskType.SYNTHESIS: settings.SYNTHESIS_MODEL,
    }
    return model_map.get(task_type, settings.PLANNING_MODEL)


class LLMClient:
    """Unified LLM client supporting multiple providers.
    
    Provides a consistent interface for calling OpenAI and Google Gemini
    with automatic retry and error handling.
    """
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        """Initialize the LLM client.
        
        Args:
            provider: Preferred provider, defaults to settings.LLM_PROVIDER
        """
        self.provider = provider or LLMProvider(settings.LLM_PROVIDER)
        self.openai_client = None
        self.google_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients based on available keys."""
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        
        if openai_key:
            try:
                import openai
                self.openai_client = openai.AsyncOpenAI(api_key=openai_key)
            except ImportError:
                pass
        
        if google_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=google_key)
                self.google_client = genai
            except ImportError:
                pass
    
    @retry(**RETRY_CONFIG)
    async def complete(
        self,
        prompt: str,
        task_type: TaskType = TaskType.EXTRACTION,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """Generate a completion for the given prompt.
        
        Args:
            prompt: User prompt text
            task_type: Task type for model selection
            system_prompt: Optional system message
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum response tokens
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        model = get_model_for_task(task_type)
        
        if self.provider == LLMProvider.OPENAI and self.openai_client:
            return await self._openai_complete(
                prompt, model, system_prompt, temperature, max_tokens
            )
        elif self.provider == LLMProvider.GOOGLE and self.google_client:
            return await self._google_complete(
                prompt, task_type, system_prompt, temperature, max_tokens
            )
        else:
            # Fallback: try OpenAI first, then Google
            if self.openai_client:
                return await self._openai_complete(
                    prompt, model, system_prompt, temperature, max_tokens
                )
            elif self.google_client:
                return await self._google_complete(
                    prompt, task_type, system_prompt, temperature, max_tokens
                )
            else:
                raise RuntimeError("No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY.")
    
    async def _openai_complete(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _google_complete(
        self,
        prompt: str,
        task_type: TaskType,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call Google Gemini API."""
        # Select Gemini model based on task complexity
        if task_type in [TaskType.PLANNING, TaskType.VERIFICATION, TaskType.SYNTHESIS]:
            model_name = "gemini-pro"
        else:
            model_name = "gemini-pro"  # Gemini Flash when available
        
        model = self.google_client.GenerativeModel(model_name)
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = await model.generate_content_async(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        
        return response.text
    
    async def complete_json(
        self,
        prompt: str,
        task_type: TaskType = TaskType.EXTRACTION,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a JSON response.
        
        Adds JSON mode instructions and parses the response.
        
        Args:
            prompt: User prompt
            task_type: Task type for model selection
            system_prompt: Optional system message
            **kwargs: Additional parameters
            
        Returns:
            Parsed JSON dictionary
        """
        import json
        
        json_system = (system_prompt or "") + "\n\nRespond ONLY with valid JSON. No markdown, no explanation."
        
        response = await self.complete(
            prompt=prompt,
            task_type=task_type,
            system_prompt=json_system.strip(),
            **kwargs
        )
        
        # Clean up response and parse JSON
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Remove markdown code blocks
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1])
        
        return json.loads(cleaned)


# Global client instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the global LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
