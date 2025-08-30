import requests
import json
import base64
import os
from datetime import datetime

#response = requests.get("http://127.0.0.1:7860/sdapi/v1/samplers")
#for s in response.json():
#    print(s["name"])

# Load JSON
with open("prompts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

prompts = data.get("prompts", [])
if not prompts:
    print("No prompts found in the JSON file.")
    exit(1)

# Create a main batch folder with datetime
batch_folder = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(batch_folder, exist_ok=True)

for idx, prompt_data in enumerate(prompts, start=1):
    #prompt_folder = os.path.join(batch_folder, str(idx))
    #os.makedirs(prompt_folder, exist_ok=True)

    print(f"Generating images for prompt #{idx}: {prompt_data.get('prompt', '')}")

    # Send request to Automatic1111 API
    response = requests.post(
        url="http://127.0.0.1:7860/sdapi/v1/txt2img",
        json=prompt_data
    )

    if response.status_code != 200:
        print(f"Failed to generate images for prompt #{idx}: {response.text}")
        continue

    result = response.json()
    for i, img_base64 in enumerate(result.get("images", [])):
        image_bytes = base64.b64decode(img_base64)
        file_path = os.path.join(batch_folder, f"generated_{idx}_{i}.png")
        with open(file_path, "wb") as f:
            f.write(image_bytes)

    #print(f"Saved images for prompt #{idx} in folder: {prompt_folder}")

print(f"All done! Batch saved in folder: {batch_folder}")
