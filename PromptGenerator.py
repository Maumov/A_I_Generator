import tkinter as tk
from itertools import product
import csv
import json

STRINGS_FILE = "prompt_strings.txt" # CSV-style: Name="opt1","opt2","opt, with comma"  
SETTINGS_FILE = "prompt_settings.txt" # key=value lines (supports ints/floats/strings) 
OUTPUT_FILE = "prompts.json"

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

    settings_copy = extra_settings.copy()
    prompts_list = []

    for combo in current_combos:
        prompt_obj = {"prompt":",".join(combo)}
        prompt_obj.update(settings_copy)
        prompts_list.append(prompt_obj)
        
    output_data = {"prompts": prompts_list}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    output_box.insert(tk.END, f"\n✅ Saved {len(prompts_list)} prompts with settings to {OUTPUT_FILE}\n")

def refresh_settings():
    global extra_settings
    extra_settings = load_settings(SETTINGS_FILE)
    output_box.insert(tk.END, "\n🔄 Settings reloaded from settings.txt\n")

# --- GUI Setup ---
root = tk.Tk()
root.title("Multi-List String Selector with Settings")
root.geometry("1250x750")

# Create a frame for the category selection
#category_frame = tk.Frame(root)
#category_frame.pack(padx=10, pady=10, fill="both", expand=True)

##listboxes.clear()
##max_columns = 3  # number of columns before wrapping to next row
##
##for i, (set_name, items) in enumerate(string_sets):
##    row = i // max_columns
##    col = i % max_columns
##
##    group = tk.Frame(category_frame, borderwidth=2, relief="groove")
##    group.grid(row=row, column=col, padx=8, pady=8, sticky="n")
##
##    label = tk.Label(group, text=set_name, font=("Arial", 10, "bold"))
##    label.pack(padx=6, pady=(6, 4))
##
##    lb = tk.Listbox(group, selectmode=tk.MULTIPLE, height=8, exportselection=False)
##    for item in items:
##        lb.insert(tk.END, item)
##    lb.pack(padx=6, pady=(0, 6), fill="both", expand=True)
##    listboxes.append(lb)
##

# Category grid frame (first 7 in top row, rest in second row)
category_frame = tk.Frame(root)
category_frame.pack(padx=10, pady=10, fill="both", expand=True)

listboxes.clear()
FIRST_ROW_COUNT = 7  # <-- change this to how many items you want in the first row

for i, (set_name, items) in enumerate(string_sets):
    if i < FIRST_ROW_COUNT:
        row = 0
        col = i
    else:
        row = 1
        col = i - FIRST_ROW_COUNT

    group = tk.Frame(category_frame, borderwidth=2, relief="groove")
    group.grid(row=row, column=col, padx=8, pady=8, sticky="n")

    label = tk.Label(group, text=set_name, font=("Arial", 10, "bold"))
    label.pack(padx=6, pady=(6, 4))

    lb = tk.Listbox(group, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    for item in items:
        lb.insert(tk.END, item)
    lb.pack(padx=6, pady=(0, 6), fill="both", expand=True)
    listboxes.append(lb)

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
