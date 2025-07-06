import sys
from pathlib import Path

from loguru import logger
import ctypes

from models import PowerManager, Timeouts


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
        set_up_logger(self.info_log_path)

        self.backup_path = (
            Path(".")
            .joinpath("backups")
            .joinpath("timeouts.json")
        )


    def handle_startup_backup_recovery(self, pow: PowerManager) -> None:
        """
        Restores backed up timeouts, if found backup at startup
        This will only happen if program terminates unexpectedly
        """
        if not self.backup_path.exists():
            return

        response = ctypes.windll.user32.MessageBoxW(
            0,
            "Backup of timeout was found.\n"
            "This can happen if this application terminates without restoring original setting.\n\n"
            "Would you like to go ahead and restore it?\n"
            "If it's not recovered, the setting will be overwritten.",
            "Found timeout setting backup...",
            4
        )

        logger.info(f"found backup, restoring original timeouts from {self.backup_path}")

        # 6=yes;7=no
        match response:
            case 6:
                pow.load_original_timeouts()
                pow.remove_backed_up_timeouts()
            case 7:
                pow.remove_backed_up_timeouts()
            case _:
                raise NotImplementedError("backed up timeouts dialog response is not 6 or 7")

    def handle_startup_already_user_set_caffeinated(self, pow: PowerManager) -> None:
        pow.load_original_timeouts()

        if pow.original_timeouts == Timeouts(0, 0):
            ctypes.windll.user32.MessageBoxW(
                0,
                "Your computer is already set not to turn off.\n"
                "Edit your power plan settings and set it to a different setting from 'Never'",
                "Your computer power plan is set to 'Never'",
                0
            )
