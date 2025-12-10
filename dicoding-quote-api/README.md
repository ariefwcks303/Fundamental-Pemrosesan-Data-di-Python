# 🌐 Dicoding Quote API Extractor (JSON Data Acquisition)

Proyek ini mendemonstrasikan proses dasar *Web Scraping* dan *API Extraction* menggunakan Python. Tujuannya adalah mengambil data kutipan (*quotes*) dalam format JSON dari *endpoint* Dicoding, memprosesnya, dan menyimpannya secara lokal.

### 📋 Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python
* **Library Utama:** `urllib.request` (built-in, untuk koneksi HTTP)
* **Library Pendukung:** `json` (built-in, untuk parsing dan penyimpanan JSON)

### ⚙️ Struktur Proyek

| File | Fungsi |
| :--- | :--- |
| `main.py` | Mengambil data dari API, mengubahnya menjadi objek Python, dan menyimpannya sebagai *file* `dicoding_quotes.json`. |
| `dicoding_quotes.json` | *File* *output* yang berisi data kutipan dalam format JSON terstruktur. |
| `requirements.txt` | Daftar *library* yang dibutuhkan (saat ini hanya mengandalkan *built-in* Python). |

### 🚀 Apa yang Dilakukan Script Ini? (`main.py`)

1.  Melakukan permintaan HTTP GET ke URL API (`https://quote-api.dicoding.dev/list`).
2.  Membaca respons (yang merupakan *string* JSON mentah).
3.  Mengubah *string* tersebut menjadi objek *list* atau *dictionary* Python (`json.loads`).
4.  Menulis objek tersebut kembali ke disk sebagai *file* `dicoding_quotes.json`, menggunakan *pretty-print* (`indent=4`) agar mudah dibaca.

### ▶️ Cara Menjalankan Proyek

#### 1. Eksekusi Script

Jalankan *script* dari Terminal/Command Prompt di folder proyek:

```bash
python main.py
