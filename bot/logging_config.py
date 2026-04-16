import logging
import logging.handlers
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(
    level: str = "INFO",
    log_file: str = "app.log",
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
) -> None:
    """
    Call once at application startup (e.g. in main.py).
    All modules that call logging.getLogger(__name__) will
    automatically inherit this config.
    """
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(level.upper())

    # Console handler — INFO and above
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    # Rotating file handler — DEBUG and above (captures everything)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    root.addHandler(console)
    root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Thin convenience wrapper — same as logging.getLogger(name).
    Optional: use this if you want one import across all files.
    """
    return logging.getLogger(name)