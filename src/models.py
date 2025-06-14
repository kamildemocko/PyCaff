from typing import Any
from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
import re
import json
import subprocess

from loguru import logger


@dataclass
class Timeouts:
    ac: int
    dc: int


class PowerManager:
    def __init__(self, backup_path: Path) -> None:
        self._backup_path: Path = backup_path
        self.original_timeouts: Timeouts | None = None
        self.timeouts_loaded: bool = False

        self.startup_info = subprocess.STARTUPINFO()
        self.startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.startup_info.wShowWindow = 0

    def load_original_timeouts(self) -> None:
        """
        Gets timeout in seconds for AC and DC
        AC - plugged in
        DC - battery
        """
        cmd = "powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE"
        result = subprocess.check_output(cmd, text=True, startupinfo=self.startup_info)
        matches = re.findall(r'Power Setting Index: 0x([0-9a-fA-F]+)', result)

        self.original_timeouts = Timeouts(
            int(matches[0], 16),
            int(matches[1], 16)
        )
        self.timeouts_loaded = True

    def backup_original_timeouts(self) -> None:
        """
        Backups up current timeouts to a folder - ./backups/timeouts.json
        """
        if not self.timeouts_loaded:
            raise RuntimeError("original timeouts not loaded, call load_original_timeouts() first")

        logger.debug(f"backing up original timeouts to {self._backup_path}")

        if not self._backup_path.exists():
            self._backup_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.original_timeouts:
            raise ValueError("cannot find timeouts on the system")

        with self._backup_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(self.original_timeouts), file)

    def restore_backed_up_timeouts(self) -> None:
        """
        Restores backed up timeouts, if missing throws an error
        """
        logger.debug(f"restoring original timeouts from {self._backup_path}")

        if not self._backup_path.exists():
            ValueError("backup file does not exist, cannot restore timeouts")

        with self._backup_path.open("r", encoding="utf-8") as file:
            dtimeouts: dict[str, Any] = json.load(file)
            if len(dtimeouts.keys()) != 2:
                raise ValueError("backup file is not valid")

            timeouts = Timeouts(**dtimeouts)
        
        self.set_timeouts(timeouts)
    
    def remove_backed_up_timeouts(self) -> None:
        """
        Deletes backup file
        """
        logger.debug(f"deleting backup timeouts from {self._backup_path}")

        if not self._backup_path.exists():
            return

        self._backup_path.unlink()


    def set_timeouts(self, timeouts: Timeouts) -> None:
        """
        Sets new timeout values

        Args:
            timeouts (Timeouts): Timeouts to set
        """
        logger.debug(f"setting new  timeouts: {timeouts}")

        subprocess.call(
            f'powercfg -change -standby-timeout-ac {timeouts.ac / 60}',
            startupinfo=self.startup_info,
        )
        subprocess.call(
            f'powercfg -change -standby-timeout-dc {timeouts.dc / 60}',
            startupinfo=self.startup_info,
        )
