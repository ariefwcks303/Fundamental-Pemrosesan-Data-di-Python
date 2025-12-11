import pandas as pd
import json
import os 

# --- VARIABEL KONFIGURASI ---
JSON_INPUT_FILE = 'books_data_output.json'
CSV_OUTPUT_FILE = 'transformed_books_data.csv' 
EXCHANGE_RATE = 19500 # Ganti dengan kurs yang relevan (misal: 1 Pound = Rp19.500)
# -----------------------------

def load_data_from_json(file_path):
    """Membaca file JSON dan mengembalikannya sebagai Pandas DataFrame."""
    if not os.path.exists(file_path):
        print(f"🛑 ERROR: File JSON tidak ditemukan di: {file_path}")
        return pd.DataFrame()
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Data berhasil dimuat dari {file_path}. Jumlah item: {len(data)}")
        return pd.DataFrame(data)
    except Exception as e:
        print(f"🛑 ERROR saat memuat data JSON: {e}")
        return pd.DataFrame()


def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    print("▶️ Memulai proses transformasi data...")

    # Kolom Harga di JSON adalah 'Price (GBP)', sehingga kita gunakan nama kolom ini
    PRICE_COLUMN = 'Price (GBP)'
    
    # 1. Transformasi Price 
    # Kolom sudah berupa float, hanya perlu membuat kolom baru dan mengkonversi tipe
    if PRICE_COLUMN in data.columns:
        data['Price_in_pounds'] = data[PRICE_COLUMN].astype(float)
    else:
        print(f"⚠️ Peringatan: Kolom '{PRICE_COLUMN}' tidak ditemukan. Melewati transformasi harga.")
        return data

    # 2. Transformasi Rating (Mengubah string 'One', 'Two', dst. menjadi angka)
    rating_mapping = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    data['Rating'] = data['Rating'].replace(rating_mapping).astype('int8')
    
    # 3. Transformasi Mata Uang (Kurs ke Rupiah)
    data['Price_in_rupiah'] = (data['Price_in_pounds'] * exchange_rate).astype(int)
    
    # 4. Menghapus kolom redundan (Kolom harga asli)
    data = data.drop(columns=[PRICE_COLUMN])
    
    # 5. Transformasi Tipe Data (Memastikan tipe data String)
    data['Title'] = data['Title'].astype('string')
    if 'Availability' in data.columns:
        data['Availability'] = data['Availability'].astype('string')
    
    print("✅ Transformasi selesai.")
    return data


def save_data(df, file_path):
    """Menyimpan DataFrame ke file CSV."""
    if df.empty:
        print("🛑 ERROR: DataFrame kosong, tidak ada data yang disimpan.")
        return
        
    try:
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"✅ Data berhasil disimpan ke: {file_path}")
    except Exception as e:
        print(f"🛑 ERROR saat menyimpan CSV: {e}")


if __name__ == "__main__":
    
    # 1. LOAD: Muat data dari JSON
    df_raw = load_data_from_json(JSON_INPUT_FILE)
    
    if not df_raw.empty:
        # 2. TRANSFORM: Jalankan transformasi
        df_transformed = transform_data(df_raw, EXCHANGE_RATE)
        
        # 3. SAVE: Simpan hasil transformasi ke CSV
        save_data(df_transformed, CSV_OUTPUT_FILE)
    else:
        print("Proses dihentikan karena tidak ada data yang dimuat.")