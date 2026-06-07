from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.config.settings import RESULTS_DIR


def _ensure() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR


def save_transcript(messages: list[dict]) -> Path:
    path = _ensure() / "transcript.json"
    data = {
        "topic": "Do smartphones make us less smart?",
        "saved_at": datetime.now().isoformat(),
        "total_messages": len(messages),
        "pro_messages": sum(1 for m in messages if m.get("speaker") == "Pro"),
        "con_messages": sum(1 for m in messages if m.get("speaker") == "Con"),
        "messages": messages,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.info(f"Transcript → {path} ({len(messages)} messages)")
    return path


def save_evidence(evidence_map: dict) -> Path:
    path = _ensure() / "evidence.json"
    data = {
        "saved_at": datetime.now().isoformat(),
        "total_rounds": len(evidence_map),
        "evidence_by_round": evidence_map,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.info(f"Evidence → {path}")
    return path


def save_verdict(winner: str, verdict_text: str, scores: dict | None = None) -> Path:
    path = _ensure() / "verdict.json"
    data = {
        "saved_at": datetime.now().isoformat(),
        "winner": winner,
        "verdict_text": verdict_text,
        "scores": scores or {},
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.info(f"Verdict → {path} (winner={winner})")
    return path


def save_run_summary(summary: dict) -> Path:
    path = _ensure() / "run_summary.json"
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    logger.info(f"Run summary → {path}")
    return path


def load_transcript(path: Path | None = None) -> dict:
    if path is None:
        path = _ensure() / "transcript.json"
    return json.loads(path.read_text(encoding="utf-8"))
