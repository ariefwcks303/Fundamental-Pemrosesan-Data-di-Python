# read_data.py

import pandas as pd
from sqlalchemy import create_engine

# Pastikan koneksi ke database yang benar ('companydb')
engine = create_engine('postgresql+psycopg2://postgres:000000@localhost:5432/companydb')

# --- PERBAIKAN PENTING DI SINI ---
# Ganti 'nama_tabel_anda' menjadi 'users'
select_query = "SELECT * FROM users;"

try:
    # Menggunakan Pandas untuk menjalankan query dan memuat hasilnya ke DataFrame
    df = pd.read_sql(select_query, engine)
    
    print("\n--- Hasil Data dari Tabel Users ---")
    print(df)
    print("----------------------------------")
    
except Exception as e:
    print(f"Terjadi kesalahan saat mengambil data: {e}")