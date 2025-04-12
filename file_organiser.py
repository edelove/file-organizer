import os
import shutil

extensions = set()
checking_dir = input("Provide path to check and organise: ")

print("###############################################\n"
"Directory content:\n")

for file in os.listdir(checking_dir):
    filepath = os.path.join(checking_dir,file)
    if os.path.isfile(filepath):
        print(file)
        _, file_ext = os.path.splitext(file)
        ext = file_ext.replace(".", "").lower()
        if ext == "":
            ext = "no_extension"
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
            current_ext = file_ext.replace(".", "").lower()
            if current_ext == extension:
                dest_path = os.path.join(ext_folder_path, file)
                print("Moving from {} to {}".format(src_path,dest_path))
                try:
                    shutil.move(src_path,dest_path)
                except Exception as e:
                    print("Failed to move {}".format(file))