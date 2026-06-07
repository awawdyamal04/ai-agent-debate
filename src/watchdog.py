import time
import threading
from functools import wraps
from typing import Any, Callable, Optional

from loguru import logger

from src.config.settings import (
    MAX_RETRIES,
    RETRY_WAIT_MIN,
    RETRY_WAIT_MAX,
    CIRCUIT_BREAKER_THRESHOLD,
    CIRCUIT_BREAKER_RESET,
)

try:
    import anthropic
    import requests
    RETRYABLE = (
        anthropic.APITimeoutError,
        anthropic.RateLimitError,
        requests.Timeout,
        requests.ConnectionError,
        TimeoutError,
        OSError,
    )
except ImportError:
    RETRYABLE = (TimeoutError, OSError)


def with_retry(
    max_attempts: int = MAX_RETRIES,
    wait_min: int = RETRY_WAIT_MIN,
    wait_max: int = RETRY_WAIT_MAX,
    fallback: Any = None,
) -> Callable:
    """Decorator: retry on transient errors with exponential back-off."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except RETRYABLE as exc:
                    last_exc = exc
                    wait = min(wait_min * (2 ** (attempt - 1)), wait_max)
                    logger.warning(
                        f"[Watchdog] {func.__name__} attempt {attempt}/{max_attempts} "
                        f"failed ({type(exc).__name__}) — retry in {wait}s"
                    )
                    if args and hasattr(args[0], "gatekeeper"):
                        args[0].gatekeeper.track_retry()
                    time.sleep(wait)
            if fallback is not None:
                logger.error(
                    f"[Watchdog] {func.__name__} exhausted retries — using fallback"
                )
                if args and hasattr(args[0], "gatekeeper"):
                    args[0].gatekeeper.track_recovery()
                return fallback
            raise last_exc  # type: ignore[misc]

        return wrapper

    return decorator


class CircuitBreaker:
    """Opens after N consecutive failures; resets after cooldown."""

    def __init__(
        self,
        threshold: int = CIRCUIT_BREAKER_THRESHOLD,
        reset_timeout: int = CIRCUIT_BREAKER_RESET,
    ) -> None:
        self.threshold = threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.is_open = False
        self.opened_at: Optional[float] = None
        self._lock = threading.Lock()

    def record_failure(self) -> None:
        with self._lock:
            self.failure_count += 1
            if self.failure_count >= self.threshold and not self.is_open:
                self.is_open = True
                self.opened_at = time.time()
                logger.warning(f"[CircuitBreaker] OPENED after {self.failure_count} failures")

    def record_success(self) -> None:
        with self._lock:
            self.failure_count = 0

    def allow_request(self) -> bool:
        with self._lock:
            if not self.is_open:
                return True
            elapsed = time.time() - (self.opened_at or 0)
            if elapsed >= self.reset_timeout:
                self.is_open = False
                self.failure_count = 0
                logger.info("[CircuitBreaker] RESET — resuming requests")
                return True
            remaining = int(self.reset_timeout - elapsed)
            logger.warning(f"[CircuitBreaker] OPEN — blocking ({remaining}s to reset)")
            return False


global_circuit_breaker = CircuitBreaker()
