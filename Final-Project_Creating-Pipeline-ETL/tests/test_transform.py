# tests/test_transform.py

import pytest
import pandas as pd
import numpy as np
from utils.transform import transform_data, EXCHANGE_RATE

# Kita membuat fixture (data dummy) yang mencakup semua kasus edge
# untuk diuji oleh fungsi transform_data
@pytest.fixture
def sample_raw_data():
    """Menyediakan data mentah sampel untuk pengujian transformasi."""
    return [
        # Kasus 1: Data valid, harus sukses diubah
        {
            "Title": "Baju Kemeja", "Price": "$20.00", 
            "Rating_Raw": "Rating: ⭐️ 4.5 / 5", "Colors_Raw": "5 Colors", 
            "Size_Raw": "Size: L", "Gender_Raw": "Gender: Male"
        },
        # Kasus 2: Duplikat dari Kasus 1, harus dihapus
        {
            "Title": "Baju Kemeja", "Price": "$20.00", 
            "Rating_Raw": "Rating: ⭐️ 4.5 / 5", "Colors_Raw": "5 Colors", 
            "Size_Raw": "Size: L", "Gender_Raw": "Gender: Male"
        },
        # Kasus 3: Data Invalid (Title), harus dihapus
        {
            "Title": "Unknown Product", "Price": "$10.00", 
            "Rating_Raw": "Rating: ⭐️ 5.0 / 5", "Colors_Raw": "1 Colors", 
            "Size_Raw": "Size: S", "Gender_Raw": "Gender: Female"
        },
        # Kasus 4: Rating Invalid, harus dihapus (karena menjadi NaN lalu didrop)
        {
            "Title": "Celana Jeans", "Price": "$5.00", 
            "Rating_Raw": "Rating: ⭐️ Invalid Rating / 5", "Colors_Raw": "3 Colors", 
            "Size_Raw": "Size: M", "Gender_Raw": "Gender: Unisex"
        },
        # Kasus 5: Harga Invalid (format salah), harus dihapus
        {
            "Title": "Jaket Kulit", "Price": "Gratis", 
            "Rating_Raw": "Rating: ⭐️ 4.0 / 5", "Colors_Raw": "2 Colors", 
            "Size_Raw": "Size: XL", "Gender_Raw": "Gender: Male"
        },
        # Kasus 6: Nilai null (misal dari hasil scraping yang gagal), harus dihapus
        {
            "Title": "Topi Baseball", "Price": "$1.00", 
            "Rating_Raw": "Rating: ⭐️ 3.0 / 5", "Colors_Raw": "N/A", 
            "Size_Raw": "Size: M", "Gender_Raw": "Gender: Female"
        },
    ]

def test_transform_output_shape(sample_raw_data):
    """Memastikan jumlah baris data output sesuai setelah pembersihan."""
    df_clean = transform_data(sample_raw_data)
    # Ekspektasi: 6 baris awal - 1 Duplikat - 1 Invalid Title - 1 Invalid Rating - 1 Invalid Price - 0 Null (karena Invalid Price sudah menjadi NaN)
    # Total yang tersisa: Kasus 1 dan Kasus 6 (jika 'N/A' diubah menjadi teks kosong, tidak dihitung null)
    # Kita asumsikan 'N/A' di Kasus 6 menjadi NaN di tahap pembersihan, jadi harusnya hanya Kasus 1 yang lolos.
    # Namun, karena Kasus 6 memiliki 'N/A' di Colors_Raw yang akan diubah menjadi string kosong di transform, baris ini mungkin lolos.
    # Kita pastikan skenario terburuk: hanya baris yang BENAR-BENAR VALID yang lolos.
    # Valid (Kasus 1): 1 baris
    
    # Berdasarkan implementasi transform.py:
    # Kasus 1: Lolos
    # Kasus 2: Dihapus (Duplikat)
    # Kasus 3: Dihapus (Unknown Product)
    # Kasus 4: Dihapus (Invalid Rating -> NaN)
    # Kasus 5: Dihapus (Invalid Price -> NaN)
    # Kasus 6: Dihapus (N/A di Colors_Raw, tapi fungsi transform menghapus row jika ada NaN di kolom manapun) -> Akan dihapus
    
    # Jadi, seharusnya 1 baris yang lolos.
    assert len(df_clean) == 1

def test_transform_price_conversion(sample_raw_data):
    """Memastikan konversi harga ($ ke IDR) sudah benar."""
    df_clean = transform_data(sample_raw_data)
    
    # Harga di Kasus 1 adalah $20.00
    expected_price_idr = 20.00 * EXCHANGE_RATE
    
    # Ambil harga dari baris yang lolos (hanya satu baris, Kasus 1)
    actual_price_idr = df_clean['Price (IDR)'].iloc[0]
    
    # Menguji nilai
    assert actual_price_idr == expected_price_idr

def test_transform_rating_clean(sample_raw_data):
    """Memastikan rating yang valid dikonversi ke float dan yang invalid dihapus."""
    df_clean = transform_data(sample_raw_data)
    
    # Rating di Kasus 1 adalah 4.5
    expected_rating = 4.5
    actual_rating = df_clean['Rating'].iloc[0]
    
    # Menguji nilai
    assert actual_rating == expected_rating

def test_transform_column_cleaning(sample_raw_data):
    """Memastikan label teks (Colors, Size, Gender) sudah dihapus."""
    df_clean = transform_data(sample_raw_data)
    
    # Hanya menguji baris yang lolos (Kasus 1)
    row = df_clean.iloc[0]
    
    # Cek apakah label sudah hilang
    assert row['Colors'] == '5' # Karena 5 Colors -> 5
    assert row['Size'] == 'L'
    assert row['Gender'] == 'Male'
    
    # Cek apakah kolom yang sudah dibersihkan tidak mengandung nilai Null/NaN
    assert not row.isnull().any()