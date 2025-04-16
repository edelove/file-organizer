# File Organizer

Smart. Safe. Straight to the point.  
Python-based tool that organizes files into folders by extension — no duplicates, no clutter, just results.

---

## Features

- Sorts files into folders by extension (`.pdf` → `/PDF`)
- Auto-resolves filename conflicts (`file (1).pdf`, `file (2).pdf`)
- Skips locked, inaccessible or corrupt files
- Dry-run mode to simulate actions without making changes
- Clean, real-time logs with rotation
- CLI and GUI support
- Built for Windows, Linux, and macOS
- GUI saves config automatically — no manual steps needed

---

## How It Works

By default, it reads from `user_config.json` — no arguments needed if using the GUI.  
You choose folders, set dry-run or real-run, hit the button. That’s it.

---

## CLI Usage

> Used mainly for automation or config-based runs.

# Run using config
python file_organiser.py --config user_config.json


## GUI Usage
python gui.py
Inside the GUI:
Add one or more folders

(Optional) Toggle:
Dry Run — for simulation
Include Subdirectories — for deep cleaning
Clear list after run — for reset after organizing
Click Run Organizer
Logs appear in real-time under the file list
All settings saved to user_config.json automatically

## Logging

All actions are logged in organize.log
Log rotation enabled: 1MB max, 5 backup files
Logs are also viewable directly in the GUI after each run

## Developer Setup

# Install dependencies
pip install -r requirements.txt

# Optional: install as CLI tool
pip install .

## Packaging to .exe
Packaged cleanly with PyInstaller. Icon included. One file. No nonsense.

## Made by
edelove