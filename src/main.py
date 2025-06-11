import msvcrt

from models import PowerManager
from models import Timeouts


def main():
    pow = PowerManager()
    pow.backup_original_timeouts()

    try:
        pow.set_timeouts(Timeouts(0, 0))

        print("press any key to exit")
        msvcrt.getch()

    finally:
        pow.restore_backed_up_timeouts()
        pow.remove_backed_up_timeouts()



if __name__ == "__main__":
    main()
