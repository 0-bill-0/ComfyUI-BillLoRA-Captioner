import os
import time

BILL_ASCII = r"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗ ██╗ ██╗     ██╗                                                ║
║   ██╔══██╗██║ ██║     ██║         ⚡ BILL'S CONCEPT ISOLATOR ⚡           ║
║   ██████╔╝██║ ██║     ██║                                                ║
║   ██╔══██╗██║ ██║     ██║         [ Powered by Gemma 4 & Ollama ]         ║
║   ██████╗ ██║ ██████╗ ██████╗                                            ║
║   ╚═════╝ ╚═╝ ╚═════╝ ╚═════╝        🚀 NEXT-GEN VISION ACTIVE            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

print(BILL_ASCII)
time.sleep(1.5) 

from .bill_lora_captioner import BillLoRACaptionNode

NODE_CLASS_MAPPINGS = {
    "BillLoRACaptionNode": BillLoRACaptionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BillLoRACaptionNode": "Bill's LoRA Detail Captioner (Gemma 4)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
