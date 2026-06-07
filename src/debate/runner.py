from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.panel import Panel

from src.config.settings import RESULTS_DIR
from src.debate.protocol import DebateMessage, ToolMetadata
from src.gatekeeper import Gatekeeper
from src.tools.logging_tool import LoggingTool
from src.utils.results import (
    save_evidence,
    save_transcript,
    save_verdict,
)


class DebateRunner:
    """Executes the debate loop on behalf of JudgeAgent."""

    def __init__(self, judge, pro, con, num_rounds: int) -> None:
        self.judge = judge
        self.pro = pro
        self.con = con
        self.num_rounds = max(num_rounds, 10)
        self.gatekeeper: Gatekeeper = judge.gatekeeper
        self.console = Console()
        self.messages: list[dict] = []
        self.evidence_map: dict = {}
        events_path = RESULTS_DIR / "events.jsonl"
        self.log_tool = LoggingTool(events_path)

    def _panel(self, text: str, title: str, style: str) -> None:
        self.console.print(Panel(text[:800], title=title, style=style, expand=False))

    def _make_fallback_msg(self, speaker: str, stance: str, rnd: int, exc_num: int, reason: str) -> dict:
        msg = DebateMessage(
            round_number=rnd, exchange_number=exc_num,
            speaker=speaker, stance=stance,
            claim=f"[FALLBACK] {speaker} maintains its position. (error: {reason[:80]})",
            tool_metadata=ToolMetadata(tools_used=["fallback"], fallback_used=True),
            confidence_score=0.0, timestamp=datetime.now().isoformat(),
            status="fallback_agent_error",
        )
        return msg.to_dict()

    def _safe_respond(self, agent, ctx: dict, speaker: str, stance: str) -> dict:
        try:
            msg = agent.respond(ctx)
        except Exception as exc:
            logger.error(f"[Runner] {speaker} respond() failed: {exc}")
            self.log_tool.log_error(f"{speaker} agent failed", {"round": ctx.get("round_number"), "error": str(exc)})
            self.gatekeeper.track_recovery()
            return self._make_fallback_msg(speaker, stance, ctx.get("round_number", 0), ctx.get("exchange_number", 0), str(exc))
        if msg.get("stance") != stance:
            logger.warning(f"[Runner] Stance drift {speaker}: got {msg.get('stance')!r}, expected {stance!r}")
            self.log_tool.log_error(f"Stance drift {speaker}", {"got": msg.get("stance"), "expected": stance})
            msg["stance"] = stance
        try:
            json.dumps(msg)
        except (TypeError, ValueError) as exc:
            self.log_tool.log_error(f"{speaker} non-serializable", {"error": str(exc), "status": "fallback_invalid_json"})
            return self._make_fallback_msg(speaker, stance, ctx.get("round_number", 0), ctx.get("exchange_number", 0), "invalid_json")
        msg["status"] = "complete"
        return msg

    def _run_exchange(self, exchange_num: int, last_con_msg: dict | None) -> tuple[dict, dict]:
        ctx_pro = {"round_number": exchange_num, "exchange_number": exchange_num, "last_opponent_message": last_con_msg}
        pro_msg = self._safe_respond(self.pro, ctx_pro, "Pro", "PRO")
        self.log_tool.log_message(pro_msg)
        self._panel(pro_msg.get("claim", ""), f"PRO — Round {exchange_num}", "blue")

        ctx_con = {"round_number": exchange_num, "exchange_number": exchange_num, "last_opponent_message": pro_msg}
        con_msg = self._safe_respond(self.con, ctx_con, "Con", "CON")
        self.log_tool.log_message(con_msg)
        self._panel(con_msg.get("claim", ""), f"CON — Round {exchange_num}", "red")

        notes = self.judge.evaluate_exchange(exchange_num, pro_msg, con_msg)
        self.log_tool.log_evaluation(exchange_num, notes)
        self.evidence_map[str(exchange_num)] = {
            "pro_evidence": pro_msg.get("evidence", []),
            "con_evidence": con_msg.get("evidence", []),
        }
        self.gatekeeper.track_exchange()
        self.gatekeeper.track_round()
        return pro_msg, con_msg

    def execute(self) -> dict:
        topic = getattr(self.judge, "_topic", "Do smartphones make us less smart?")
        self.log_tool.log_debate_start(topic, self.num_rounds)
        self.console.rule(f"[bold yellow]DEBATE: {topic}")

        opening = self.judge.generate_opening()
        self._panel(opening, "JUDGE — Opening", "yellow")

        last_con_msg: dict | None = None
        for exchange_num in range(1, self.num_rounds + 1):
            self.console.rule(f"[dim]Exchange {exchange_num} / {self.num_rounds}")
            pro_msg, con_msg = self._run_exchange(exchange_num, last_con_msg)
            self.messages.extend([pro_msg, con_msg])
            last_con_msg = con_msg

        pro_count = sum(1 for m in self.messages if m.get("speaker") == "Pro")
        con_count = sum(1 for m in self.messages if m.get("speaker") == "Con")
        if pro_count < 10 or con_count < 10:
            logger.error(f"[Runner] Insufficient messages: Pro={pro_count} Con={con_count} (min 10 each)")
            self.log_tool.log_error("Insufficient exchanges", {"pro": pro_count, "con": con_count})
        logger.info(f"[Runner] Verified: Pro={pro_count} Con={con_count}")

        winner, verdict_text = self.judge.declare_winner(self.messages)
        self._panel(verdict_text, "JUDGE — Final Verdict", "yellow")
        self.console.print(f"\n[bold green]WINNER: {winner.upper()}[/bold green]\n")
        self.log_tool.log_verdict(winner, verdict_text)
        self.log_tool.log_debate_end(winner, pro_count)

        t_path = save_transcript(self.messages)
        e_path = save_evidence(self.evidence_map)
        v_path = save_verdict(winner, verdict_text)
        summary = self._build_summary(winner, verdict_text, t_path, e_path, v_path)
        self.gatekeeper.save(RESULTS_DIR / "run_summary.json")
        self.console.print(f"[dim]Saved: {t_path} | {v_path}")
        return summary

    def _build_summary(self, winner, verdict_text, t_path, e_path, v_path) -> dict:
        return {
            "winner": winner,
            "total_exchanges": self.num_rounds,
            "transcript_path": str(t_path),
            "evidence_path": str(e_path),
            "verdict_path": str(v_path),
            "gatekeeper": self.gatekeeper.get_summary(),
            "finished_at": datetime.now().isoformat(),
        }
