from __future__ import annotations

from datetime import datetime
from loguru import logger

from src.agents.base import BaseAgent
from src.config.settings import MAX_TOKENS_JUDGE, MIN_EXCHANGES, SKILLS_DIR
from src.debate.protocol import DebateMessage, ToolMetadata, messages_to_text
from src.gatekeeper import Gatekeeper
from src.watchdog import with_retry


class JudgeAgent(BaseAgent):
    """Active Father/Moderator: orchestrates the debate and declares one winner.

    Skill: src/skills/judge_skill.md defines evaluation criteria and verdict format.
    """

    def __init__(self, gatekeeper: Gatekeeper) -> None:
        super().__init__(SKILLS_DIR / "judge_skill.md", gatekeeper)
        self.evaluation_notes: list[str] = []

    def _judge_call(self, prompt: str, max_tokens: int = 512) -> str:
        return self._api_call([{"role": "user", "content": prompt}], max_tokens)

    @with_retry(fallback="[FALLBACK] Opening: The debate begins. Both sides present your best arguments.")
    def generate_opening(self) -> str:
        prompt = (
            "Open this debate formally. State the topic, introduce both sides, "
            "remind them of the rules (10 rounds minimum, maintain position, use evidence), "
            "and invite the Pro side to make the first argument."
        )
        text = self._judge_call(prompt, max_tokens=512)
        logger.info("[Judge] Opening statement generated")
        return text

    @with_retry(fallback="[FALLBACK] Both arguments noted. Proceeding.")
    def evaluate_exchange(self, round_num: int, pro_msg: dict, con_msg: dict) -> str:
        pro_claim = pro_msg.get("claim", "")
        con_claim = con_msg.get("claim", "")
        prompt = (
            f"=== Round {round_num} Evaluation ===\n"
            f"PRO argued:\n{pro_claim}\n\n"
            f"CON argued:\n{con_claim}\n\n"
            "Score each side 0–10 on: factual evidence quality, relevance, consistency, "
            "rebuttal strength, use of sources, logical clarity. "
            "State which side won this round and why (2–3 sentences)."
        )
        notes = self._judge_call(prompt, max_tokens=512)
        self.evaluation_notes.append(f"Round {round_num}: {notes}")
        logger.info(f"[Judge] Exchange {round_num} evaluated ({len(notes)} chars)")
        return notes

    @with_retry(fallback=None)
    def _verdict_call(self, prompt: str) -> str:
        return self._judge_call(prompt, max_tokens=MAX_TOKENS_JUDGE)

    def declare_winner(self, messages: list[dict]) -> tuple[str, str]:
        transcript = messages_to_text(messages)
        all_notes = "\n\n".join(self.evaluation_notes)
        prompt = (
            f"FULL DEBATE TRANSCRIPT:\n{transcript}\n\n"
            f"YOUR EVALUATION NOTES:\n{all_notes}\n\n"
            f"Total exchanges: {len([m for m in messages if m.get('speaker') in ('Pro','Con')])}\n\n"
            "Based on the full transcript and your round-by-round notes, declare the winner. "
            "Evaluate: factual evidence quality, relevance, consistency, rebuttal strength, "
            "use of external sources, logical clarity. "
            "No ties allowed. Write 'WINNER: Pro' or 'WINNER: Con' on its own line."
        )
        for attempt in range(3):
            verdict_text = self._verdict_call(prompt)
            if verdict_text is None:
                continue
            for line in verdict_text.splitlines():
                stripped = line.strip().upper()
                if stripped.startswith("WINNER:"):
                    token = stripped.replace("WINNER:", "").strip()
                    if "PRO" in token:
                        logger.info("[Judge] Winner declared: Pro")
                        return "Pro", verdict_text
                    if "CON" in token:
                        logger.info("[Judge] Winner declared: Con")
                        return "Con", verdict_text
            logger.warning(f"[Judge] Could not parse winner (attempt {attempt + 1})")
        raise ValueError("Judge failed to declare a clear winner after 3 attempts")

    def respond(self, context: dict) -> dict:
        """Judge responds with an evaluation message."""
        notes = context.get("notes", "Evaluation pending.")
        msg = DebateMessage(
            round_number=context.get("round_number", 0),
            exchange_number=context.get("exchange_number", 0),
            speaker="Judge",
            stance="JUDGE",
            claim=notes,
            tool_metadata=ToolMetadata(tools_used=["anthropic"]),
            confidence_score=1.0,
            timestamp=datetime.now().isoformat(),
            status="complete",
        )
        return msg.to_dict()

    def run_debate(self, pro: BaseAgent, con: BaseAgent, num_rounds: int = MIN_EXCHANGES) -> dict:
        """Active orchestration entry-point — Judge drives the full ping-pong loop."""
        from src.debate.runner import DebateRunner
        runner = DebateRunner(judge=self, pro=pro, con=con, num_rounds=num_rounds)
        return runner.execute()
