# tests/test_load.py

import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from utils.load import load_data 

# Data dummy untuk di-load
@pytest.fixture
def sample_transformed_data():
    """Menyediakan data DataFrame yang sudah bersih untuk pengujian loading."""
    return pd.DataFrame({
        'Title': ['Product A', 'Product B'],
        'Price (IDR)': [320000, 800000],
        'Rating': [4.5, 3.8],
        'Colors': ['Red', 'Blue'],
        'Size': ['S', 'M'],
        'Gender': ['Male', 'Female']
    })

def test_load_to_csv_success(sample_transformed_data, tmp_path):
    """Menguji loading data ke file CSV lokal."""
    
    # Gunakan tmp_path dari pytest untuk direktori sementara
    output_file = tmp_path / "test_output.csv"
    
    # Jalankan fungsi loading
    load_data(sample_transformed_data, str(output_file))
    
    # 1. Cek apakah file berhasil dibuat
    assert os.path.exists(output_file)
    
    # 2. Cek apakah isi file CSV sesuai
    df_loaded = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(sample_transformed_data, df_loaded)

# --- Tambahan: Pengujian Simulasi Loading ke PostgreSQL ---
# Catatan: Untuk menguji ini, Anda harus menginstal sqlalchemy dan memodifikasi utils/load.py
# agar memiliki logika penyimpanan ke database.

@patch('utils.load.create_engine') 
def test_load_to_postgres_success(mock_create_engine, sample_transformed_data):
    """Menguji loading data secara simulasi ke database PostgreSQL."""
    
    # 1. Simulasikan Engine dan Koneksi Database
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    # 2. Jalankan fungsi loading (dengan path dummy)
    # Asumsi: Anda memodifikasi load_data untuk menerima engine atau URL database
    # Kita harus memanggil fungsi load_data_to_db yang baru
    
    # Di Sini, kita akan mem-mock method to_sql dari Pandas yang digunakan untuk menulis ke DB
    with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
        
        # Panggil load_data dengan asumsi load_data telah diperbarui untuk menangani DB
        # Jika Anda tidak mengubah load_data.py, test ini akan gagal/tidak relevan.
        # Jika load_data.py hanya menyimpan CSV, kita perlu fungsi load_to_db terpisah.
        
        # Kita panggil fungsi dummy yang memanggil to_sql untuk pengujian:
        sample_transformed_data.to_sql(
            'fashion_data', 
            con=mock_engine, 
            if_exists='replace', 
            index=False
        )

        # 3. Cek apakah to_sql dipanggil dengan parameter yang benar
        mock_to_sql.assert_called_once_with(
            'fashion_data', 
            con=mock_engine, 
            if_exists='replace', 
            index=False
        )

# Anda harus memodifikasi utils/load.py agar test database ini benar-benar berfungsi
# Misalnya, tambahkan fungsi baru:
# def load_data_to_db(df, db_url):
#     engine = create_engine(db_url)
#     df.to_sql('fashion_data', con=engine, if_exists='replace', index=False)