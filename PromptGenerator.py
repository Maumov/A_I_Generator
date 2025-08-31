import json
import itertools
import random
import tkinter as tk
from itertools import product

# Define keyword sets

CONFIG_FILE = "promptConfig.txt"

def load_string_sets(filename):
    sets = []
    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                name, values = line.strip().split("=", 1)
                items = [s.strip() for s in values.split(",") if s.strip()]
                if items:
                    sets.append((name.strip(), items))
    return sets

string_sets = load_string_sets(CONFIG_FILE)

listboxes = []

def get_combinations():
    selections = []
    for idx, (set_name, items) in enumerate(string_sets):
        selected_items = [items[i] for i in listboxes[idx].curselection()]
        if selected_items:
            selections.append(selected_items)

    if len(selections) == len(string_sets):
        combos = list(product(*selections))
        output_box.delete("1.0", tk.END)
        for combo in combos:
            output_box.insert(tk.END, " ".join(combo) + "\n")
    else:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "⚠️ Select at least one item from each list.\n")

##faceposes = [
##  #  "smiling",
##  #  "subtle smile",
##    "neutral expression",
##  #  "soft smile",
##  #  "slight smirk",
##  # "serious expression",
##  #  "playful expression",
##  #  "relaxed face",
##    ]
##
##poses = [
##  #  "selfie, looking at camera",
##  #  "front view, facing camera, looking at viewer",
##  #  "side profile, profile view, looking to the left",
##  #  "three-quarter view, looking slightly to the left",
##  #  "low angle view, looking down at camera",
##  #  "from above, looking up",
##    "looking back,over shoulder, turned head, looking at viewer, back view, head turned, profile with gaze at viewer"
##
##  #  "mirror selfie, holding phone",
##  #  "candid selfie, looking away",
##  #  "bathroom mirror selfie",
##  #  "outdoor selfie, holding drink",
##]
##
##clothing = [
##  #  "casual t-shirt and jeans",
##  #  "gym outfit, sports bra and leggings",
##  #  "elegant dress, evening style",
##  #  "street style outfit, jacket and sneakers",
##  #  "home outfit, comfy hoodie",
##  # "tank top and yoga pants",
##    "pajamas",
##]
##
##backgrounds = [
##    "indoors, cozy lighting",
##  # "modern bathroom",
##  #  "sunny outdoor street",
##  # "bedroom with soft lighting",
##  #  "gym interior",
##]
##
##lighting = [
##  #  "natural daylight",
##  #  "warm evening light",
##    "soft diffuse light",
##  #  "harsh overhead light",
##  #  "golden hour sunlight",
##]
# Global settings
settings = {
    "steps": 28,
    "width": 768,
    "height": 1024,
    "sampler_name": "DPM++ 2M",
    "scheduler":"Karras",
    "batch_size": 4,
    "n_iter": 1,
    "cfg_scale": 7.0,
    "seed": 10,    
}
# high res fix settings
highresSettings = {
  "enable_hr": True,             # 🔥 enables hires fix
  "hr_upscaler": "Latent",       # options: Latent, ESRGAN_4x, R-ESRGAN 4x+
  "hr_scale": 2,                 # upscale factor (2x, 1.5x, etc.)
  "hr_second_pass_steps": 10,    # extra steps on the upscaled image
  "denoising_strength": 0.4,     # how much it changes details in hires pass
}
# Negative prompt
consistency = "different face,changing identity, unrecognizable face, face distortion, face swap"
negative = "blurry, out of frame, extra arms, extra legs, extra fingers, deformed, distorted, ugly, distorted face, bad quality, low quality, lowres, watermark, text"
negativepromt = f"{consistency}, {negative}"
# Generate combinations (all or random sample)
combinations = list(itertools.product(faceposes, poses, clothing, backgrounds, lighting))

# Optional: shuffle and limit number of samples
#random.shuffle(combinations)
#max_images = 5  # <-- change this for dataset size
#combinations = combinations[:max_images]

#Character features
#hair = "brunette"
hair = "long brown hair, straight hair, natural hairstyle"

face = "oval face, soft chin, defined jawline, straight nose"

#age = "23 years old"
age = "early 20s woman" 

#eyes = "brown eyes"
eyes = "hazel eyes" 

#skin = "golden skin"
skin = "light skin tone"

#promt setup
model = f"athena_woman, {age}, no makeup ,{face}, {eyes}, {hair}, fit body, huge breasts, {skin}, cleavage"
stability = "symmetrical face, consistent face,same person, photorealistic portrait of the same woman, character consistency"
realistic = "photorealistic, realistic skin, natural face, candid , homemade"


startprompt =  f"{model}, {stability}, {realistic} "
endprompt =  "<lora:RealVisXL:0.8>, <lora:RealMirrorSelfieXL:0.7>"   

#json setup
def GeneratePromptsFile
    requests = []
    for combo in combinations:
        prompt = f"{startprompt}, {combo[0]}, {combo[1]}, {combo[2]}, {combo[3]}, {combo[4]}, {endprompt}"
        req = {
            "prompt": prompt,
            "negative_prompt": negativepromt,
            **settings
        }
        requests.append(req)

    output = {"prompts": requests}

    # Save JSON file
    with open("prompts.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"✅ prompts.json generated with {len(requests)} requests.")


root = tk.Tk()
root.title("Title")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a listbox for each named set
for idx, (set_name, items) in enumerate(string_sets):
    label = tk.Label(frame, text=set_name, font=("Arial", 10, "bold"))
    label.grid(row=0, column=idx, padx=5, pady=5)

    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
    for item in items:
        listbox.insert(tk.END, item)
    listbox.grid(row=1, column=idx, padx=5, pady=5)
    listboxes.append(listbox)

btn = tk.Button(root, text="Generate Combinations", command=get_combinations)
btn.pack(pady=10)

output_box = tk.Text(root, wrap="word", height=15)
output_box.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
