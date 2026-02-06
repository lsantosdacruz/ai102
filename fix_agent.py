#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update agent.py to increase max_tokens and improve error handling
"""

with open("app/agent.py", "r", encoding="utf-8") as f:
    content = f.read()

# Cambio 1: Aumentar max_tokens a 2048 en process_message
content = content.replace(
    'async def process_message(self, user_message: str, max_tokens: int = 512) -> str:',
    'async def process_message(self, user_message: str, max_tokens: int = 2048) -> str:'
)

# Cambio 2: Aumentar max_tokens a 2048 en _process_message_sync
content = content.replace(
    'def _process_message_sync(self, user_message: str, max_tokens: int = 512) -> str:',
    'def _process_message_sync(self, user_message: str, max_tokens: int = 2048) -> str:'
)

# Cambio 3: Mejorar el parsing de respuestas
old_parsing = '''        # Try to extract the assistant content from standard OpenAI-style response
        assistant_text: Optional[str] = None
        try:
            choices = data.get("choices") or []
            if choices:
                first = choices[0]
                # Newer chat response shape
                msg = first.get("message") or first.get("delta") or {}
                if isinstance(msg, dict):
                    # message.content or message.get('content')
                    assistant_text = msg.get("content") or msg.get("content", None)
                # fallback to text field
                if not assistant_text:
                    assistant_text = first.get("text")
        except Exception:
            logger.exception("Failed to parse model response")

        if not assistant_text:
            # As a last resort, try other locations
            assistant_text = data.get("choices", [{}])[0].get("message", {}).get("content") if data.get("choices") else None

        if not assistant_text:
            raise Exception(f"No assistant response found in model output: {data}")

        return assistant_text'''

new_parsing = '''        # Try to extract the assistant content from standard OpenAI-style response
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

        return assistant_text'''

content = content.replace(old_parsing, new_parsing)

with open("app/agent.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] app/agent.py actualizado:")
print("  - max_tokens aumentado a 2048")
print("  - Mejor manejo de respuestas vacías")
print("  - Mejor manejo de truncado (finish_reason=length)")
