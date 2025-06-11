import sys

from PIL import Image
import pystray


class Icon:
    icon_off = Image.open("./resources/icon_off.png")
    icon_on = Image.open("./resources/icon_on.png")

    def __init__(self) -> None:
        self.icon = pystray.Icon(
            "pycaff", 
            Icon.icon_off, 
            "PyCaff", 
            self._set_menu()
        )
    
    def _set_menu(self) -> tuple[pystray.MenuItem]:
        return (
            pystray.MenuItem("Start", self._start, default=True),
            pystray.MenuItem("Quit", self._quit),
        )
    
    def run(self) -> None:
        self.icon.run()
    
    def _start(self) -> None:
        print("start")
        self.icon.notify("Your system is py-caffeinated")

    def _quit(self) -> None:
        self.icon.stop()
