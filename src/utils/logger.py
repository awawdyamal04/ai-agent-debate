import sys
from pathlib import Path

from loguru import logger


def setup_logger(log_file: Path | None = None, verbose: bool = False) -> None:
    """Configure loguru sinks: console + optional rotating file."""
    logger.remove()

    level = "DEBUG" if verbose else "INFO"
    console_fmt = "<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
    logger.add(sys.stderr, level=level, format=console_fmt, colorize=True)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_fmt = "{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{line} | {message}"
        logger.add(
            str(log_file),
            level="DEBUG",
            format=file_fmt,
            rotation="10 MB",
            retention="7 days",
            encoding="utf-8",
        )
        logger.info(f"File logging active → {log_file}")


def get_logger():
    return logger
