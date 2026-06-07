from __future__ import annotations

import requests
from loguru import logger

from src.config.settings import (
    SERPER_API_KEY,
    SERPER_RESULTS_COUNT,
    SERPER_URL,
    API_TIMEOUT,
)
from src.debate.protocol import EvidenceItem
from src.watchdog import global_circuit_breaker

_FALLBACK: dict[str, list[dict]] = {
    "pro": [
        {"snippet": "[DEMO EVIDENCE] Studies suggest heavy smartphone use correlates with reduced sustained attention and increased distractibility in some populations.", "url": "https://example.com/demo/pro/1"},
        {"snippet": "[DEMO EVIDENCE] Research indicates reliance on search engines may reduce the need to memorise facts, potentially weakening long-term memory consolidation.", "url": "https://example.com/demo/pro/2"},
        {"snippet": "[DEMO EVIDENCE] Constant notifications fragment cognitive focus, hampering deep-work capacity and complex problem-solving ability.", "url": "https://example.com/demo/pro/3"},
        {"snippet": "[DEMO EVIDENCE] Adolescent smartphone overuse linked to lower academic performance in several longitudinal studies.", "url": "https://example.com/demo/pro/4"},
        {"snippet": "[DEMO EVIDENCE] Average screen time has risen sharply, with users checking devices 96 times per day on average.", "url": "https://example.com/demo/pro/5"},
    ],
    "con": [
        {"snippet": "[DEMO EVIDENCE] Smartphones give instant access to encyclopaedic knowledge, extending human cognition beyond biological limits.", "url": "https://example.com/demo/con/1"},
        {"snippet": "[DEMO EVIDENCE] Educational apps and MOOCs delivered via smartphones have democratised learning for millions globally.", "url": "https://example.com/demo/con/2"},
        {"snippet": "[DEMO EVIDENCE] Navigation and productivity tools free working memory for higher-order thinking by outsourcing routine cognitive tasks.", "url": "https://example.com/demo/con/3"},
        {"snippet": "[DEMO EVIDENCE] Research shows moderate smartphone use does not impair cognitive function and may support collaborative intelligence.", "url": "https://example.com/demo/con/4"},
        {"snippet": "[DEMO EVIDENCE] Multilingual translation, accessibility features, and real-time information lookup measurably improve outcomes for users.", "url": "https://example.com/demo/con/5"},
    ],
}


class SearchTool:
    """Serper-backed search with automatic fallback to clearly-labelled demo evidence."""

    def __init__(self) -> None:
        self.api_key = SERPER_API_KEY
        self.use_fallback = not bool(self.api_key)
        if self.use_fallback:
            logger.warning("[SearchTool] No SERPER_API_KEY — using DEMO evidence only")

    def _serper_call(self, query: str) -> list[EvidenceItem]:
        if not global_circuit_breaker.allow_request():
            return []
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": SERPER_RESULTS_COUNT}
        try:
            resp = requests.post(SERPER_URL, headers=headers, json=payload, timeout=API_TIMEOUT)
            resp.raise_for_status()
            raw = resp.json().get("organic", [])
            global_circuit_breaker.record_success()
            return [
                EvidenceItem(
                    snippet=r.get("snippet", ""),
                    url=r.get("link", ""),
                    source="serper",
                    label="live",
                )
                for r in raw[:SERPER_RESULTS_COUNT]
            ]
        except Exception as exc:
            global_circuit_breaker.record_failure()
            logger.warning(f"[SearchTool] Serper failed ({type(exc).__name__}) — fallback")
            return []

    def search(self, query: str, stance: str = "pro") -> tuple[list[EvidenceItem], bool]:
        """Return (items, fallback_used). stance='pro'|'con' selects fallback bucket."""
        if not self.use_fallback:
            items = self._serper_call(query)
            if items:
                return items, False
        key = "con" if "con" in stance.lower() or stance.upper() == "CON" else "pro"
        bucket = _FALLBACK.get(key, _FALLBACK["pro"])
        items = [EvidenceItem(s["snippet"], s["url"], "fallback", "fallback/demo") for s in bucket[:3]]
        return items, True

    @staticmethod
    def format_for_agent(items: list[EvidenceItem]) -> str:
        if not items:
            return "No search evidence available."
        lines = []
        for item in items:
            tag = " [DEMO]" if item.label == "fallback/demo" else ""
            lines.append(f"• {item.snippet}{tag}\n  Source: {item.url}")
        return "\n".join(lines)[:2000]
