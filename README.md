# 🧠 AI-Opis-Zdjęć

Webowa aplikacja do automatycznego opisywania i wyszukiwania zdjęć przy użyciu sztucznej inteligencji.

## ✨ Funkcje

- 📤 Wgrywanie własnych zdjęć
- 🧠 Automatyczne opisy tworzone przez model AI (BLIP)
- 🔍 Wyszukiwanie zdjęć po opisie (semantyczne, nie dosłowne!)
- 🖼️ Galeria z miniaturkami
- 🌐 Interfejs webowy zbudowany we Flasku

## 🔧 Technologie

- Python 3.9+
- Flask
- PostgreSQL + psycopg2
- BLIP (Salesforce)
- Sentence-Transformers
- HuggingFace Transformers
- HTML/CSS

## 🚀 Jak uruchomić

1. **Sklonuj repozytorium (lub pobierz ZIP):**


git clone https://github.com/TWOJ-USER/ai-opis-zdjec.git
cd ai-opis-zdjec
Zainstaluj zależności:


pip install -r requirements.txt
Uruchom kontener PostgreSQL (jeśli używasz Dockera):


docker run --name baza-postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=haslo -e POSTGRES_DB=moja_baza -p 5432:5432 -d postgres
Uruchom aplikację:

python app.py
Wejdź w przeglądarkę:


http://127.0.0.1:5000