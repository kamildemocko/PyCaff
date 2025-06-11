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
    def __init__(self) -> None:
        self._backup_path = Path(".").joinpath("backups").joinpath("timeouts.json")
        self.original_timeouts = self._get_timeouts()

    @staticmethod
    def _get_timeouts() -> "Timeouts":
        """
        Gets timeout in seconds for AC and DC
        AC - plugged in
        DC - battery
        """
        cmd = "powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE"
        result = subprocess.check_output(cmd, text=True)
        matches = re.findall(r'Power Setting Index: 0x([0-9a-fA-F]+)', result)

        return Timeouts(
            int(matches[0], 16),
            int(matches[1], 16)
        )

    def backup_original_timeouts(self) -> None:
        """
        Backups up current timeouts to a folder - ./backups/timeouts.json
        """
        logger.info(f"backing up original timeouts to {self._backup_path}")

        if not self._backup_path.exists():
            self._backup_path.parent.mkdir(parents=True, exist_ok=True)

        with self._backup_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(self.original_timeouts), file)

    def restore_backed_up_timeouts(self) -> None:
        """
        Restores backed up timeouts, if missing throws an error
        """
        logger.info(f"restoring original timeouts from {self._backup_path}")

        with self._backup_path.open("r", encoding="utf-8") as file:
            dtimeouts = json.load(file)
            timeouts = Timeouts(**dtimeouts)
        
        self.set_timeouts(timeouts)
    
    def remove_backed_up_timeouts(self) -> None:
        """
        Deletes backup file
        """
        logger.info(f"deleting backup timeouts from {self._backup_path}")

        if not self._backup_path.exists():
            return

        self._backup_path.unlink()


    def set_timeouts(self, timeouts: Timeouts):
        """
        Sets new timeout values

        Args:
            timeouts (Timeouts): Timeouts to set
        """
        logger.info(f"setting new  timeouts: {timeouts}")

        subprocess.call(f'powercfg -change -standby-timeout-ac {timeouts.ac / 60}')
        subprocess.call(f'powercfg -change -standby-timeout-dc {timeouts.dc / 60}')
