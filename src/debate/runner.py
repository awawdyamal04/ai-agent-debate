from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.panel import Panel

from src.config.settings import RESULTS_DIR
from src.gatekeeper import Gatekeeper
from src.tools.logging_tool import LoggingTool
from src.utils.results import (
    save_evidence,
    save_transcript,
    save_verdict,
)


class DebateRunner:
    """Executes the debate loop on behalf of JudgeAgent.

    The Judge initialises, calls Pro and Con each round, evaluates,
    verifies ≥10 exchanges, then declares the winner.
    """

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

    def _run_exchange(self, exchange_num: int, last_con_msg: dict | None) -> tuple[dict, dict]:
        ctx_pro = {
            "round_number": exchange_num,
            "exchange_number": exchange_num,
            "last_opponent_message": last_con_msg,
        }
        pro_msg = self.pro.respond(ctx_pro)
        pro_msg["status"] = "complete"
        self.log_tool.log_message(pro_msg)
        self._panel(pro_msg.get("claim", ""), f"PRO — Round {exchange_num}", "blue")

        ctx_con = {
            "round_number": exchange_num,
            "exchange_number": exchange_num,
            "last_opponent_message": pro_msg,
        }
        con_msg = self.con.respond(ctx_con)
        con_msg["status"] = "complete"
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
        assert pro_count >= 10, f"Only {pro_count} Pro messages — minimum 10 required"
        logger.info(f"[Runner] {pro_count} exchanges verified ≥ 10")

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
