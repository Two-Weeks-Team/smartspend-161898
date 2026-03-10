import os
import json
import re
import httpx
from typing import Any, Dict, List


def _extract_json(text: str) -> str:
    """Extract a JSON block from LLM output that may be wrapped in markdown.
    """
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Any:
    url = "https://inference.do-ai.run/v1/chat/completions"
    api_key = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    model = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
    headers: Dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Expected OpenAI‑compatible structure
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            json_str = _extract_json(content)
            if not json_str:
                return {"note": "AI returned no JSON content"}
            return json.loads(json_str)
        except Exception as exc:
            # Graceful fallback – never raise to the caller
            return {"note": f"AI service unavailable: {str(exc)}"}


async def call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Any:
    """Public async wrapper used by route handlers.
    """
    return await _call_inference(messages, max_tokens)
