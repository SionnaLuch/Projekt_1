from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Ścieżka do zdjęcia
image_path = "/Users/sionnapoleszuk/Desktop/zestaw_zdjec/1.jpg"

# Wczytaj model i procesor z Hugging Face
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base", use_fast=False
)
# Wczytaj obrazek
raw_image = Image.open(image_path).convert('RGB')

# Przetwórz obrazek i wygeneruj opis
inputs = processor(raw_image, return_tensors="pt")
output = model.generate(**inputs)
description = processor.decode(output[0], skip_special_tokens=True)

print(f"📝 Opis zdjęcia: {description}")