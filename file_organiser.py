import os
import shutil
import argparse
import logging
from logging.handlers import RotatingFileHandler
import platform

### CASE SCENARIO HANDLING FUNCTIONS

def validate_input_directory(input_dir):
    if not os.path.exists(input_dir):
        logging.error("Provided path does not exist: {}".format(input_dir))
        return False
    if not os.path.isdir(input_dir):
        logging.error("Provided path is not a directory: {}".format(input_dir))
        return False
    if not any(os.path.isfile(os.path.join(input_dir,f)) for f in os.listdir(input_dir)):
        logging.error("Provided path is empty: {}".format(input_dir))
        return False
    return True
    
def normalize_extension(extension):
    ext = extension.replace(".","")
    return ext if ext else "UNCLASSIFIED"

def resolve_conflict(dest_path):
    if not os.path.exists(dest_path):
        return dest_path
    base, ext = os.path.splitext(dest_path)
    counter = 1

    while True:
        new_path = "{} ({}){}".format(base, counter, ext)
        if not os.path.exists(new_path):
            return new_path
            
        counter += 1

def is_file_locked(src_path):
    if not os.path.exists(src_path):
        return False
    
    system = platform.system()
    if system not in ["Windows", "Linux", "Darwin"]:
        logging.warning("Unknown OS — skipping file lock check.")
    try:
        if system == "Windows":
            with open(src_path, "r+") as f:
                import msvcrt
                msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK, 1)
                msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK, 1)
                return False
        elif system in ["Linux","Darwin"]:
            try:
                with open(src_path,"r+") as f:
                    import fcntl
                    fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(f,fcntl.LOCK_UN)
                    return False
            except BlockingIOError:
                return True
        else:
            return False
    except (PermissionError, IOError, OSError):
        return True

def has_permission(src_path):
    try:
        with open(src_path,'rb'):
            return True
    except PermissionError:
        return False
    
def is_valid_path(src_path):
    try:
        if os.path.exists(src_path) and os.path.isfile(src_path):
            with open(src_path, 'rb'):
                pass
        else:
            test_dir = os.path.dirname(src_path)
            test_name = os.path.basename(src_path)
            if not os.path.exists(test_dir):
                os.makedirs(test_dir, exist_ok=True)
            test_path = os.path.join(test_dir,test_name)
            with open(test_path,'w') as f:
                f.write("test")
            os.remove(test_path)
        return True
    except (UnicodeEncodeError, OSError, Exception):
        return False
    
### END OF CASE SCENARIO HANDLING FUCNTIONS

### MAIN LOGIC ###
def scan_extensions(checking_dir):
    extensions = set()

    for file in os.listdir(checking_dir):
        filepath = os.path.join(checking_dir,file)
        if os.path.isfile(filepath):
            _, file_ext = os.path.splitext(file)
            ext = normalize_extension(file_ext)
            extensions.add(ext)
    return extensions

def should_move_file(src_path,resolved_dest_path):
    if not os.path.exists(src_path):
        logging.warning("{} no longer exists, skipping...".format(src_path))
        return False

    if not has_permission(src_path):
        logging.warning("No permission to access {}, skipping...".format(src_path))
        return False

    if is_file_locked(src_path):
        logging.warning("{} is locked, skipping...".format(src_path))
        return False

    if not is_valid_path(src_path) or not is_valid_path(resolved_dest_path):
        logging.warning("Invalid or corrupt path for {}, skipping...".format(src_path))
        return False
    
    return True

def cleanup_empty_folders(checking_dir, extensions):
    for directory in os.listdir(checking_dir):
        full_path = os.path.join(checking_dir, directory)
        if os.path.isdir(os.path.join(checking_dir,directory)) and directory.upper() not in [ ext.upper() for ext in extensions ]:
            if not os.listdir(full_path):
                try:
                    os.rmdir(full_path)
                    logging.info("Removed empty folder {}".format(full_path))
                except Exception as e:
                    logging.error("Failed to remove empty directory {}: {}".format(full_path, e))

def parse_args():
    parser = argparse.ArgumentParser(description="Organize files by extensions into folders.")
    parser.add_argument("--directory",required=True,help="The path to the directory you want to organize")
    parser.add_argument("--dry-run",action="store_true",help="Show what would be done without making any changes")

    return parser.parse_args()

def organize_files(checking_dir, dry_run):
    extensions = scan_extensions(checking_dir)

    for extension in extensions:
        ext_folder_path = os.path.join(checking_dir,extension.upper())
        os.makedirs(ext_folder_path,exist_ok=True)

        for file in os.listdir(checking_dir):
            src_path = os.path.join(checking_dir,file)
            if os.path.isfile(src_path):
                _, file_ext = os.path.splitext(file)
                current_ext = normalize_extension(file_ext)
                if current_ext == extension:
                    dest_path = os.path.join(ext_folder_path, file)
                    resolved_dest_path = resolve_conflict(dest_path)
                    if should_move_file(src_path,resolved_dest_path):
                        logging.info("Moving from {} to {}".format(src_path,resolved_dest_path))

                        if not dry_run:
                            shutil.move(src_path,resolved_dest_path)

    cleanup_empty_folders(checking_dir,extensions)


def main():

    file_handler = RotatingFileHandler(
        "organize.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            file_handler,
            logging.StreamHandler()
        ]
    )

    args = parse_args()
    checking_dir = args.directory
    dry_run = args.dry_run

    if not validate_input_directory(checking_dir):
        exit()
    organize_files(checking_dir,dry_run)

if __name__ == "__main__":
    main()
