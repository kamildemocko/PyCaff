import sys
from pathlib import Path

from models import PowerManager


class Initializator:
    def __init__(self) -> None:
        self.backup_path = (
            Path(".")
            .joinpath("backups")
            .joinpath("timeouts.json")
        )

        restore_flag = False
        if len(sys.argv) > 1 and sys.argv[1] == "--restore":
            restore_flag = True

        if self.backup_path.exists() and restore_flag:
            pow = PowerManager(self.backup_path)
            pow.restore_backed_up_timeouts()
            pow.remove_backed_up_timeouts()
            sys.exit(0)
        
        elif self.backup_path.exists() and not restore_flag:
            print("old backup found, either restore backup "
                "with '--restore' flag or delete backup folder")
            sys.exit(1)

        elif not self.backup_path.exists() and restore_flag:
            print("no backup found, nothing to restore")
            sys.exit(1)
