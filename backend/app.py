from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
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

# Muat data saat startup
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

# Sajikan index.html (frontend)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Sajikan static file (JS, CSS, logo.png, dsb)
@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
