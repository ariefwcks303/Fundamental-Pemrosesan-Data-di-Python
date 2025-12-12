# tests/test_extract.py

import pytest
import requests
from unittest.mock import patch, Mock
from utils.extract import extract_data, BASE_URL, MAX_PAGES, MAX_DATA, headers # <--- Tambahkan , headers

# Data HTML dummy yang akan disimulasikan sebagai respons website
# Kita simulasikan 10 produk per halaman
MOCK_HTML_CONTENT = """
<div class="product-details">
    <h3 class="product-title">Produk Test A</h3>
    <div class="price-container"><span class="price">$10.00</span></div>
    <p style="font-size: 14px; color: #777;">Rating: ⭐️ 4.0 / 5</p>
    <p style="font-size: 14px; color: #777;">5 Colors</p>
    <p style="font-size: 14px; color: #777;">Size: S</p>
    <p style="font-size: 14px; color: #777;">Gender: Female</p>
</div>
<div class="product-details">
    <h3 class="product-title">Produk Test B</h3>
    <div class="price-container"><span class="price">$50.00</span></div>
    <p style="font-size: 14px; color: #777;">Rating: ⭐️ 3.5 / 5</p>
    <p style="font-size: 14px; color: #777;">2 Colors</p>
    <p style="font-size: 14px; color: #777;">Size: M</p>
    <p style="font-size: 14px; color: #777;">Gender: Male</p>
</div>
""" * 5 # Menggandakan 5 kali, jadi ada 10 produk per halaman

@patch('utils.extract.MAX_PAGES', 2)
@patch('requests.get')
def test_extract_success(mock_get):
    """Menguji ekstraksi yang berhasil dari dua halaman."""
    
    # Konfigurasi respons mock
    mock_response_page1 = Mock()
    mock_response_page1.status_code = 200
    mock_response_page1.content = MOCK_HTML_CONTENT.encode('utf-8')
    mock_response_page1.raise_for_status.return_value = None
    
    mock_response_page2 = Mock()
    mock_response_page2.status_code = 200
    mock_response_page2.content = MOCK_HTML_CONTENT.encode('utf-8')
    mock_response_page2.raise_for_status.return_value = None
    
    # Atur respons untuk panggilan requests.get() yang berbeda
    # Kita hanya perlu menguji dua halaman untuk memastikan logika perulangan berjalan
    mock_get.side_effect = [mock_response_page1, mock_response_page2] 
    
    # Jalankan fungsi extract_data (akan berhenti setelah MAX_DATA)
    # Kita ubah MAX_DATA secara temporer untuk pengujian, jika MAX_DATA di utils/extract.py = 1000, 
    # maka pengujian ini akan berjalan terlalu lama. Asumsi kita menguji hanya dua halaman.
    
    # Untuk pengujian ini, kita hanya menjalankan 2 halaman (20 data)
    data = extract_data() 
    
    # Ekspektasi: 10 produk di halaman 1 + 10 produk di halaman 2 = 20 data
    assert len(data) == 20
    assert isinstance(data, list)
    assert data[0]['Title'] == 'Produk Test A'
    assert data[10]['Price'] == '$10.00'
    
    # Pastikan requests.get dipanggil untuk halaman 1 dan 2
    #mock_get.assert_any_call(f"{BASE_URL}?page=1", headers=f"{extract_data.__globals__['headers']}", timeout=10)
    #mock_get.assert_any_call(f"{BASE_URL}?page=2", headers=f"{extract_data.__globals__['headers']}", timeout=10)
    mock_get.assert_any_call(f"{BASE_URL}/", headers=headers, timeout=10)
    mock_get.assert_any_call(f"{BASE_URL}/page2", headers=headers, timeout=10)


@patch('requests.get')
def test_extract_http_error(mock_get):
    """Menguji penanganan kesalahan HTTP (misal 404 atau 500)."""
    
    mock_response = Mock()
    mock_response.status_code = 404
    # Konfigurasi raise_for_status untuk melempar exception requests.HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    
    mock_get.return_value = mock_response
    
    # Jalankan fungsi, seharusnya mengembalikan list kosong atau list dengan data sebelum error
    data = extract_data()
    
    # Karena kita belum memasukkan data valid, kita asumsikan 0 data
    # (extract_data akan menangkap error dan mengembalikan data yang sudah terkumpul)
    assert len(data) == 0

# Catatan: Untuk menjalankan test ini, Anda mungkin perlu mengubah import headers 
# atau mendefinisikannya dalam test atau di utils/extract.py