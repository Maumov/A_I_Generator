import tkinter as tk
import subprocess
import sys
import os

jsonGeneratorScript = "PromptGenerator.py"
imageGeneratorScript = "Generator.py"
a1111LauncherScript = r"C:\Users\Mauricio\Escritorio\AI\webui-user_READY.lnk"

CONFIG_FILE = "config.txt"

def load_config(filename):
    settings = {}
    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                settings[key.strip()] = value.strip()
    return settings

settings = load_config(CONFIG_FILE)

# Function to run another python script
def run_script(script_name):
    # sys.executable ensures you use the same Python interpreter
    subprocess.Popen([sys.executable, script_name])

def run_shortcut(shortcut_path):
    """Run a Windows shortcut or bash/batch file"""
    # If it's a .lnk shortcut or a .bat file
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

if "script1" in settings:
    btn1 = tk.Button(frame, text="Run Script 1", command=lambda: run_python(settings["script1"]))
    btn1.pack(pady=5, fill="x")

if "script2" in settings:
    btn2 = tk.Button(frame, text="Run Script 2", command=lambda: run_python(settings["script2"]))
    btn2.pack(pady=5, fill="x")

if "shortcut" in settings:
    btn3 = tk.Button(frame, text="Run Shortcut", command=lambda: run_shortcut(settings["shortcut"]))
    btn3.pack(pady=5, fill="x")



# Run the GUI loop
root.mainloop()
