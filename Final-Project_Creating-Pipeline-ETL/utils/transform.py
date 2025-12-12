# utils/transform.py
import pandas as pd
import numpy as np
import re

EXCHANGE_RATE = 16000 # Asumsi nilai tukar USD/IDR

def convert_price(price_str):
    """Fungsi pembantu untuk konversi harga dari $ ke IDR."""
    try:
        # Hapus simbol '$'
        usd_price = float(price_str.replace('$', '').strip())
        return usd_price * EXCHANGE_RATE
    except:
        return np.nan 

def clean_rating(rating_raw):
    """Fungsi pembantu untuk membersihkan string Rating dan menghapus invalid."""
    # Hapus baris yang mengandung 'Invalid Rating'
    if 'Invalid Rating' in rating_raw or 'N/A' in rating_raw:
        return np.nan
    
    # Coba ekstrak nilai rating dari teks (misal: "Rating: ⭐️ 4.5 / 5")
    # Cari pola angka atau angka desimal
    match = re.search(r'(\d\.\d|\d)', rating_raw)
    if match:
        try:
            return float(match.group(1))
        except:
            return np.nan
    return np.nan

# --- FUNGSI BARU UNTUK MEMBANTU CLEANING KOLOM DETAIL ---
def clean_detail_columns(df):
    """Membersihkan kolom detail mentah."""

    # Kolom 'Colors' (Perbaikan Kegagalan #4)
    def clean_colors(x):
        x_str = str(x).strip()
        # Perbaikan Kegagalan #3: Pastikan N/A, string kosong, atau string 'Colors' saja menjadi NaN
        if x_str.lower() in ('n/a', 'colors') or not x_str:
            return np.nan
        
        # Ekstrak angka, jika ada. Misal: "5 Colors" -> "5"
        # Perbaikan Kegagalan #4: Memastikan angka diekstrak dengan benar
        match = re.search(r'^(\d+)', x_str)
        if match:
             return match.group(1) # Akan mengembalikan string '5'
        
        # Jika tidak ada angka (misal hanya "Red" atau "Blue")
        return x_str.replace('Colors', '').strip()

    # Kolom 'Size' dan 'Gender' (Perbaikan Kegagalan #3)
    def clean_generic(x, prefix):
        x_str = str(x).strip()
        # Perbaikan Kegagalan #3: Pastikan N/A atau string kosong menjadi NaN
        # Kita juga harus menangani kasus "Size: M" menjadi "M" dengan mengganti prefix
        if x_str.lower() == 'n/a' or not x_str or x_str == prefix.strip():
            return np.nan 
        
        # Hapus prefix yang sudah kita tahu ada di Raw Data (misalnya 'Size:' atau 'Gender:')
        return x_str.replace(prefix, '').strip()

    # Panggil fungsi pembersihan pada DataFrame
    df['Colors'] = df['Colors_Raw'].apply(clean_colors)
    df['Size'] = df['Size_Raw'].apply(lambda x: clean_generic(x, 'Size:'))
    df['Gender'] = df['Gender_Raw'].apply(lambda x: clean_generic(x, 'Gender:'))
    
    df.drop(columns=['Colors_Raw', 'Size_Raw', 'Gender_Raw'], inplace=True)
    return df
# --- AKHIR FUNGSI BARU ---


def transform_data(raw_data: list) -> pd.DataFrame:
    """Membersihkan, memvalidasi, dan mentransformasi data."""
    
    df = pd.DataFrame(raw_data)
    initial_count = len(df)
    print(f"--- Memulai Transformasi Data ({initial_count} baris awal) ---")

    # 1. Hapus Duplikat
    df.drop_duplicates(inplace=True)
    print(f"Baris setelah hapus duplikat: {len(df)}")
    
    # 2. Hapus Nilai Invalid pada Title ("Unknown Product")
    df = df[df['Title'] != 'Unknown Product']
    print(f"Baris setelah hapus 'Unknown Product': {len(df)}")

    # 3. Pembersihan dan Konversi Kolom
    
    # A. Price ($ ke IDR)
    df['Price (IDR)'] = df['Price'].apply(convert_price)
    df.drop('Price', axis=1, inplace=True)
    
    # B. Rating (membersihkan dan menghapus 'Invalid Rating')
    df['Rating'] = df['Rating_Raw'].apply(clean_rating)
    df.drop('Rating_Raw', axis=1, inplace=True)
    
    # C. Colors, Size, Gender (Gunakan fungsi yang sudah diperbaiki)
    df = clean_detail_columns(df) 
    
    # 4. Hapus Nilai Null (NaN) di semua kolom yang tersisa
    # Karena N/A, Invalid Price/Rating, dan Invalid Colors/Size/Gender kini menjadi np.nan,
    # baris-baris ini akan dihapus di sini (Perbaikan Kegagalan #3)
    df.dropna(inplace=True)
    print(f"Baris setelah hapus Null/Invalid: {len(df)}")

    # Atur ulang urutan kolom
    final_cols = ['Title', 'Price (IDR)', 'Rating', 'Colors', 'Size', 'Gender']
    df = df[final_cols]
    
    final_count = len(df)
    print(f"--- Selesai Transformasi: {final_count} baris akhir. ---")
    return df