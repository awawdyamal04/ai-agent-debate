import json
from datetime import datetime
from pathlib import Path

from loguru import logger


class LoggingTool:
    """Structured JSONL event logger — one JSON object per line in results/events.jsonl."""

    def __init__(self, events_path: Path) -> None:
        self.events_path = events_path
        self.events_path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, event_type: str, data: dict) -> None:
        event = {"timestamp": datetime.now().isoformat(), "event_type": event_type, **data}
        with open(self.events_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event) + "\n")

    def log_debate_start(self, topic: str, num_rounds: int) -> None:
        self._write("debate_start", {"topic": topic, "num_rounds": num_rounds})
        logger.info(f"[Event] debate_start topic='{topic}' rounds={num_rounds}")

    def log_message(self, msg: dict) -> None:
        self._write("debate_message", {
            "speaker": msg.get("speaker"),
            "round": msg.get("round_number"),
            "exchange": msg.get("exchange_number"),
            "claim_chars": len(msg.get("claim", "")),
            "evidence_count": len(msg.get("evidence", [])),
            "fallback_used": msg.get("tool_metadata", {}).get("fallback_used", False),
            "status": msg.get("status"),
        })

    def log_evaluation(self, round_num: int, notes: str) -> None:
        self._write("judge_evaluation", {"round": round_num, "notes_chars": len(notes)})
        logger.info(f"[Event] judge_evaluation round={round_num}")

    def log_verdict(self, winner: str, verdict_text: str) -> None:
        self._write("verdict", {"winner": winner, "verdict_chars": len(verdict_text)})
        logger.info(f"[Event] verdict winner={winner}")

    def log_error(self, error: str, context: dict | None = None) -> None:
        self._write("error", {"error": error, "context": context or {}})
        logger.error(f"[Event] error: {error}")

    def log_debate_end(self, winner: str, total_exchanges: int) -> None:
        self._write("debate_end", {"winner": winner, "total_exchanges": total_exchanges})
        logger.info(f"[Event] debate_end winner={winner} exchanges={total_exchanges}")
