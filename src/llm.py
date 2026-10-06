import os
import json
import requests
from typing import Optional, Dict, Any

class LLMUnavailable(Exception):
    """Raised when an LLM provider fails, times out, or exceeds rate limits (§7)."""
    pass

class LLMSessionTracker:
    """Tracks per-session LLM usage with a strict cap (§7 of build spec)."""
    def __init__(self, max_calls: int = 10):
        self.max_calls = max_calls
        self.call_count = 0

    def can_call(self) -> bool:
        return self.call_count < self.max_calls

    def record_call(self):
        self.call_count += 1

    def remaining_calls(self) -> int:
        return max(0, self.max_calls - self.call_count)


# Global default tracker
_DEFAULT_TRACKER = LLMSessionTracker(max_calls=10)


def generate(
    prompt: str, 
    system: Optional[str] = None, 
    json_mode: bool = False,
    override_provider: Optional[str] = None,
    override_api_key: Optional[str] = None,
    session_tracker: Optional[LLMSessionTracker] = None
) -> str:
    """
    Provider-agnostic LLM generation function complying with §7 of build spec.
    Providers: 'none' | 'gemini' | 'groq' | 'anthropic' (default: 'none').
    Falls back gracefully and raises typed LLMUnavailable on network or token exhaustion.
    """
    tracker = session_tracker or _DEFAULT_TRACKER
    
    provider = (override_provider or os.getenv("LLM_PROVIDER", "none")).strip().lower()
    if provider in ["none", "off", ""]:
        raise LLMUnavailable("LLM mode disabled (LLM_PROVIDER=none). Operating in deterministic mode.")

    if not tracker.can_call():
        raise LLMUnavailable(f"Session cap of {tracker.max_calls} LLM calls reached. Auto-switching to template mode.")

    # 1. Google Gemini (Free Tier Supported)
    if provider == "gemini":
        api_key = override_api_key or os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise LLMUnavailable("Gemini API key not configured.")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        parts = []
        if system:
            parts.append({"text": f"System Instructions: {system}\n\n"})
        parts.append({"text": prompt})
        
        payload: Dict[str, Any] = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 350
            }
        }
        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"
            
        try:
            resp = requests.post(url, json=payload, timeout=8)
            if resp.status_code != 200:
                raise LLMUnavailable(f"Gemini API returned status {resp.status_code}: {resp.text[:120]}")
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise LLMUnavailable("Gemini returned empty candidate list.")
            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            tracker.record_call()
            return text.strip()
        except requests.RequestException as e:
            raise LLMUnavailable(f"Gemini connection error: {e}")

    # 2. Groq (Free Tier Supported)
    elif provider == "groq":
        api_key = override_api_key or os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise LLMUnavailable("Groq API key not configured.")
            
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 350
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
            
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=8)
            if resp.status_code != 200:
                raise LLMUnavailable(f"Groq API returned status {resp.status_code}: {resp.text[:120]}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            tracker.record_call()
            return content.strip()
        except requests.RequestException as e:
            raise LLMUnavailable(f"Groq connection error: {e}")

    # 3. Anthropic (Optional)
    elif provider == "anthropic":
        api_key = override_api_key or os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise LLMUnavailable("Anthropic API key not configured.")
            
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 350,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system:
            payload["system"] = system
            
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=8)
            if resp.status_code != 200:
                raise LLMUnavailable(f"Anthropic returned status {resp.status_code}: {resp.text[:120]}")
            data = resp.json()
            content = data["content"][0]["text"]
            tracker.record_call()
            return content.strip()
        except requests.RequestException as e:
            raise LLMUnavailable(f"Anthropic connection error: {e}")

    else:
        raise LLMUnavailable(f"Unsupported LLM_PROVIDER: '{provider}'. Allowed: none, gemini, groq, anthropic")
