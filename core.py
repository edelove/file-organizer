import logging
import os
import shutil
from utils import normalize_extension,has_permission,is_valid_path,is_file_locked,resolve_conflict,validate_input_directory

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

def organize_files(checking_dir, dry_run):
    extensions = scan_extensions(checking_dir)

    for extension in extensions:
        ext_folder_path = os.path.join(checking_dir, extension.upper())

        if dry_run:
            logging.info(f"[DRY RUN] Would create folder: {ext_folder_path}")
        else:
            os.makedirs(ext_folder_path, exist_ok=True)

        for file in os.listdir(checking_dir):
            src_path = os.path.join(checking_dir, file)
            if os.path.isfile(src_path):
                _, file_ext = os.path.splitext(file)
                current_ext = normalize_extension(file_ext)

                if current_ext == extension:
                    if dry_run:
                        logging.info(f"[DRY RUN] Would move: {src_path} → {ext_folder_path}")
                        continue

                    dest_path = os.path.join(ext_folder_path, file)
                    resolved_dest_path = resolve_conflict(dest_path)

                    if should_move_file(src_path, resolved_dest_path):
                        logging.info(f"Moving from {src_path} to {resolved_dest_path}")
                        shutil.move(src_path, resolved_dest_path)

    if not dry_run:
        cleanup_empty_folders(checking_dir, extensions)
    else:
        logging.info("[DRY RUN] Skipping cleanup of empty folders.")