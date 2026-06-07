import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from loguru import logger


@dataclass
class _Stats:
    rounds: int = 0
    exchanges: int = 0
    characters_used: int = 0
    search_calls: int = 0
    retries: int = 0
    failures_recovered: int = 0
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())


class Gatekeeper:
    """Tracks rounds, exchanges, token-approximation, search calls, retries, recoveries."""

    def __init__(self) -> None:
        self._stats = _Stats()

    def track_round(self) -> None:
        self._stats.rounds += 1

    def track_exchange(self) -> None:
        self._stats.exchanges += 1

    def track_tokens(self, char_count: int) -> None:
        self._stats.characters_used += char_count

    def track_search_call(self) -> None:
        self._stats.search_calls += 1

    def track_retry(self) -> None:
        self._stats.retries += 1

    def track_recovery(self) -> None:
        self._stats.failures_recovered += 1

    def get_summary(self) -> dict:
        s = self._stats
        return {
            "rounds": s.rounds,
            "exchanges": s.exchanges,
            "characters_used": s.characters_used,
            "approx_tokens": s.characters_used // 4,
            "search_calls": s.search_calls,
            "retries": s.retries,
            "failures_recovered": s.failures_recovered,
            "start_time": s.start_time,
            "end_time": datetime.now().isoformat(),
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.get_summary(), indent=2))
        logger.info(f"Gatekeeper stats saved → {path}")

    def log_status(self) -> None:
        s = self._stats
        logger.info(
            f"[Gatekeeper] rounds={s.rounds} exchanges={s.exchanges} "
            f"chars={s.characters_used} searches={s.search_calls} "
            f"retries={s.retries} recovered={s.failures_recovered}"
        )
