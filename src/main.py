import sys

from init import Initializator
from models import PowerManager
from models import Timeouts
from icon import Icon


def main():
    init = Initializator()
    icon = Icon()

    pow = PowerManager(init.backup_path)
    pow.load_original_timeouts()
    pow.backup_original_timeouts()

    try:
        pow.set_timeouts(Timeouts(0, 0))
        icon.run()

    finally:
        pow.restore_backed_up_timeouts()
        pow.remove_backed_up_timeouts()



if __name__ == "__main__":
    main()
