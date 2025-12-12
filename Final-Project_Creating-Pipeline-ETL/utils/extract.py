import requests
from bs4 import BeautifulSoup
import time
import re # Untuk pembersihan teks

BASE_URL = "https://fashion-studio.dicoding.dev"
MAX_PAGES = 50
MAX_DATA = 1000

headers = { # <-- PASTIKAN headers ADA DI SINI
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_data() -> list:
    """Mengambil data produk dari seluruh halaman website."""
    
    all_products = []
    
    print("--- Memulai Ekstraksi Data (Scraping) ---")
    
    # Header untuk simulasi browser agar tidak mudah diblokir
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, MAX_PAGES + 1):
        if len(all_products) >= MAX_DATA:
            break
            
        #url = f"{BASE_URL}?page={page}"
        # --- PERBAIKAN URL DI SINI ---
        if page == 1:
            # Halaman 1 harus https://fashion-studio.dicoding.dev/
            url = BASE_URL + "/"
        else:
            # Halaman 2 dan seterusnya harus https://fashion-studio.dicoding.dev/pageN
            url = f"{BASE_URL}/page{page}"
        # --- AKHIR PERBAIKAN URL ---
        
        print(f"Mengambil data dari halaman {page} ({url})...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari semua elemen produk
            product_cards = soup.find_all('div', class_='product-details')
            
            # --- LOGIKA PENGHENTIAN PERBAIKAN ---
            if not product_cards:
                print(f"Halaman {page} kosong, mengasumsikan akhir data. Menghentikan loop.")
                break # <-- Hanya berhenti jika halaman kosong!
            # --- AKHIR LOGIKA PENGHENTIAN ---

            for card in product_cards:
                if len(all_products) >= MAX_DATA:
                    break
                    
                # 1. Title (H3)
                title = card.find('h3', class_='product-title').text.strip()
                
                # 2. Price (span.price di dalam div.price-container)
                price_container = card.find('div', class_='price-container')
                # Asumsi price_str adalah "$100.00"
                price_str = price_container.find('span', class_='price').text.strip() if price_container and price_container.find('span', class_='price') else "$0.00"

                # 3, 4, 5, 6. Details (Tag P dengan style tertentu)
                # Mencari semua tag <p> yang berisi detail produk
                p_details = card.find_all('p', style=lambda value: value and 'font-size' in value)
                
                # Kita akan menyimpan teks mentah dan membersihkannya di tahap Transformasi
                rating_raw = p_details[0].text.strip() if len(p_details) > 0 else "N/A"
                colors_raw = p_details[1].text.strip() if len(p_details) > 1 else "N/A"
                size_raw = p_details[2].text.strip() if len(p_details) > 2 else "N/A"
                gender_raw = p_details[3].text.strip() if len(p_details) > 3 else "N/A"

                all_products.append({
                    "Title": title,
                    "Price": price_str,
                    "Rating_Raw": rating_raw, 
                    "Colors_Raw": colors_raw,
                    "Size_Raw": size_raw,
                    "Gender_Raw": gender_raw
                })

            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil halaman {page}. Menghentikan ekstraksi: {e}")
            break

    print(f"--- Selesai Ekstraksi: {len(all_products)} data terkumpul. ---")
    return all_products