from init import Initializator
from models import PowerManager
from models import Timeouts
from icon import Icon


def main():
    init = Initializator()
    pow = PowerManager(init.backup_path)

    def turn_on():
        pow.load_original_timeouts()
        pow.backup_original_timeouts()
        pow.set_timeouts(Timeouts(0, 0))
    
    def turn_off():
        pow.restore_backed_up_timeouts()
        pow.remove_backed_up_timeouts()
    
    def show_logs():
        pow.open_logs(init.info_log_path)

    icon = Icon(turn_on, turn_off, show_logs)
    icon.run()


if __name__ == "__main__":
    main()
