import sys
from pathlib import Path

from models import PowerManager

from loguru import logger


def set_up_logger(info_log_path: Path) -> None:
    logger.remove()
    logger.add(
        info_log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {module}:{function} - {message}",
        level="INFO",
        rotation="1 month",
        retention="12 months",
        backtrace=True,
    )
    if not sys.stdout:
        return 

    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {module}:{function} - {message}",
        level="INFO",
    )


class Initializator:
    def __init__(self) -> None:
        self.info_log_path = Path("./logs/run.txt")
        self.backup_path = (
            Path(".")
            .joinpath("backups")
            .joinpath("timeouts.json")
        )
