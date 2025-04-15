# File organizer
A smart Python-based file organizer that scans a directory and organizes files into folders by their extension.  
Cross-platform ready (Windows, Linux, macOS), with safe handling of file locks, permissions, and invalid paths.

# Features
Organizes files by extension (e.g. .pdf → /PDF)

Resolves filename conflicts (file (1).pdf, file (2).pdf)

Skips locked, inaccessible or invalid files

Dry-run mode to preview changes before execution

Real-time logging with rotating file logs

Cross-platform: Windows, Linux, macOS

CLI + GUI support

Installable via setup.py or packaged into .exe


## Arguments
| Flag             | Description                                                        |
|------------------|---------------------------------------------------------------     |
| --config	Optional. Path to a .json file with multiple directories and dry-run flag   |


---

## Logging
All operations are logged to `organize.log` in real-time.  
The log uses rotation (max size 1MB, 5 backups) to ensure maintainability.

##  Usage

##  Developer Installation
# Install dependencies
pip install -r requirements.txt

# Build CLI entry point
pip install .


## CLI Installation
# Single-folder sort (real mode)
python file_organiser.py --directory "C:\Downloads"

# Preview-only mode (no changes)
python file_organiser.py --directory "C:\Downloads" --dry-run

# Load from config file
python file_organiser.py --config user_config.json


## GUI Usage
# Run the graphical interface
python gui.py

In the GUI:

Add one or more folders to sort

Enable dry-run if needed

Click "Run Organizer" to start

Config is saved automatically on run

During execution, buttons are temporarily disabled to prevent conflicts.



# Author
edelove