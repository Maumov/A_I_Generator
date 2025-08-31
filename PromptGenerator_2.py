import tkinter as tk
from itertools import product
import csv
import json

STRINGS_FILE = "prompt_config.txt"
SETTINGS_FILE = "prompt_settings.txt"
OUTPUT_FILE = "new_prompts2.json"

# --- Load named sets of strings from CSV-style txt ---
def load_string_sets(filename):
    sets = []
    with open(filename, "r", newline="") as f:
        for line in f:
            if "=" in line:
                name, values = line.split("=", 1)
                name = name.strip()
                reader = csv.reader([values.strip()], skipinitialspace=True)
                items = next(reader)
                items = [s.strip() for s in items if s.strip()]
                if items:
                    sets.append((name, items))
    return sets

# --- Load additional settings from txt ---
def load_settings(filename):
    settings = {}
    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                value = value.strip()
                # Try to convert to int or float, otherwise leave as string
                if value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                settings[key.strip()] = value
    return settings

string_sets = load_string_sets(STRINGS_FILE)
extra_settings = load_settings(SETTINGS_FILE)

# --- UI Functions ---
listboxes = []
current_combos = []

def get_combinations():
    global current_combos
    selections = []
    for idx, (set_name, items) in enumerate(string_sets):
        selected_items = [items[i] for i in listboxes[idx].curselection()]
        if selected_items:
            selections.append(selected_items)

    if len(selections) == len(string_sets):
        current_combos = list(product(*selections))
        output_box.delete("1.0", tk.END)
        for combo in current_combos:
            output_box.insert(tk.END, ",".join(combo) + "\n")
    else:
        current_combos = []
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "⚠️ Select at least one item from each list.\n")

def save_to_json():
    if not current_combos:
        output_box.insert(tk.END, "\n⚠️ No combinations to save. Generate first.\n")
        return

    prompts = [{"prompt": ",".join(combo)} for combo in current_combos]

    output_data = {"prompts": prompts}
    # Merge extra settings into JSON root
    output_data.update(extra_settings)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    output_box.insert(tk.END, f"\n✅ Saved {len(prompts)} prompts with settings to {OUTPUT_FILE}\n")

def refresh_settings():
    global extra_settings
    extra_settings = load_settings(SETTINGS_FILE)
    output_box.insert(tk.END, "\n🔄 Settings reloaded from settings.txt\n")

# --- GUI Setup ---
root = tk.Tk()
root.title("Multi-List String Selector with Settings")
root.geometry("750x550")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

for idx, (set_name, items) in enumerate(string_sets):
    label = tk.Label(frame, text=set_name, font=("Arial", 10, "bold"))
    label.grid(row=0, column=idx, padx=5, pady=5)

    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
    for item in items:
        listbox.insert(tk.END, item)
    listbox.grid(row=1, column=idx, padx=5, pady=5)
    listboxes.append(listbox)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_gen = tk.Button(btn_frame, text="Generate Combinations", command=get_combinations)
btn_gen.grid(row=0, column=0, padx=10)

btn_save = tk.Button(btn_frame, text="Save to JSON", command=save_to_json)
btn_save.grid(row=0, column=1, padx=10)

btn_refresh = tk.Button(btn_frame, text="Refresh Settings", command=refresh_settings)
btn_refresh.grid(row=0, column=2, padx=10)

output_box = tk.Text(root, wrap="word", height=15)
output_box.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
