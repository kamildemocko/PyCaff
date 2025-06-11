import sys
from pathlib import Path

from loguru import logger

from models import PowerManager

class Initializator:
    def __init__(self) -> None:
        self.backup_path = (
            Path(".")
            .joinpath("backups")
            .joinpath("timeouts.json")
        )

        if self.backup_path.exists():
            print(sys.argv)
            if len(sys.argv) > 1 and sys.argv[1] == "--restore":
                pow = PowerManager(self.backup_path)
                pow.restore_backed_up_timeouts()
                pow.remove_backed_up_timeouts()
                sys.exit(0)

            else:
                print("old backup found, either restore backup "
                    "with '--restore' flag or delete backup folder")
                sys.exit(1)