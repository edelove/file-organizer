import os
import platform
import logging
from constants import DEFAULT_EXTENSION, SUPPORTED_PLATFORMS

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
    return ext if ext else DEFAULT_EXTENSION

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
    if system not in SUPPORTED_PLATFORMS:
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