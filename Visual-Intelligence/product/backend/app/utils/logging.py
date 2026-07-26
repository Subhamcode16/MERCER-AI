"""
Mercer AI — Structured Logging

Filters sensitive data from all log records before they are emitted.
Prompt content and API keys must never appear in logs — only job IDs and
sanitised metadata.
"""
import logging
import re
from typing import ClassVar


# Patterns that should never appear in logs
_SENSITIVE_PATTERNS: list[re.Pattern] = [
    re.compile(r'"prompt"\s*:\s*"[^"]*"', re.IGNORECASE),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),           # OpenAI key
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),          # Google API key
    re.compile(r"rzp_[a-zA-Z0-9_]{20,}"),           # Razorpay key
    re.compile(r"\"password\"\s*:\s*\"[^\"]*\"", re.IGNORECASE),
    re.compile(r"\"secret\"\s*:\s*\"[^\"]*\"", re.IGNORECASE),
    re.compile(r"Bearer [a-zA-Z0-9\-_.]+"),          # JWT / Bearer tokens
]


class SensitiveDataFilter(logging.Filter):
    """
    Strips sensitive patterns from log messages before emission.
    Attach to every handler — not just the root logger.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
            for pattern in _SENSITIVE_PATTERNS:
                msg = pattern.sub("[REDACTED]", msg)
            record.msg = msg
            record.args = ()   # already formatted above
        except Exception:
            pass               # never let logging itself crash the app
        return True


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging with the sensitive data filter.
    Call once at startup (main.py) before any other imports emit logs.
    """
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    handler.addFilter(SensitiveDataFilter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # Quieten noisy third-party loggers
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
