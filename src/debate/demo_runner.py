"""Demo runner — produces all result files without requiring API keys.

All arguments are pre-written and clearly labelled [DEMO MODE].
This demonstrates the full architecture: JSON protocol, JSONL logging,
gatekeeper tracking, evidence collection, and results persistence.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.panel import Panel

from src.agents.demo import (
    CON_ARGS, PRO_ARGS, JUDGE_EVALS, JUDGE_OPENING, JUDGE_VERDICT,
    get_demo_con_msg, get_demo_pro_msg,
)
from src.config.settings import RESULTS_DIR
from src.gatekeeper import Gatekeeper
from src.tools.logging_tool import LoggingTool
from src.utils.results import save_evidence, save_transcript, save_verdict


class DemoRunner:
    """Runs the full debate flow using pre-written demo arguments."""

    def __init__(self, num_rounds: int = 10) -> None:
        self.num_rounds = max(num_rounds, 10)
        self.gatekeeper = Gatekeeper()
        self.console = Console()
        self.messages: list[dict] = []
        self.evidence_map: dict = {}
        self.log_tool = LoggingTool(RESULTS_DIR / "events.jsonl")

    def _panel(self, text: str, title: str, style: str) -> None:
        self.console.print(Panel(text[:600], title=f"[DEMO] {title}", style=style, expand=False))

    def execute(self) -> dict:
        topic = "Do smartphones make us less smart?"
        self.log_tool.log_debate_start(topic, self.num_rounds)
        self.console.rule(f"[bold yellow][DEMO MODE] DEBATE: {topic}")
        self.console.print("[yellow]⚠ Running in DEMO mode — no API key. Arguments are pre-written.[/yellow]\n")

        self._panel(JUDGE_OPENING, "JUDGE — Opening", "yellow")

        for rnd in range(1, self.num_rounds + 1):
            self.console.rule(f"[dim]Exchange {rnd} / {self.num_rounds}")

            pro_msg = get_demo_pro_msg(rnd, rnd)
            self.log_tool.log_message(pro_msg)
            self._panel(pro_msg["claim"], f"PRO — Round {rnd}", "blue")

            con_msg = get_demo_con_msg(rnd, rnd, pro_msg["claim"])
            self.log_tool.log_message(con_msg)
            self._panel(con_msg["claim"], f"CON — Round {rnd}", "red")

            eval_note = JUDGE_EVALS[min(rnd - 1, len(JUDGE_EVALS) - 1)]
            self.log_tool.log_evaluation(rnd, eval_note)

            self.messages.extend([pro_msg, con_msg])
            self.evidence_map[str(rnd)] = {
                "pro_evidence": pro_msg.get("evidence", []),
                "con_evidence": con_msg.get("evidence", []),
            }
            self.gatekeeper.track_exchange()
            self.gatekeeper.track_round()

        # Verdict
        winner = "Con"
        self._panel(JUDGE_VERDICT, "JUDGE — Final Verdict", "yellow")
        self.console.print(f"\n[bold green]WINNER: {winner.upper()} (DEMO)[/bold green]\n")
        self.log_tool.log_verdict(winner, JUDGE_VERDICT)
        self.log_tool.log_debate_end(winner, self.num_rounds)

        t_path = save_transcript(self.messages)
        e_path = save_evidence(self.evidence_map)
        v_path = save_verdict(winner, JUDGE_VERDICT)

        summary = {
            "mode": "DEMO — no API keys used",
            "winner": winner,
            "total_exchanges": self.num_rounds,
            "transcript_path": str(t_path),
            "evidence_path": str(e_path),
            "verdict_path": str(v_path),
            "gatekeeper": self.gatekeeper.get_summary(),
            "finished_at": datetime.now().isoformat(),
        }
        self.gatekeeper.save(RESULTS_DIR / "run_summary.json")
        self.console.print(f"[dim]Saved: {t_path.name} | {v_path.name} | run_summary.json | events.jsonl")
        return summary
