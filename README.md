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


## Arguments
| Flag             | Description                                                   |
|------------------|---------------------------------------------------------------|
| `--directory`     | Required. Path to the folder you want to organize             |
| `--dry-run`       | Optional. Simulates actions without moving files (default: `False`) |

---

## Logging
All operations are logged to `organize.log` in real-time.  
The log uses rotation (max size 1MB, 5 backups) to ensure maintainability.

##  Usage

##  Run via Python
```bash
python file_organiser.py --directory "path_to_your_folder"

# Example Directory - Before
C:\Downloads
├── resume.pdf
├── image.png
├── document.docx

# Example Directory - After
C:\Downloads
├── PDF
│   └── resume.pdf
├── PNG
│   └── image.png
├── DOCX
│   └── document.docx

#CLI Installation
pip install .
organizer --directory "C:\path\to\folder"
'''

# Author
edelove