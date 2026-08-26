"""
Base LLM orchestration layer supporting Gemini API, Claude API, and high-fidelity local execution.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel

from config import ANTHROPIC_API_KEY, GEMINI_API_KEY
from rules_engine import rules_engine

logger = logging.getLogger("pawpawdoo.llm")

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """Unified client handling Gemini and Claude calls with rule injection."""

    @staticmethod
    def call_gemini(
        prompt: str,
        system_instruction: str,
        response_model: Optional[Type[T]] = None,
    ) -> Any:
        """Executes a call to Gemini API using google-genai or returns structured schema."""
        active_rules = rules_engine.format_rules_for_prompt()
        full_system = f"{system_instruction}\n\n### MANDATORY ACTIVE RULES:\n{active_rules}"

        if GEMINI_API_KEY:
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=GEMINI_API_KEY)
                config_kwargs = {}
                if response_model:
                    config = types.GenerateContentConfig(
                        system_instruction=full_system,
                        response_mime_type="application/json",
                        response_schema=response_model,
                        temperature=0.2,
                    )
                else:
                    config = types.GenerateContentConfig(
                        system_instruction=full_system,
                        temperature=0.2,
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config,
                )
                if response_model:
                    return response_model.model_validate_json(response.text)
                return response.text
            except Exception as e:
                logger.warning(f"Live Gemini API call failed ({e}), falling back to structured engine.")

        return None

    @staticmethod
    def call_claude(
        prompt: str,
        system_instruction: str,
        response_model: Optional[Type[T]] = None,
    ) -> Any:
        """Executes a call to Claude API using Anthropic SDK or returns structured schema."""
        active_rules = rules_engine.format_rules_for_prompt()
        full_system = f"{system_instruction}\n\n### MANDATORY ACTIVE RULES:\n{active_rules}"

        if ANTHROPIC_API_KEY:
            try:
                import anthropic

                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                system_prompt = full_system
                if response_model:
                    system_prompt += f"\n\nYou MUST respond strictly in valid JSON matching this schema:\n{json.dumps(response_model.model_json_schema())}"

                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw_text = message.content[0].text
                if response_model:
                    # Clean potential markdown wrapping
                    clean_json = raw_text.strip()
                    if clean_json.startswith("```json"):
                        clean_json = clean_json[7:]
                    if clean_json.startswith("```"):
                        clean_json = clean_json[3:]
                    if clean_json.endswith("```"):
                        clean_json = clean_json[:-3]
                    return response_model.model_validate_json(clean_json.strip())
                return raw_text
            except Exception as e:
                logger.warning(f"Live Claude API call failed ({e}), falling back to structured engine.")

        return None

