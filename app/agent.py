"""
OpenAI-compatible model client for Azure OpenAI / OpenAI-compatible endpoints.

This replaces the Foundry agent-based implementation and posts to
`/chat/completions` using the configured deployment name (model) and API key.
"""

import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import requests

from app.config import Settings

logger = logging.getLogger(__name__)

# Import system prompt if available
try:
    from system_prompt import SYSTEM_PROMPT_AI102
except ImportError:
    SYSTEM_PROMPT_AI102 = "You are a helpful assistant. Respond in the same language as the user."

# Thread pool for running sync HTTP operations asynchronously
executor = ThreadPoolExecutor(max_workers=4)


class AIAgent:
    """Simple OpenAI-compatible model client using REST calls."""

    def __init__(self, settings: Settings):
        self.settings = settings
        # endpoint is expected like: https://<resource>.openai.azure.com/openai/v1
        self.endpoint = settings.azure_endpoint.rstrip("/")
        self.api_key = settings.azure_api_key
        # deployment name or model identifier (e.g. gpt-5-mini)
        self.model = settings.azure_deployment_id
        self.api_version = settings.azure_api_version or None
        # System prompt - use AI-102 if configured
        if settings.use_ai102_system_prompt:
            self.system_prompt = SYSTEM_PROMPT_AI102
        else:
            self.system_prompt = "You are a helpful assistant. Respond in the same language as the user."

    async def process_message(self, user_message: str, conversation_history: list = None, max_tokens: int = 20000) -> str:
        """Send a user message to the model and return the assistant response.

        This method is async but performs the HTTP call in a thread pool.
        Accepts full conversation history for context.
        """
        if conversation_history is None:
            conversation_history = []
        return await asyncio.get_event_loop().run_in_executor(
            executor, self._process_message_sync, user_message, conversation_history, max_tokens
        )

    def _process_message_sync(self, user_message: str, conversation_history: list = None, max_tokens: int = 20000) -> str:
        if conversation_history is None:
            conversation_history = []
            
        url = f"{self.endpoint}/chat/completions"
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

        # Construir mensajes: sistema + histórico completo
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Agregar el histórico completo de conversación
        for msg in conversation_history:
            if msg.get("role") in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})

        payload = {
            "model": self.model,
            "messages": messages,
            # Azure OpenAI variant expects `max_completion_tokens`
            "max_completion_tokens": max_tokens,
        }

        params = {}
        if self.api_version:
            params["api-version"] = self.api_version

        logger.debug(f"POST {url} payload={payload} params={params}")

        resp = requests.post(url, headers=headers, json=payload, params=params, timeout=30)
        if resp.status_code != 200:
            msg = resp.text
            logger.error(f"Model call failed: {resp.status_code} {msg}")
            raise Exception(f"Model call failed: {resp.status_code} {msg}")

        data = resp.json()

        # Try to extract the assistant content from standard OpenAI-style response
        assistant_text: Optional[str] = None
        try:
            choices = data.get("choices") or []
            if choices:
                first = choices[0]
                # Extract from 'message' field (most common)
                msg = first.get("message") or {}
                if isinstance(msg, dict):
                    assistant_text = msg.get("content")
                # Fallback to 'delta' field
                if not assistant_text:
                    delta = first.get("delta") or {}
                    if isinstance(delta, dict):
                        assistant_text = delta.get("content")
                # Last fallback to 'text' field
                if not assistant_text:
                    assistant_text = first.get("text")
        except Exception:
            logger.exception("Failed to parse model response")

        # If content is empty but we got 'finish_reason': 'length', model ran out of tokens
        if not assistant_text and data.get("choices"):
            finish_reason = data["choices"][0].get("finish_reason")
            if finish_reason == "length":
                logger.warning(f"Model response was truncated (finish_reason=length).")
                # Return a helpful message instead of error
                return "[La respuesta fue truncada - aumentando límite de tokens. Por favor intente nuevamente.]"

        if not assistant_text:
            raise Exception(f"No assistant response found in model output: {data}")

        return assistant_text

    def clear_history(self):
        # No server-side history stored for this client; noop
        logger.info("clear_history called - no-op for OpenAI-compatible model client")
