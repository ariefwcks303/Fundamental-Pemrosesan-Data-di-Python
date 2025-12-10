from sqlalchemy import create_engine, Table, MetaData, update, text

# Pastikan semua library yang Anda butuhkan (termasuk Table, MetaData) sudah diimpor
# Jika Anda menjalankan ini di file terpisah, Anda perlu mendefinisikan ulang MetaData dan Table.

DATABASE_URL = 'postgresql+psycopg2://postgres:000000@localhost:5432/companydb'
engine = create_engine(DATABASE_URL)

metadata = MetaData()
# PENTING: Jika menggunakan Table dan MetaData, Anda harus memuat (merefleksikan) skema tabel dari database.
# Jika tidak, Anda akan mendapat UndefinedTable.
user_table = Table("users", metadata, autoload_with=engine) 

# --- Perintah UPDATE ---
def update_user_data(user_id, new_first_name):
    # 1. Definisikan perintah UPDATE
    update_stmt = (
        update(user_table)
        .where(user_table.c.id == user_id) # Target ID
        .values(first_name=new_first_name) # Nilai yang diubah
    )
    
    # 2. Jalankan perintah
    try:
        with engine.connect() as connection:
            result = connection.execute(update_stmt)
            connection.commit() 
            
            # Mendapatkan jumlah baris yang terpengaruh
            print(f"Update berhasil! {result.rowcount} baris diubah.")
            
    except Exception as e:
        print(f"Gagal memperbarui data: {e}")

# --- Eksekusi ---
update_user_data(user_id=1, new_first_name='Budi')

# --- Verifikasi ---
print("\nVerifikasi Data (Gunakan read_data.py untuk melihat hasilnya)")