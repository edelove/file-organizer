# File organizer
A smart Python-based file organizer that scans a directory and organizes files into folders by their extension.  
Cross-platform ready (Windows, Linux, macOS), with safe handling of file locks, permissions, and invalid paths.

# Features
Organizes files into folders by extension (e.g. `.pdf` → `/PDF`)  
Automatically resolves filename conflicts (`file (1).pdf`, `file (2).pdf`)  
Skips locked/inaccessible/corrupted files  
Simulates changes with `--dry-run` mode  
Logs all operations to `organize.log` (with rotating logs)  
Cross-platform (Windows, Linux, macOS)  
Packaged into `.exe` via PyInstaller  
Installable as CLI tool via `setup.py`

# Logging
All operations are logged to organize.log.
The log rotates automatically to prevent large file sizes.

# Arguments
--directory DIRECTORY => Point the directory you want to organize
--dry-run (FALSE by default) => Specify if you want to only see what will be done without making changes.

# Usage

### Run via Python
```bash
python file_organiser.py --directory "path_to_your_folder"

# Example run
python file_organiser.py --directory "C:\Downloads" --dry-run

Input directory:
C:\Downloads
│
├── resume.pdf
├── image.png
├── document.docx

Results:
C:\Downloads
├── PDF
│   └── resume.pdf
├── PNG
│   └── image.png
├── DOCX
│   └── document.docx

# CLI Installation
pip install .
organizer --directory "C:\path\to\folder"



# Author
edelove