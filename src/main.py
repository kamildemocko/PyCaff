import msvcrt

from init import Initializator
from models import PowerManager
from models import Timeouts


def main():
    init = Initializator()

    pow = PowerManager(init.backup_path)
    pow.load_original_timeouts()
    pow.backup_original_timeouts()

    try:
        pow.set_timeouts(Timeouts(0, 0))

        print("System is py-caffeinated!")
        print("Press any key to exit")

        msvcrt.getch()

    finally:
        print("Restoring timeouts...")
        pow.restore_backed_up_timeouts()
        pow.remove_backed_up_timeouts()



if __name__ == "__main__":
    main()
