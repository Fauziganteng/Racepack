<<<<<<< HEAD
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

EXCEL_FILE = 'data_peserta.xlsx'
participants_data = None

def load_excel_data():
    global participants_data
    excel_path = os.path.join(os.path.dirname(__file__), EXCEL_FILE)

    if not os.path.exists(excel_path):
        print(f"ERROR: File Excel '{EXCEL_FILE}' tidak ditemukan.")
        participants_data = pd.DataFrame(columns=['id_pendaftar', 'nama', 'jenis_kelamin', 'ukuran_jersey', 'nomor_bib', 'kategori'])
        return

    try:
        participants_data = pd.read_excel(excel_path, sheet_name='Peserta')
        participants_data['id_pendaftar'] = participants_data['id_pendaftar'].astype(str)
        participants_data['nama'] = participants_data['nama'].astype(str)
        print(f"Data berhasil dimuat. Jumlah peserta: {len(participants_data)}")
    except Exception as e:
        print(f"ERROR saat baca Excel: {e}")
        participants_data = pd.DataFrame(columns=['id_pendaftar', 'nama', 'jenis_kelamin', 'ukuran_jersey', 'nomor_bib', 'kategori'])

load_excel_data()

@app.route('/api/peserta', methods=['GET'])
def get_peserta():
    search_query = request.args.get('query', '').strip().lower()
    
    if not search_query:
        return jsonify({"message": "Mohon masukkan ID Pendaftar atau Nama."}), 400

    if participants_data is None or participants_data.empty:
        return jsonify({"message": "Data peserta belum dimuat atau kosong."}), 500

    match = participants_data[
        (participants_data['id_pendaftar'].str.lower() == search_query) |
        (participants_data['nama'].str.lower() == search_query)
    ]

    if not match.empty:
        return jsonify(match.iloc[0].to_dict())
    else:
        return jsonify({"message": "Data tidak ditemukan"}), 404
=======
# Import library yang dibutuhkan
from flask import Flask, request, jsonify
import pandas as pd # Import pandas untuk membaca Excel
import os
from flask_cors import CORS # Import CORS untuk menangani Cross-Origin Resource Sharing

# Inisialisasi aplikasi Flask
app = Flask(__name__)
# Aktifkan CORS untuk semua rute.
CORS(app) 

# Nama file Excel
EXCEL_FILE = 'data_peserta.xlsx'
# Variabel global untuk menyimpan data dari Excel
participants_data = None

# Fungsi untuk memuat data dari file Excel
def load_excel_data():
    global participants_data
    excel_path = os.path.join(os.path.dirname(__file__), EXCEL_FILE)
    
    if not os.path.exists(excel_path):
        print(f"ERROR: File Excel '{EXCEL_FILE}' tidak ditemukan di '{excel_path}'.")
        print("Pastikan Anda telah membuat file Excel dengan nama dan struktur yang benar.")
        # Buat DataFrame kosong jika file tidak ditemukan
        participants_data = pd.DataFrame(columns=['id_pendaftar', 'nama', 'jenis_kelamin', 'ukuran_jersey', 'nomor_bib', 'kategori'])
        return

    try:
        # Membaca sheet 'Peserta' dari file Excel
        participants_data = pd.read_excel(excel_path, sheet_name='Peserta')
        # Mengonversi kolom 'id_pendaftar' dan 'nama' ke string untuk pencarian yang konsisten
        participants_data['id_pendaftar'] = participants_data['id_pendaftar'].astype(str)
        participants_data['nama'] = participants_data['nama'].astype(str)
        print(f"Data berhasil dimuat dari '{EXCEL_FILE}'. Jumlah peserta: {len(participants_data)}")
    except Exception as e:
        print(f"ERROR: Gagal memuat data dari Excel: {e}")
        print("Pastikan nama sheet adalah 'Peserta' dan format file benar (.xlsx).")
        # Buat DataFrame kosong jika gagal memuat
        participants_data = pd.DataFrame(columns=['id_pendaftar', 'nama', 'jenis_kelamin', 'ukuran_jersey', 'nomor_bib', 'kategori'])

# Muat data Excel saat aplikasi dimulai
load_excel_data()


# Endpoint API untuk mencari data peserta
@app.route('/api/peserta', methods=['GET'])
def get_peserta():
    search_query = request.args.get('query', '').strip().lower() # Ambil query dan konversi ke huruf kecil
    
    if not search_query:
        return jsonify({"message": "Mohon masukkan ID Pendaftar atau Nama."}), 400

    if participants_data is None or participants_data.empty:
        return jsonify({"message": "Data peserta belum dimuat atau kosong."}), 500

    found_participant = None

    # Cari berdasarkan id_pendaftar (pencocokan persis, case-insensitive)
    # Menggunakan .str.lower() untuk mencocokkan secara case-insensitive
    match_id = participants_data[participants_data['id_pendaftar'].str.lower() == search_query]
    if not match_id.empty:
        found_participant = match_id.iloc[0].to_dict()
    else:
        # Jika tidak ditemukan berdasarkan id_pendaftar, coba cari berdasarkan nama (pencocokan persis, case-insensitive)
        match_name = participants_data[participants_data['nama'].str.lower() == search_query]
        if not match_name.empty:
            found_participant = match_name.iloc[0].to_dict()
    
    if found_participant:
        return jsonify(found_participant)
    else:
        return jsonify({"message": "Data tidak ditemukan"}), 404 

# Jalankan aplikasi Flask
if __name__ == '__main__':
    # Untuk pengembangan, aktifkan debug mode dan izinkan CORS
    # Untuk produksi, Anda perlu konfigurasi CORS yang lebih ketat dan menggunakan WSGI server (misal Gunicorn)
    app.run(debug=True, port=5000) # Jalankan di port 5000 secara default
>>>>>>> 0849f76d935397053b60b0fcc4eb796a6ef8452a
