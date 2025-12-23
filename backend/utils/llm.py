"""LLM Service for interacting with Gemini and OpenAI."""
import os
import json
import logging
import google.generativeai as genai
from openai import OpenAI
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        self.gemini_client = None
        self.openai_client = None

        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.gemini_client = genai.GenerativeModel('gemini-pro')

        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)

    async def generate_json(self, prompt: str, context: str, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate JSON output using available LLMs.
        Prioritizes Gemini, falls back to OpenAI.
        """
        full_prompt = f"""
        Context Information:
        {context}

        Task:
        {prompt}

        Instructions:
        - Analyze the context carefully.
        - Extract or infer the requested information.
        - Return ONLY valid JSON matching the structure.
        - Do not include markdown formatting (like ```json ... ```).
        - If information is missing, make a reasonable estimate based on context or use null/generic values,
          but try to be as accurate as possible.
        """

        if schema:
            full_prompt += f"\nExpected JSON Structure: {json.dumps(schema, indent=2)}"

        # Try Gemini
        if self.gemini_client:
            try:
                response = self.gemini_client.generate_content(full_prompt)
                text = response.text
                return self._parse_json(text)
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")

        # Try OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",  # Cost effective, supports JSON mode
                    messages=[
                        {"role": "system", "content": "You are a helpful researcher who extracts structured data from text. Return only JSON."},
                        {"role": "user", "content": full_prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                text = response.choices[0].message.content
                return self._parse_json(text)
            except Exception as e:
                logger.error(f"OpenAI generation failed: {e}")

        # If both fail or keys missing
        logger.warning("No LLM available or both failed. Returning empty dict.")
        return {}

    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Clean and parse JSON string."""
        try:
            # Remove markdown code blocks if present
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]

            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}. Text: {text}")
            return {}

llm_service = LLMService()
