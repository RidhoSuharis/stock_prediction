from flask import Blueprint, request, render_template

from services.services_upl.stock_data_upl import (
    validate_prediction_data
)

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/proses-prediksi', methods=['POST'])
def process_prediction():

    # 1. Mengambil input pengguna
    stock = request.form.get('stock')
    csv_file = request.files.get('csv_file')
    horizon = request.form.get('horizon')

    # 2. Validasi kode saham
    if stock not in ["ANTM", "BBCA", "BBRI", "BMRI", "TLKM"]:
        return "Kode saham tidak valid."

    # 3. Validasi horizon
    if horizon not in ["1"]:
        return "Horizon prediksi tidak valid."

    # 4. Validasi data CSV
    df, error = validate_prediction_data(csv_file)

    if error:
        return f"""
            <h3>Validasi Data Gagal</h3>
            <p>{error}</p>
            <a href="/prediksi">Kembali</a>
        """

    # 5. Jika validasi berhasil
    return f"""
        <h2>Validasi Data Berhasil</h2>
        <p>Saham: {stock}</p>
        <p>Jumlah data: {len(df)} baris</p>
        <p>Tanggal awal: {df['Date'].min().date()}</p>
        <p>Tanggal akhir: {df['Date'].max().date()}</p>
        <p>Horizon: {horizon} hari</p>
        <p>Data siap untuk proses prediksi.</p>
        <a href="/prediksi">Kembali</a>
    """