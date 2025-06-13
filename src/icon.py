import atexit
from typing import Callable

from PIL import Image
import pystray


class Icon:
    icon_off = Image.open("./resources/icon_off.png")
    icon_on = Image.open("./resources/icon_on.png")

    def __init__(self, func_on: Callable, func_off: Callable) -> None:
        self.icon = pystray.Icon(
            "pycaff", 
            Icon.icon_off, 
            "PyCaff", 
            self._set_menu()
        )
        self.turn_on = func_on
        self.turn_off = func_off
        self.caffeinated: bool = False
    
    def _set_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(
                lambda x: "Stop" if self.caffeinated else "Start", 
                self._toggle, 
                default=True,
            ),
            pystray.MenuItem("Quit", self._quit),
        )
    
    def run(self) -> None:
        self.icon.run()
    
    def _toggle(self) -> None:
        if self.caffeinated:
            self.turn_off()
            self.caffeinated = False
            atexit.unregister(self._quit)

            self.icon.icon = Icon.icon_off
            self.icon.notify("Your system is py-caffeinated")

        else:
            self.turn_on()
            self.caffeinated = True
            atexit.register(self._quit)

            self.icon.icon = Icon.icon_on
            self.icon.notify("Your system is no longer py-caffeinated")

        self.icon.update_menu()


    def _quit(self) -> None:
        if self.caffeinated:
            self.turn_off()
            self.caffeinated = False

        self.icon.stop()
