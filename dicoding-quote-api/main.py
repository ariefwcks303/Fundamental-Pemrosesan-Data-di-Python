import urllib.request
import json
import os # Import library os untuk path

# 1. Ambil data dari API
url = "https://quote-api.dicoding.dev/list"
response = urllib.request.urlopen(url)
result = response.read().decode()

# Ubah string JSON menjadi objek Python (list/dict)
data = json.loads(result)

# 2. Definisikan nama file output
output_file_name = "dicoding_quotes.json"

# 3. Simpan objek Python ke file JSON
try:
    with open(output_file_name, 'w', encoding='utf-8') as f:
        # Menggunakan json.dump untuk menulis objek ke file
        # indent=4 agar file JSON mudah dibaca (pretty print)
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Cetak konfirmasi keberhasilan
    print(f"Data JSON berhasil diekstraksi dan disimpan ke '{output_file_name}'")
    print(f"File '{output_file_name}' kini berada di folder proyek Anda.")

except Exception as e:
    print(f"Terjadi kesalahan saat menyimpan file: {e}")