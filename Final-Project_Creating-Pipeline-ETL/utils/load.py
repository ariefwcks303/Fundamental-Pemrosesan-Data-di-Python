# utils/load.py
import pandas as pd
from sqlalchemy import create_engine

def load_data(transformed_data: pd.DataFrame, file_path: str) -> None:
    """Menyimpan data yang telah ditransformasi ke berkas CSV."""
    
    print(f"--- Memulai Loading Data ke {file_path} ---")
    
    try:
        # Simpan DataFrame ke CSV tanpa indeks
        transformed_data.to_csv(file_path, index=False)
        print(f"Berhasil menyimpan {len(transformed_data)} baris data ke {file_path}.")
    except Exception as e:
        print(f"Gagal menyimpan data ke CSV: {e}")