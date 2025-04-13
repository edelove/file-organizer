import os
import shutil
import msvcrt

### CASE SCENARIO HANDLING FUNCTIONS

def validate_input_directory(input_dir):
    if not os.path.exists(input_dir):
        print("Provided path does not exist: {}".format(input_dir))
        return False
    if not os.path.isdir(input_dir):
        print("Provided path is not a directory: {}".format(input_dir))
        return False
    if not any(os.path.isfile(os.path.join(input_dir,f)) for f in os.listdir(input_dir)):
        print("Provided path is empty: {}".format(input_dir))
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
    try:
        with open(src_path, "r+") as f:
            msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK, 1)
            msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK, 1)
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
extensions = set()
checking_dir = input("Provide path to check and organise: ")
if not validate_input_directory(checking_dir):
    exit()

print("###############################################\n"
"Directory content:\n")

for file in os.listdir(checking_dir):
    filepath = os.path.join(checking_dir,file)
    if os.path.isfile(filepath):
        print(file)
        _, file_ext = os.path.splitext(file)
        ext = normalize_extension(file_ext)
        extensions.add(ext)

print("\nAll found extensions:")
print(extensions)

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
                try:
                    if not os.path.exists(src_path):
                        print("WARNING: {} no longer exists, skipping...".format(src_path))
                        continue

                    if not has_permission(src_path):
                        print("WARNING: No permission to access {}, skipping...".format(src_path))
                        continue

                    if is_file_locked(src_path):
                        print("WARNING: {} is locked, skipping...".format(src_path))
                        continue

                    if not is_valid_path(src_path) or not is_valid_path(resolved_dest_path):
                        print("WARNING: Invalid or corrupt path for {}, skipping...".format(src_path))
                        continue

                    print("Moving from {} to {}".format(src_path,resolved_dest_path))
                    shutil.move(src_path,resolved_dest_path)
                except Exception as e:
                    print("Failed to move {}: {}".format(file, e))

for directory in os.listdir(checking_dir):
    full_path = os.path.join(checking_dir, directory)
    if os.path.isdir(os.path.join(checking_dir,directory)) and directory.upper() not in [ ext.upper() for ext in extensions ]:
        if not os.listdir(full_path):
            try:
                os.rmdir(full_path)
                print("Removed empty folder {}".format(full_path))
            except Exception as e:
                print("Failed to remove empty directory {}: {}".format(full_path, e))
