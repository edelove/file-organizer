import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
from file_organiser import main as run_organizer



buttons_to_toggle = []

def browse_directories():
    dir_path = filedialog.askdirectory()
    if dir_path:
        norm_path = os.path.normpath(dir_path)
        if norm_path not in folder_tree.get_children():
            node = folder_tree.insert("", "end", text=norm_path, open=False)
            populate_tree(node, norm_path)

# Expand logic
def populate_tree(parent, path):
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                folder_tree.insert(parent, "end", text=entry, open=False)
            else:
                folder_tree.insert(parent, "end", text=entry)
    except Exception as e:
        print(f"Error reading {path}: {e}")

def save_config(directories, dry_run, include_subdirs):
    config = {
        "directories":directories,
        "dry_run":dry_run,
        "include_subdirs":include_subdirs
    }
    with open("user_config.json","w") as config_file:
        json.dump(config, config_file, indent=2)



def load_log():
    try:
        with open("organize.log", "r", encoding="utf-8") as log:
            log_lines = log.readlines()
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)
            for line in log_lines[-50:]:
                log_text.insert(tk.END, line)
            log_text.config(state=tk.DISABLED)
    except FileNotFoundError:
        pass

def remove_selected_folder():
    selected_item = folder_tree.selection()
    if selected_item:
        folder_tree.delete(selected_item)

def browse_directories():
    dir_path = filedialog.askdirectory()
    if dir_path:
        existing_dirs = folder_tree.get(0, tk.END)
        if dir_path not in existing_dirs:
            folder_tree.insert(tk.END, dir_path)
        else:
            messagebox.showinfo("Info", "This folder is already in the list.")

def generate_config():
    directories = folder_tree.get(0,tk.END)
    dry_run = bool(dry_run_var.get())
    include_subdirs = bool(include_subdirs_var.get())

    if not directories:
        messagebox.showwarning("Input Missing", "Please Add at least one directory.")
        return

    save_config(list(directories),dry_run,include_subdirs)

def run_with_config():
    config_path = "user_config.json"
    try:
        run_organizer(config_path)
        messagebox.showinfo("Success","Organizer finished running successfully")
    except Exception as e:
        messagebox.showerror("Error","Failed to run organizer: \n".format(e))

def run_frum_gui():
    toggle_buttons("disabled")
    update_status("Generating config...", "blue")

    directories = folder_tree.get(0, tk.END)
    dry_run = bool(dry_run_var.get())
    include_subdirs = bool(include_subdirs_var.get())

    if not directories:
        update_status("Please add at least one folder before running.", "red")
        messagebox.showwarning("Input Missing", "Please add at least one folder.")
        toggle_buttons("normal")
        return

    # Save config and proceed
    save_config(list(directories), dry_run, include_subdirs)
    update_status("Running organizer...", "blue")

    try:
        run_organizer(config_file="user_config.json")
        load_log()
        update_status("Organizer finished successfully.", "green")
        messagebox.showinfo("Success", "Organizer has completed.")
    except Exception as e:
        update_status(f"Error: {e}", "red")
        messagebox.showerror("Error","Something went wrong: {}".format(e))
    finally:
        toggle_buttons("normal")
        if clear_after_run_var.get():
            for item in folder_tree.get_children():
                folder_tree.delete(item)

def toggle_buttons(state):
    for button in buttons_to_toggle:
        button.config(state=state)

def update_status(message, color="green"):
    status_label.config(text=message,fg=color,bg="#1e1e1e",font=("Segoe UI",12,"italic","bold"))
    root.update_idletasks()

def clear_interface():
    for item in folder_tree.get_children():
        folder_tree.delete(item)
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0,tk.END)
    log_text.config(state=tk.DISABLED)
    update_status("Interface cleared.","lightblue")


# Main Frame

# Main Window
root = tk.Tk()
root.title("File Organizer Config")
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())
root.configure(bg="#1e1e1e")
root.iconbitmap("organizer_icon_black.ico")

# Add folder
def browse_directories():
    dir_path = filedialog.askdirectory()
    if dir_path:
        norm_path = os.path.normpath(dir_path)
        if norm_path not in folder_tree.get_children():
            node = folder_tree.insert("", "end", text=norm_path, open=False)
            populate_tree(node, norm_path)

# Expand logic
def populate_tree(parent, path):
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                folder_tree.insert(parent, "end", text=entry, open=False)
            else:
                folder_tree.insert(parent, "end", text=entry)
    except Exception as e:
        print(f"Error reading {path}: {e}")

# Instruction label
instruction = tk.Label(root, text="Select folder(s) to organize:",font=("Segoe UI",15,"bold"),fg="white")
instruction.configure(bg="#1e1e1e")
instruction.pack(pady=(20,30))


# Folder Tree Frame
folder_tree_frame = tk.Frame(root, bg="#1e1e1e", padx=30)
folder_tree_frame.pack(fill="both", expand=True, pady=(0, 20))

# Scrollbars
x_scrollbar = tk.Scrollbar(folder_tree_frame, orient="horizontal")
x_scrollbar.pack(side="bottom", fill="x")

y_scrollbar = tk.Scrollbar(folder_tree_frame, orient="vertical")
y_scrollbar.pack(side="right", fill="y")

# Treeview
folder_tree = ttk.Treeview(
    folder_tree_frame,
    columns=("FullPath",),
    show="tree",
    selectmode="browse",
    xscrollcommand=x_scrollbar.set,
    yscrollcommand=y_scrollbar.set
)
folder_tree.heading("#0", text="Folder / File")
folder_tree.column("#0", anchor="w", stretch=True, minwidth=1000)
folder_tree.pack(fill="both", expand=True)

x_scrollbar.config(command=folder_tree.xview)
y_scrollbar.config(command=folder_tree.yview)


style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#2b2b2b",
    foreground="#f0f0f0",
    fieldbackground="#2b2b2b",
    font=("Segoe UI", 10),
    rowheight=22
)

style.map("Treeview",
    background=[("selected", "#444444")],
    foreground=[("selected", "#ffffff")]
)

buttons_to_toggle.append(folder_tree)


# Checkbox Group Frame
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(pady=10, anchor="s")
checkbox_frame.configure(bg="#1e1e1e")

# Dry Run Checkbox
dry_run_var = tk.BooleanVar()
dry_run_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Dry Run",
    variable=dry_run_var,
    font=("Segoe UI", 10),
    fg="white",               # Text color
    bg="#1e1e1e",             # Background color
    selectcolor="#1e1e1e",    # Background color of the checkbox when selected
    activeforeground="white",
    activebackground="#2e2e2e"
)
dry_run_checkbox.pack(side=tk.LEFT, padx=5)


# Include Subdirectories
include_subdirs_var = tk.BooleanVar()
include_subdirs_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Include subdirectories",
    variable=include_subdirs_var,
    font=("Segoe UI", 10),
    fg="white",               # Text color
    bg="#1e1e1e",             # Background color
    selectcolor="#1e1e1e",    # Background color of the checkbox when selected
    activeforeground="white",
    activebackground="#2e2e2e"
)
include_subdirs_checkbox.pack(side=tk.LEFT, padx=5)

# Clear list after run
clear_after_run_var = tk.BooleanVar()
clear_after_run_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Clear list after run",
    variable=clear_after_run_var,
    font=("Segoe UI", 10),
    fg="white",               # Text color
    bg="#1e1e1e",             # Background color
    selectcolor="#1e1e1e",    # Background color of the checkbox when selected
    activeforeground="white",
    activebackground="#2e2e2e"
)
clear_after_run_checkbox.pack(side=tk.LEFT, padx=5)

buttons_to_toggle.extend([dry_run_checkbox, include_subdirs_checkbox, clear_after_run_checkbox])

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
button_width = 12
button_frame.configure(bg="#1e1e1e")
button_style = {
    "bg": "#2b2b2b",
    "fg": "#f0f0f0",
    "activebackground": "#3c3c3c",
    "activeforeground": "#ffffff",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "padx": 10,
    "font": ("Segoe UI",11),
    "pady": 6,
}

# Add Folder Button
browse_btn = tk.Button(button_frame, text="Add Folder", command=browse_directories,width=button_width,**button_style)
browse_btn.pack(side=tk.LEFT, padx=15)
buttons_to_toggle.append(browse_btn)

# Remove Folder Button
remove_btn = tk.Button(
    button_frame,
    text="Remove Folder",
    command=lambda: remove_selected_folder(),
    width=button_width,
    **button_style
)
remove_btn.pack(side=tk.LEFT, padx=15)
buttons_to_toggle.append(remove_btn)

# Clear Button
clear_btn = tk.Button(button_frame, text="Clear", command=clear_interface, width=button_width,**button_style)
clear_btn.pack(side=tk.LEFT, padx=15)
buttons_to_toggle.append(clear_btn)
run_button = tk.Button(root, text="Run Organizer", command=run_frum_gui, **button_style)
run_button.pack(pady=25)
buttons_to_toggle.append(run_button)



log_label = tk.Label(root,text="Organizer Log Output:",font=("Segoe UI",15,"bold"),fg="white")
log_label.pack(padx=(10,0))
log_label.configure(bg="#1e1e1e")
# Scrollable text
log_frame = tk.Frame(root)
log_scrollbar = tk.Scrollbar(log_frame)
log_text = tk.Text(log_frame, height=10, width=60, wrap=tk.WORD, yscrollcommand=log_scrollbar.set, state=tk.DISABLED)
log_text.configure(bg="#1e1e1e",fg="white",font=("Segoe UI", 8))
log_scrollbar.config(command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)
log_frame.pack(pady=10,padx=15)


# Loading label
status_label = tk.Label(root,text="",fg="green",font=("Segoe UI",12))
status_label.pack(pady=5)

root.mainloop()

