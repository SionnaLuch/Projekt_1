import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import os

# Załaduj model do embeddingów (MiniLM - szybki i dobry)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Funkcja do przeliczenia tekstu na wektor
def embed(text):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        model_output = model(**encoded)
    return F.normalize(model_output.last_hidden_state[:, 0, :], p=2, dim=1)

# Połącz się z bazą
conn = psycopg2.connect(
    dbname="projekt_1",
    user="admin",
    password="haslo123",
    host="localhost",
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT nazwa, opis FROM zdjecia WHERE opis IS NOT NULL;")
rows = cur.fetchall()
print(f"📄 Załadowano {len(rows)} opisów z bazy.")

# Wczytaj wszystkie opisy + zdjęcia
zdjecia = []
embedings = []

for nazwa, opis in rows:
    zdjecia.append((nazwa, opis))
    vec = embed(opis)
    embedings.append(vec)

# Pobierz zapytanie użytkownika
query = input("Wpisz, co chcesz znaleźć (np. kobieta z niebieskimi oczami): ")
query_vec = embed(query)

# Oblicz podobieństwo kosinusowe
similarities = [F.cosine_similarity(query_vec, e)[0].item() for e in embedings]

# Posortuj i pokaż 5 najlepszych
wyniki = sorted(zip(similarities, zdjecia), reverse=True)[:5]

print("\n🔍 Najbardziej pasujące zdjęcia:\n")
for sim, (nazwa, opis) in wyniki:
    print(f"📸 {nazwa} ({sim:.2f})\n📝 {opis}\n")