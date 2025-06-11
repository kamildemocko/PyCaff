# PyCaff

PyCaff is a Python utility that prevents your Windows system from going to sleep. It temporarily disables sleep mode timeouts and restores them when you exit the application.

## Features

- Disables system sleep mode while running
- Automatically restores original power settings on exit
- Backup and restore functionality for power settings

## Installation

Requires Python 3.10 or higher.

```cmd
# Clone the repository
git clone https://github.com/yourusername/pycaff.git
cd pycaff

# Install dependencies
uv sync
```

## Usage

Run the application to prevent your system from sleeping:

```cmd
uv run ./src/main.py
```

Press any key to exit and restore original power settings.

If the application exits unexpectedly, you can restore your original power settings with:

```bash
python -m src.main --restore
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.