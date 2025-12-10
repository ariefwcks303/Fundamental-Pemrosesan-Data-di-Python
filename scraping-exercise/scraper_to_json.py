import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL dasar untuk scraping
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_books_data():
    """Mengambil data buku dari 50 halaman pertama dan mengembalikannya sebagai list of dictionaries."""
    all_books_data = []
    
    # Batasan halaman: 50 halaman
    for i in range(1, 51):
        url = BASE_URL.format(i)
        print(f"Scraping halaman: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Cek jika ada error HTTP
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari semua item buku pada halaman
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                title = book.h3.a['title']
                price_str = book.find('p', class_='price_color').text.replace('Â£', '').replace('£', '')
                rating_class = book.find('p', class_='star-rating')['class']
                
                # Mengambil rating dari class CSS (e.g., ['star-rating', 'Two'])
                rating = rating_class[1] if len(rating_class) > 1 else 'N/A'
                
                # Tambahkan data buku ke list
                all_books_data.append({
                    "Title": title,
                    "Price (GBP)": float(price_str),
                    "Rating": rating
                })
                
        except requests.exceptions.RequestException as e:
            print(f"Error saat mengakses {url}: {e}")
            continue
            
    return all_books_data

def save_to_json(data, filename="books_data_output.json"):
    """Menyimpan list data ke dalam file JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # json.dump digunakan untuk menulis list of dicts ke file.
            # indent=4 untuk format yang rapi.
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"\n=======================================================")
        print(f"✅ Scraping dan penyimpanan JSON berhasil!")
        print(f"Total {len(data)} data buku telah disimpan ke: {filename}")
        print(f"=======================================================")
        
    except IOError as e:
        print(f"❌ Terjadi kesalahan saat menulis file JSON: {e}")

# --- EKSEKUSI SKRIP ---
if __name__ == "__main__":
    
    # 1. Melakukan proses scraping
    books_data = scrape_books_data()
    
    if books_data:
        # 2. Menyimpan data yang terkumpul ke dalam file JSON
        save_to_json(books_data)
    else:
        print("Tidak ada data yang berhasil dikumpulkan.")