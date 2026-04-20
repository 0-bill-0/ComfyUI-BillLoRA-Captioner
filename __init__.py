import os
import time
import sys

# --- Visual Configuration ---
BILL_ASCII = r"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   ██████╗ ██╗ ██╗     ██╗    Bill's Concept Isolator                            ║
║   ██╔══██╗██║ ██║     ██║                                                      ║
║   ██████╔╝██║ ██║     ██║                                                      ║
║   ██╔══██╗██║ ██║     ██║                                                      ║
║   ██████╗ ██║ ██████╗ ██████╗                                                  ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

def run_startup_animation():
    # 1. Print the clean professional banner
    print(BILL_ASCII)
    
    # 2. Define the scrolling text
    scroll_text = " Bill! Bill! Bill! Bill! Bill! Bill! Bill! Bill! "
    full_scroll = scroll_text + scroll_text 
    
    # 3. The Animation Loop
    for i in range(len(scroll_text)):
        frame = full_scroll[i : i + len(scroll_text)]
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        time.sleep(0.06) 
        
    # 4. Move to the next line so ComfyUI logs start fresh
    print() 

# Execute the animation
run_startup_animation()

# --- Node Registration ---
from .bill_lora_captioner import BillLoRACaptionNode

NODE_CLASS_MAPPINGS = {
    "BillLoRACaptionNode": BillLoRACaptionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BillLoRACaptionNode": "Bill's LoRA Detail Captioner (Gemma 4)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
