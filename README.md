# PyCaff

PyCaff is a Python utility that prevents your Windows system from going to sleep. It temporarily disables sleep mode timeouts and restores them when you exit the application.

## Features

- Disables system sleep mode while running
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

## Manual

Run the application to prevent your system from sleeping:

```cmd
uv run ./src/main.py
```

Press any key to exit and restore original power settings.

If the application exits unexpectedly, you can restore your original power settings with:

```bash
python -m src.main --restore
```

### Script

You can create a batch file to easily run PyCaff:

1. Create a file named `pycaff.bat` with the following content:

```batch
@echo off
SET "LOGURU_LEVEL=INFO"
uv run ./src/main.py
```

2. Save the batch file in the PyCaff root folder
3. Create a shortcut to this batch file
3. Double-click the batch file whenever you want to prevent your system from sleeping

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.