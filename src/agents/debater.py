from __future__ import annotations

from datetime import datetime
from pathlib import Path

from loguru import logger

from src.agents.base import BaseAgent
from src.config.settings import MAX_TOKENS_AGENT
from src.debate.protocol import DebateMessage, EvidenceItem, ToolMetadata
from src.gatekeeper import Gatekeeper
from src.tools.search import SearchTool
from src.watchdog import with_retry


class DebaterAgent(BaseAgent):
    """Shared logic for Pro and Con agents.

    Subclasses set: speaker, stance, and override _get_search_query().
    Skill files define the agent's persona and fixed position.
    """

    speaker: str = ""
    stance: str = ""

    def __init__(self, skill_path: Path, gatekeeper: Gatekeeper) -> None:
        super().__init__(skill_path, gatekeeper)
        self.search_tool = SearchTool()

    def _get_search_query(self, context: dict) -> str:
        raise NotImplementedError

    def _build_prompt(self, context: dict, evidence_text: str) -> str:
        opp_msg = context.get("last_opponent_message") or {}
        opp_name = "Con" if self.speaker == "Pro" else "Pro"
        last_claim = opp_msg.get("claim", "(opening round — no prior argument)") if opp_msg else "(opening round — no prior argument)"
        round_num = context.get("round_number", 1)
        return (
            f"=== Round {round_num} ===\n"
            f"Your opponent ({opp_name}) just argued:\n{last_claim}\n\n"
            f"Search evidence for this round:\n{evidence_text}\n\n"
            f"Now deliver your argument. Directly rebut your opponent's main claim, "
            f"then reinforce your position with evidence."
        )

    @with_retry(fallback="[FALLBACK] Position maintained due to API error.")
    def _call_claude(self, prompt: str) -> str:
        self.conversation_history.append({"role": "user", "content": prompt})
        result = self._api_call(self.conversation_history, MAX_TOKENS_AGENT)
        self.conversation_history.append({"role": "assistant", "content": result})
        return result

    def _extract_claim(self, raw: str) -> str:
        """If LLM returns JSON, extract 'claim'/'text' field; otherwise use raw text."""
        if raw and raw.lstrip().startswith("{"):
            from src.debate.protocol import try_parse_json
            parsed = try_parse_json(raw)
            if isinstance(parsed, dict):
                return str(parsed.get("claim") or parsed.get("text") or raw)
        return raw

    def respond(self, context: dict) -> dict:
        round_num = context.get("round_number", 1)
        exchange_num = context.get("exchange_number", round_num)

        query = self._get_search_query(context)
        evidence_items, fallback_used = self.search_tool.search(query, self.stance)
        self.gatekeeper.track_search_call()
        evidence_text = SearchTool.format_for_agent(evidence_items)

        prompt = self._build_prompt(context, evidence_text)
        claim = self._extract_claim(self._call_claude(prompt))
        is_fallback = claim.startswith("[FALLBACK]")
        if is_fallback:
            self.gatekeeper.track_recovery()

        opp_msg = context.get("last_opponent_message") or {}
        rebuttal_target = (opp_msg.get("claim", "")[:120] if opp_msg else "")

        msg = DebateMessage(
            round_number=round_num,
            exchange_number=exchange_num,
            speaker=self.speaker,
            stance=self.stance,
            claim=claim,
            evidence=evidence_items,
            tool_metadata=ToolMetadata(
                tools_used=["search", "anthropic"],
                search_queries=[query],
                search_results_count=len(evidence_items),
                fallback_used=fallback_used or is_fallback,
            ),
            rebuttal_target=rebuttal_target,
            confidence_score=0.7 if (fallback_used or is_fallback) else 0.85,
            timestamp=datetime.now().isoformat(),
            status="complete",
        )
        logger.info(f"[{self.speaker}] Round {round_num}: {len(claim)} chars | fallback={fallback_used}")
        return msg.to_dict()
