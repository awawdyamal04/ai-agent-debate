import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List


@dataclass
class EvidenceItem:
    snippet: str
    url: str
    source: str = "serper"
    label: str = ""


@dataclass
class ToolMetadata:
    tools_used: List[str] = field(default_factory=list)
    search_queries: List[str] = field(default_factory=list)
    search_results_count: int = 0
    fallback_used: bool = False


@dataclass
class DebateMessage:
    """Structured JSON communication unit between all agents."""

    round_number: int
    exchange_number: int
    speaker: str          # "Pro" | "Con" | "Judge"
    stance: str           # "PRO" | "CON" | "JUDGE"
    claim: str
    evidence: List[EvidenceItem] = field(default_factory=list)
    tool_metadata: ToolMetadata = field(default_factory=ToolMetadata)
    rebuttal_target: str = ""
    confidence_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "DebateMessage":
        evidence = [EvidenceItem(**e) for e in data.pop("evidence", [])]
        tm = data.pop("tool_metadata", {})
        tool_meta = ToolMetadata(**tm) if isinstance(tm, dict) else ToolMetadata()
        return cls(**data, evidence=evidence, tool_metadata=tool_meta)


def try_parse_json(text: str, log_error_fn=None) -> dict | None:
    """Parse text as JSON; attempt bracket-repair if malformed; return None on failure."""
    if not text or not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError as exc:
            if log_error_fn:
                log_error_fn(f"JSON repair failed: {exc}", {"raw": text[:200], "status": "fallback_invalid_json"})
    return None


def messages_to_text(messages: list) -> str:
    """Convert list of DebateMessage dicts to human-readable transcript text."""
    lines = []
    for m in messages:
        speaker = m.get("speaker", "?")
        rnd = m.get("round_number", "?")
        claim = m.get("claim", "")
        lines.append(f"=== Round {rnd} — {speaker} ===")
        lines.append(claim)
        lines.append("")
    return "\n".join(lines)
