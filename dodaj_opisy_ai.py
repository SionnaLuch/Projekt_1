from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import psycopg2
import os

# Wczytaj model AI
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    use_safetensors=True
)

# Ścieżka do folderu ze zdjęciami
folder_path = os.path.join(os.getcwd(), "zestaw_zdjec")

# Połączenie z bazą PostgreSQL
conn = psycopg2.connect(
    dbname="projekt_1",
    user="admin",
    password="haslo123",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Pobierz zdjęcia z bazy
cur.execute("SELECT id, nazwa FROM zdjecia;")
zdjecia = cur.fetchall()

for zdj_id, nazwa in zdjecia:
    sciezka = os.path.join(folder_path, nazwa)
    if os.path.exists(sciezka):
        try:
            raw_image = Image.open(sciezka).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs)
            opis = processor.decode(out[0], skip_special_tokens=True)
            cur.execute("UPDATE zdjecia SET opis = %s WHERE id = %s;", (opis, zdj_id))
            print(f"✅ {nazwa}: {opis}")
        except Exception as e:
            print(f"⚠️ Błąd przy {nazwa}: {e}")
    else:
        print(f"❌ Nie znaleziono pliku: {nazwa}")

conn.commit()
cur.close()
conn.close()
print("🎉 Wszystkie opisy AI zostały zapisane do bazy.")