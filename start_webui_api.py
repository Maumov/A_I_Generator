import subprocess
import os
import sys

# CHANGE this to your actual Automatic1111 folder path
webui_folder = r"C:\Users\Mauricio\Documentos\stable-diffusion-webui"

def main():
    # Change working directory to the webui folder
    os.chdir(webui_folder)

    # Construct the command
    # Use sys.executable to call the same Python interpreter running this script
    cmd = [sys.executable, "launch.py", "--api"]

    print(f"Running command: {' '.join(cmd)} in {webui_folder}")
    try:
        # Run the process and wait for it to finish
        # shell=True can be avoided since we provide the full command as a list
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running launch.py: {e}")

    input("Press Enter to exit...")  # Keeps the window open after script ends

if __name__ == "__main__":
    main()
