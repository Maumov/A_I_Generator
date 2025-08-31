import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

CONFIG_FILE = "manager_config_file.txt"

def load_config(filename):
    settings = {}
    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                settings[key.strip()] = value.strip()
    return settings

settings = load_config(CONFIG_FILE)

#  Function to run another python script
def run_script(script_name):
    if not os.path.exists(script_name):
        messagebox.showerror(
            "File not found",
            f"The file:\n{script_name}\nwas not found.\n\n"
            "👉 Please check that the path in manager_config_file.txt is correct,\n"
            "or move the file to the expected location."
        )
        return 
    # sys.executable ensures you use the same Python interpreter
    subprocess.Popen([sys.executable, script_name])

def run_shortcut(shortcut_path):
    """Run a Windows shortcut or bash/batch file"""
    # If it's a .lnk shortcut or a .bat file
    shortcut_path = os.path.normpath(shortcut_path)
    if not os.path.exists(shortcut_path):
        messagebox.showerror(
            "File not found",
            f"The file:\n{shortcut_path}\nwas not found.\n\n"
            "👉 Please check that the path in manager_config_file.txt is correct,\n"
            "or move the file to the expected location."
        )
        return 
    if shortcut_path.endswith(".lnk") or shortcut_path.endswith(".bat"):
        os.startfile(shortcut_path)
    else:
        # For bash .sh files (needs WSL or Git Bash installed)
        subprocess.Popen(["bash", shortcut_path], shell=True)

# Create the main window
root = tk.Tk()
root.title("Script Launcher")
root.geometry("300x200")

# Add buttons
frame = tk.Frame(root)
frame.pack(pady=20)
if "a1111LauncherScript" in settings:
    btn1 = tk.Button(frame, text="Run A1111", command=lambda: run_shortcut(settings["a1111LauncherScript"]))
    btn1.pack(pady=5, fill="x")
    
if "jsonGeneratorScript" in settings:
    btn2 = tk.Button(frame, text="Run Prompts helper UI", command=lambda: run_script(settings["jsonGeneratorScript"]))
    btn2.pack(pady=5, fill="x")

if "imageGeneratorScript" in settings:
    btn3 = tk.Button(frame, text="Generate Images from prompts.json", command=lambda: run_script(settings["imageGeneratorScript"]))
    btn3.pack(pady=5, fill="x")


# Run the GUI loop
root.mainloop()
