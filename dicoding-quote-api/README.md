# 🧩 Data Handling Projects Portfolio (Python)

Proyek ini adalah koleksi *script* Python yang mendemonstrasikan kemampuan fundamental dalam *Data Science* dan pengembangan *backend*, meliputi koneksi *database*, operasi CRUD, pengambilan data dari API, dan pemrosesan *file* non-standar (Excel).

## 1. 📂 Proyek I: PostgreSQL CRUD & Data Management

Bagian ini berfokus pada interaksi penuh dengan *database* PostgreSQL.

### Teknologi
* **Database:** PostgreSQL
* **ORM/Koneksi:** SQLAlchemy, Psycopg2
* **Verifikasi Data:** Pandas

### Struktur File (Folder: CONNECTING-TO-POSTGRE)

| File | Fungsi | Operasi CRUD |
| :--- | :--- | :--- |
| `create_db.py` | Membuat *database* tujuan (`companydb`) sebagai langkah inisiasi. | **CREATE (Database)** |
| `main.py` | Mendefinisikan skema tabel `users` dan menyisipkan (*INSERT*) data. | **CREATE (Table) & INSERT** |
| `update_data.py` | Memperbarui (*UPDATE*) data di tabel `users`. | **UPDATE** |
| `read_data.py` | Membaca (*SELECT*) semua data dari tabel `users` menggunakan Pandas. | **READ** |
| `delete_data.py` | (Opsional) Berisi logika untuk menghapus (*DELETE*) baris data. | **DELETE** |

### Prasyarat

* PostgreSQL Server harus berjalan di `localhost:5432`.
* Instalasi *library*: `pip install sqlalchemy psycopg2-binary pandas`

***

## 2. 🌐 Proyek II: Data Extraction & Format Handling

Bagian ini menunjukkan kemampuan mengambil data dari sumber eksternal (API) dan memproses *file* berformat lain (Excel).

### Teknologi
* **API:** Python `urllib.request` (built-in)
* **File Handling:** JSON, Pandas (untuk Excel)

### Struktur File (Folder: DICODING-QUOTE-API)

| File | Fungsi |
| :--- | :--- |
| `main.py` | Mengambil data JSON dari API Dicoding dan menyimpan hasilnya ke *file* `dicoding_quotes.json`. |

### Struktur File (Folder: EXTRACTING-OTHER-FORMAT)

| File | Fungsi |
| :--- | :--- |
| `main.py` | Memuat (*read*) data dari *file* Excel (`spreadsheets/customer_and_product.xlsx`) ke dalam **Pandas DataFrame** untuk diproses. |

### Prasyarat

* Instalasi *library* tambahan untuk *spreadsheet*: `pip install pandas openpyxl`

***

## ▶️ Cara Menjalankan Proyek

### A. Menjalankan Proyek PostgreSQL

1.  Pindah ke folder `CONNECTING-TO-POSTGRE`.
2.  Jalankan berurutan: `python create_db.py`, lalu `python main.py`.

### B. Menjalankan Proyek API Extraction

1.  Pindah ke folder `DICODING-QUOTE-API`.
2.  Jalankan: `python main.py` (akan menghasilkan file `dicoding_quotes.json`).

### C. Menjalankan Proyek Excel Extraction

1.  Pindah ke folder `EXTRACTING-OTHER-FORMAT`.
2.  Pastikan *file* Excel berada di *path* `spreadsheets/customer_and_product.xlsx`.
3.  Jalankan: `python main.py`

---