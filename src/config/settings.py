import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = BASE_DIR / "results"
SKILLS_DIR = BASE_DIR / "src" / "skills"

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

MODEL_NAME: str = "claude-sonnet-4-6"
MIN_EXCHANGES: int = 10
MAX_TOKENS_AGENT: int = 1024
MAX_TOKENS_JUDGE: int = 2048
MAX_RETRIES: int = 3
RETRY_WAIT_MIN: int = 2
RETRY_WAIT_MAX: int = 8
API_TIMEOUT: int = 60
CIRCUIT_BREAKER_THRESHOLD: int = 5
CIRCUIT_BREAKER_RESET: int = 120
SERPER_URL: str = "https://google.serper.dev/search"
SERPER_RESULTS_COUNT: int = 3
DEBATE_TOPIC: str = "Do smartphones make us less smart?"
PRO_POSITION: str = "Yes, smartphones make us less smart."
CON_POSITION: str = "No, smartphones do not make us less smart."


class ConfigurationError(Exception):
    pass


def validate_config() -> None:
    if not ANTHROPIC_API_KEY:
        raise ConfigurationError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    if not SERPER_API_KEY:
        import warnings
        warnings.warn(
            "SERPER_API_KEY is not set — running in fallback/demo evidence mode.",
            stacklevel=2,
        )
