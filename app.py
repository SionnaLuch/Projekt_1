import os
import uuid
from flask import Flask, render_template, request, redirect
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import psycopg2
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer, util
semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

app = Flask(__name__, static_folder='static')

# Wczytanie modelu BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    use_safetensors=True,
    trust_remote_code=True
)

UPLOAD_FOLDER = os.path.join('static', 'zestaw_zdjec')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Konfiguracja bazy danych
def get_connection():
    return psycopg2.connect(
        dbname="projekt_1",
        user="admin",
        password="haslo123",
        host="localhost"
    )

# 🔎 Strona główna
@app.route("/", methods=["GET"])
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nazwa, opis FROM zdjecia ORDER BY id DESC;")
    wyniki = [{"nazwa": nazwa, "opis": opis} for nazwa, opis in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("index.html", wyniki=wyniki)

# 📤 Obsługa przesyłania zdjęcia
@app.route("/upload", methods=["POST"])
def upload():
    plik = request.files["plik"]
    if plik:
        nazwa_bezpieczna = secure_filename(plik.filename)
        unikalna_nazwa = str(uuid.uuid4()) + "_" + nazwa_bezpieczna
        sciezka = os.path.join(UPLOAD_FOLDER, unikalna_nazwa)
        plik.save(sciezka)

        # Generowanie opisu AI
        obrazek = Image.open(sciezka).convert("RGB")
        inputs = processor(images=obrazek, return_tensors="pt")
        out = model.generate(**inputs)
        opis = processor.decode(out[0], skip_special_tokens=True)

        # Zapis do bazy danych
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO zdjecia (nazwa, opis) VALUES (%s, %s);", (unikalna_nazwa, opis))
        conn.commit()
        cur.close()
        conn.close()

    return redirect("/")

# 🔍 Wyszukiwanie zdjęć po opisie
@app.route("/search", methods=["POST"])
def search():
    zapytanie = request.form["query"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nazwa, opis FROM zdjecia;")
    dane = cur.fetchall()
    cur.close()
    conn.close()

    # Wygeneruj embeddingi
    query_embedding = semantic_model.encode(zapytanie, convert_to_tensor=True)
    wyniki = []

    for nazwa, opis in dane:
        opis_embedding = semantic_model.encode(opis, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, opis_embedding).item()
        if similarity > 0.3:
            wyniki.append({
                "nazwa": nazwa,
                "opis": opis,
                "dopasowanie": f"{int(similarity * 100)}%"
            })

    wyniki = sorted(wyniki, key=lambda x: float(x["dopasowanie"].replace('%', '')), reverse=True)
    return render_template("index.html", wyniki=wyniki)
# 🚀 Uruchomienie aplikacji
if __name__ == "__main__":
    app.run(debug=True)
