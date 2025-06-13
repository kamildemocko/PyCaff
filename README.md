# PyCaff

PyCaff is a Python utility that prevents your Windows system from going to sleep. It temporarily disables sleep mode timeouts and restores them when you exit the application.

## Features

- Disables system sleep mode while running
- System tray icon for easy access
- Toggle between caffeinated (Start/Stop) modes
- Automatically restores original power settings on exit
- Backup and restore functionality for power settings

## Installation

Requires Python 3.10 or higher.  
Requires uv  

```cmd
git clone https://github.com/kamildemocko/PyCaff.git
cd pycaff
uv sync
```

## Usage

Run the application

```cmd
uv run ./src/main.py
```

A system tray icon will appear. Click on it to access the menu:
- **Start/Stop**: Toggle caffeinated mode (prevents sleep when active)
- **Show logs**: Opens up log file in default text app
- **Quit**: Exit the application and restore power settings

If the application exits unexpectedly, you can restore your original power settings with:

```cmd
uv run ./src/main.py --restore
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.