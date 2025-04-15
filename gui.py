import tkinter as tk
from tkinter import filedialog, messagebox
import json
from file_organiser import main as run_organizer

buttons_to_toggle = []
def save_config(directories, dry_run):
    config = {
        "directories":directories,
        "dry_run":dry_run
    }
    with open("user_config.json","w") as config_file:
        json.dump(config, config_file, indent=2)

def browse_directories():
    dir_path = filedialog.askdirectory()
    if dir_path:
        directory_listbox.insert(tk.END,dir_path)

def generate_config():
    directories = directory_listbox.get(0,tk.END)
    dry_run = bool(dry_run_var.get())

    if not directories:
        messagebox.showwarning("Input Missing", "Please Add at least one directory.")
        return

    save_config(list(directories),dry_run)

def run_with_config():
    config_path = "user_config.json"
    try:
        run_organizer(config_path)
        messagebox.showinfo("Success","Organizer finished running successfully")
    except Exception as e:
        messagebox.showerror("Error","Failed to run organizer: \n".format(e))

def run_frum_gui():
    toggle_buttons("disabled")
    update_status("Running organizer...", "blue")
    generate_config()
    try:
        run_organizer(config_file="user_config.json")
        update_status("Organizer finished successfully.", "green")
        messagebox.showinfo("Success", "Organizer has completed.")
    except Exception as e:
        update_status(f"Error: {e}", "red")
        messagebox.showerror("Error","Something went wrong: {}".format(e))
    finally:
        toggle_buttons("normal")
        if clear_after_run_var.get():
            directory_listbox.delete(0, tk.END)

def toggle_buttons(state):
    for button in buttons_to_toggle:
        button.config(state=state)

def update_status(message, color="green"):
    status_label.config(text=message,fg=color)
    root.update_idletasks()

# Main Window
root = tk.Tk()
root.title("File Organizer Config")
root.geometry("500x400")

# Instruction label
instruction = tk.Label(root, text="Select folder(s) to organize:",font=("Arial",12))
instruction.pack(pady=10)

# Directory Listbox
directory_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=10)
directory_listbox.pack()

# Dry Run Checkbox
dry_run_var = tk.BooleanVar()
dry_run_checkbox = tk.Checkbutton(root, text="Dry Run (No actual changes)",variable=dry_run_var)
dry_run_checkbox.pack(pady=5)
buttons_to_toggle.append(dry_run_checkbox)
clear_after_run_var = tk.BooleanVar()
clear_after_run_checkbox = tk.Checkbutton(root,text="Clear list after run",variable=clear_after_run_var)
clear_after_run_checkbox.pack(pady=5)
buttons_to_toggle.append(clear_after_run_checkbox)

# Buttons
browse_btn = tk.Button(root, text="Add folder",command=browse_directories)
browse_btn.pack()
buttons_to_toggle.append(browse_btn)
generate_btn = tk.Button(root, text="Save Configuration",command=generate_config)
generate_btn.pack(pady=10)
buttons_to_toggle.append(generate_btn)
clear_btn = tk.Button(root, text="Clear",command=lambda: directory_listbox.delete(0,tk.END))
clear_btn.pack(pady=5)
buttons_to_toggle.append(clear_btn)
#run_btn = tk.Button(root, text="Run Organizer",command=run_with_config)
#run_btn.pack(pady=5)
run_button = tk.Button(root, text="Run Organizer", command=run_frum_gui)
run_button.pack(pady=5)
buttons_to_toggle.append(run_button)

# Loading label
status_label = tk.Label(root,text="",fg="green",font=("Arial",10))
status_label.pack(pady=5)

root.mainloop()