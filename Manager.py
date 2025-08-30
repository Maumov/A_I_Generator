import tkinter as tk
import subprocess
import sys
import os

jsonGeneratorScript = "PromptGenerator.py"
imageGeneratorScript = "Generator.py"
a1111LauncherScript = r"C:\Users\Mauricio\Escritorio\AI\webui-user_READY.lnk"

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
btn1 = tk.Button(root, text="Init api", command=lambda: run_shortcut(f"{a1111LauncherScript}"))
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Generate", command=lambda: run_script(f"{jsonGeneratorScript}"))
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Run", command=lambda: run_script(f"{imageGeneratorScript}"))
btn3.pack(pady=10)



# Run the GUI loop
root.mainloop()
