import psycopg2
import os

# Połączenie z bazą danych PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="projekt_1",
    user="admin",
    password="haslo123"
)

cur = conn.cursor()

# Ścieżka do folderu ze zdjęciami (na biurku)
folder_path = os.path.expanduser("~/Desktop/zestaw_zdjec")

# Wgraj zdjęcia 1.jpg do 100.jpg
for i in range(1, 100):
    file_name = f"{i}.jpg"
    full_path = os.path.join(folder_path, file_name)

    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            obrazek = f.read()
            cur.execute("""
                INSERT INTO zdjecia (nazwa, obrazek)
                VALUES (%s, %s)
            """, (file_name, psycopg2.Binary(obrazek)))
            print(f"✅ Dodano: {file_name}")
    else:
        print(f"⚠️  Nie znaleziono pliku: {file_name}")

conn.commit()
cur.close()
conn.close()
print("✅ Wszystkie dane zostały zapisane.")
