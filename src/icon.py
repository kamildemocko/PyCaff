import atexit
from typing import Callable

from PIL import Image
import pystray


class Icon:
    icon_off = Image.open("./resources/icon_off.png")
    icon_on = Image.open("./resources/icon_on.png")

    def __init__(self, func_on: Callable, func_off: Callable, func_logs: Callable) -> None:
        self.turn_on = func_on
        self.turn_off = func_off
        self.show_logs = func_logs
        self.caffeinated: bool = False

        self.icon = pystray.Icon(
            "pycaff", 
            Icon.icon_off, 
            "PyCaff", 
            self._set_menu()
        )
    
    def _set_menu(self) -> list[pystray.MenuItem]:
        return [
            pystray.MenuItem(
                lambda x: "Stop" if self.caffeinated else "Start", 
                self._toggle, 
                default=True,
            ),
            pystray.MenuItem("Logs", self.show_logs),
            pystray.MenuItem("Quit", self._quit),
        ]
    
    def run(self) -> None:
        self.icon.run()
    
    def _toggle(self) -> None:
        if self.caffeinated:
            self.turn_off()
            self.caffeinated = False
            atexit.unregister(self._quit)

            self.icon.icon = Icon.icon_off
            self.icon.notify("Your system is no longer PY-Caffeinated")

        else:
            self.turn_on()
            self.caffeinated = True
            atexit.register(self._quit)

            self.icon.icon = Icon.icon_on
            self.icon.notify("Your system is PY-Caffeinated")

        self.icon.update_menu()
    
    def _quit(self) -> None:
        if self.caffeinated:
            self.turn_off()
            self.caffeinated = False

        self.icon.stop()
