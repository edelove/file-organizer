################################################# !!! !!! ###################################################################
# This repository contains only the CLI-compatible version of File Organizer.                                               #
# The full GUI version is available via our Gumroad store: [Buy Premium Version](dayasoftware.gumroad.com/l/file-organizer) #
#                                                                                                                           #
# For developers, this repo serves as a reference and base for custom CLI tools.                                            #
# **Want to test the full version for free?**                                                                               #
# Reach out to me at: **adam.czlapinski@gmail.com**                                                                         #
################################################# !!! !!! ###################################################################


## File Organizer

Smart. Safe. Efficient.
Sorts files into folders based on their extension. No duplicates. No mess.

## Features

Organizes files by extension (.jpg → /JPG)
Resolves name conflicts (file (1).jpg, file (2).jpg)
Skips locked, read-only, or invalid files
Dry-run mode (preview without changes)
Clean logging with log rotation
GUI + CLI included
Windows, Linux, macOS supported
GUI saves config automatically

## How It Works

# GUI users:
Run python gui.py, select folders, choose options, start organizing.
Config is saved to user_config.json and wiped on exit.

# CLI users:
Run with config:

python file_organiser.py --config user_config.json
Logging
Logs stored in organize.log
Log file rotates at 1MB (max 5 backups).
GUI also displays log output after each run.

## EXE ready to use
You can run this tool without installing anything or running any command.
Go to ./dist and File Organizer.exe

## Developer Setup
# Install dependencies:

pip install -r requirements.txt
Install as CLI tool (optional):
pip install .
Package into .exe with PyInstaller:
pyinstaller gui.spec

## License

This tool is provided under a personal-use license. See [LICENSE.txt](LICENSE.txt) for more information.

## Author
Made by: edelove