# 🚀 Python PostgreSQL CRUD Project (SQLAlchemy + Psycopg2 + Pandas)

Proyek ini mendemonstrasikan cara membuat, membaca, memperbarui, dan menghapus (**CRUD**) data dalam *database* **PostgreSQL** menggunakan Python. Proyek ini memanfaatkan *library* **SQLAlchemy** (untuk mendefinisikan skema tabel secara *Pythonic*) dan **Psycopg2** sebagai *driver* koneksi.

### 📋 Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python
* **Database:** PostgreSQL
* **ORM/Koneksi:** SQLAlchemy
* **Driver Database:** Psycopg2
* **Verifikasi Data:** Pandas (untuk pembacaan data)

### ⚙️ Struktur Proyek

| File | Fungsi Utama | Operasi CRUD |
| :--- | :--- | :--- |
| `create_db.py` | Menggunakan koneksi *superuser* untuk membuat *database* tujuan (`companydb`). | **CREATE (Database)** |
| `main.py` | Mendefinisikan skema tabel `users` dan menyisipkan (*INSERT*) data awal. | **CREATE (Table) & INSERT** |
| `update_data.py` | Memperbarui (*UPDATE*) kolom `first_name` untuk baris dengan ID tertentu. | **UPDATE** |
| `read_data.py` | Membaca (*SELECT*) semua data dari tabel `users` dan menampilkannya dengan Pandas. | **READ** |
| `delete_data.py` | (Opsional) Berisi logika untuk menghapus (*DELETE*) baris data. | **DELETE** |

### 🔑 Prasyarat

Pastikan Anda memiliki hal-hal berikut sebelum menjalankan *script*:

1.  **PostgreSQL Server:** Server harus berjalan di `localhost:5432`.
2.  **Kredensial Latihan:** Kredensial yang digunakan dalam kode (untuk tujuan latihan): **User:** `postgres` | **Password:** `000000`.

### 📦 Instalasi Library

Semua *script* dalam proyek ini memerlukan *library* berikut. Instal dengan perintah:

```bash
pip install sqlalchemy psycopg2-binary pandas