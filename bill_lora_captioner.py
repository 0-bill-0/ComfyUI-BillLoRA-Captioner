import torch
import numpy as np
from PIL import Image
import io
import base64
import requests
import json
import os

class BillLoRACaptionNode:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"

    @classmethod
    def INPUT_TYPES(s):
        installed_models = BillLoRACaptionNode.get_ollama_models()
        
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (installed_models, ), 
                "excluded_details": ("STRING", {"multiline": True, "default": "man with grey hair and blue eyes"}), 
                "trigger_word": ("STRING", {"default": "Bill"}), 
            },
            "optional": {
                "filename": ("STRING", {"default": "image"}),
                "save_folder": ("STRING", {"default": "comfyui/output/captions"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "caption_image"
    CATEGORY = "BillNodes/Training"

    @staticmethod
    def get_ollama_models():
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                return models if models else ["gemma4"]
        except Exception as e:
            print(f"BillLoRA Error: Could not connect to Ollama. {e}")
        return ["gemma4"]

    def image_to_base64(self, image_tensor):
        i = 255. * image_tensor[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def caption_image(self, image, model, excluded_details, trigger_word, filename="image", save_folder="comfyui/output/captions"):
        img_b64 = self.image_to_base64(image)

        # --- THE GEMMA 4 OPTIMIZED MASTER PROMPT ---
        master_prompt = (
            f"You are an expert AI visual analyst specialized in cinematic photorealistic descriptions.\n\n"
            f"OBJECTIVE: Describe this image in verbose, high-fidelity detail. Focus on exact chromatic hues, "
            f"tactile textures, volumetric lighting, and environmental composition.\n\n"
            f"CONCEPT ISOLATION CONSTRAINT: The subject is defined as '{excluded_details}'. "
            f"You MUST NOT describe the physical traits of this subject. Do not mention their hair, eyes, skin, or age. "
            f"Instead, refer to the subject ONLY as the trigger word: '{trigger_word}'.\n\n"
            f"EXAMPLE: Instead of 'A man with grey hair and blue eyes wearing a red shirt', "
            f"write '{trigger_word} wearing a red shirt'.\n\n"
            f"Output the result as a single, fluid, cinematic paragraph. No lists. No bullets."
        )

        payload = {
            "model": model,
            "prompt": master_prompt,
            "images": [img_b64],
            "stream": False,
            "options": { "temperature": 0.3 }
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            final_caption = response.json().get("response", "").strip()
        except Exception as e:
            final_caption = f"Error: {str(e)}"

        if filename:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder, exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            file_path = os.path.join(save_folder, f"{base_name}.txt")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(final_caption)
            except Exception as e:
                print(f"❌ BillLoRA: Failed to save {file_path}. Error: {e}")

        return (final_caption,)
