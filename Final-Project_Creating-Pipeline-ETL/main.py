# main.py

from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_data
import pandas as pd

def run_etl_pipeline():
    """Menjalankan alur kerja Extract, Transform, Load."""
    
    OUTPUT_FILE = "products.csv"
    
    print("====================================")
    print("     MEMULAI PIPELINE ETL FASHION   ")
    print("====================================")
    
    # 1. Extract
    try:
        raw_data = extract_data()
    except Exception as e:
        print(f"\n[ERROR EKSRAKSI] Gagal: {e}")
        return

    # 2. Transform
    if raw_data:
        try:
            clean_df = transform_data(raw_data)
        except Exception as e:
            print(f"\n[ERROR TRANSFORMASI] Gagal: {e}")
            return
            
        # 3. Load
        if not clean_df.empty:
            try:
                load_data(clean_df, OUTPUT_FILE)
            except Exception as e:
                print(f"\n[ERROR LOADING] Gagal: {e}")
                return
        else:
            print("\n[INFO] Data bersih kosong setelah transformasi, loading dibatalkan.")
    else:
        print("\n[INFO] Data mentah kosong, pipeline dihentikan.")

    print("====================================")
    print("       PIPELINE ETL SELESAI         ")
    print("====================================")

if __name__ == "__main__":
    run_etl_pipeline()