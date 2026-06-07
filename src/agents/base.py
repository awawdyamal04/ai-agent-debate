from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import anthropic
from loguru import logger

from src.config.settings import ANTHROPIC_API_KEY, API_TIMEOUT, MODEL_NAME
from src.gatekeeper import Gatekeeper


class BaseAgent(ABC):
    """Abstract base for all debate agents.

    Subclasses must implement respond(context) -> dict returning a
    DebateMessage-compatible dict.

    Skill files (markdown in src/skills/) define HOW the agent thinks.
    Tools (src/tools/) define WHAT the agent can do.
    """

    def __init__(self, skill_path: Path, gatekeeper: Gatekeeper) -> None:
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=API_TIMEOUT)
        self.skill_path = skill_path
        self.system_prompt: str = self._load_skill()
        self.conversation_history: list[dict] = []
        self.gatekeeper = gatekeeper
        self.name = self.__class__.__name__
        logger.info(f"[{self.name}] initialized | skill={skill_path.name}")

    def _load_skill(self) -> str:
        try:
            return self.skill_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.warning(f"Skill file not found: {self.skill_path}")
            return ""

    def _api_call(self, messages: list[dict], max_tokens: int = 1024) -> str:
        """Raw Anthropic API call — no retry logic (apply via watchdog decorator at call site)."""
        response = self.client.messages.create(
            model=MODEL_NAME,
            system=self.system_prompt,
            messages=messages,
            max_tokens=max_tokens,
        )
        text: str = response.content[0].text
        self.gatekeeper.track_tokens(len(text))
        return text

    def get_history(self) -> list[dict]:
        return list(self.conversation_history)

    def reset(self) -> None:
        self.conversation_history.clear()
        logger.debug(f"[{self.name}] history cleared")

    @abstractmethod
    def respond(self, context: dict) -> dict:
        """Return a DebateMessage-compatible dict for the given context."""
