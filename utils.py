"""Utility functions for AgentForge."""
import json, re
from datetime import datetime

def sanitize_output(text: str) -> str:
    """Remove markdown code fences from LLM output."""
    text = re.sub(r"```json\n?", "", text)
    text = re.sub(r"```\n?", "", text)
    return text.strip()

def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")

def safe_json_parse(text: str, fallback=None):
    try: return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return fallback if fallback is not None else {"raw": text}
