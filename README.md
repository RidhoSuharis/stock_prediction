# StockPredict

Prototipe aplikasi web untuk memprediksi harga penutupan saham LQ45 menggunakan model **Bidirectional Long Short-Term Memory (Bi-LSTM)**. Pengguna memilih saham, mengunggah data historis dalam format CSV, menentukan horizon prediksi, lalu melihat hasilnya dalam bentuk ringkasan, tabel, dan grafik.

> Aplikasi ini merupakan prototipe penelitian. Seluruh angka yang ditampilkan adalah estimasi model, bukan rekomendasi investasi.

## Fitur Utama

- **Prediksi Bi-LSTM**: model deep learning yang mempelajari pola harga penutupan dari data historis.
- **Prediksi multi-horizon**: estimasi harga untuk 1, 5, dan 10 hari perdagangan ke depan.
- **Recursive multi-step forecasting**: hasil prediksi digunakan kembali sebagai input untuk memprediksi hari berikutnya.
- **Validasi data otomatis**: file dan isi CSV diperiksa di browser serta di server sebelum diproses model.
- **Visualisasi interaktif**: grafik harga historis dan prediksi, ringkasan perubahan harga, serta tabel estimasi per hari.

## Saham dan Horizon

| Saham | Nama Perusahaan | Horizon |
|---|---|---|
| `ANTM` | Aneka Tambang | 1, 5, dan 10 hari |
| `BBCA` | Bank Central Asia | 1, 5, dan 10 hari |
| `BBRI` | Bank Rakyat Indonesia | 1, 5, dan 10 hari |
| `BMRI` | Bank Mandiri | 1, 5, dan 10 hari |
| `TLKM` | Telkom Indonesia | 1, 5, dan 10 hari |

Setiap saham menggunakan model, scaler, dan metadata tersendiri.

## Cara Kerja

1. Pengguna memilih kode saham.
2. Pengguna mengunggah data historis dalam format CSV.
3. Server memvalidasi file, kolom, tanggal, dan nilai harga.
4. Data `Close` sebanyak 30 periode terakhir dinormalisasi menggunakan scaler hasil training.
5. Model Bi-LSTM melakukan prediksi.
6. Untuk horizon lebih dari satu hari, prediksi dilakukan secara bertahap menggunakan **Recursive Multi-Step Forecasting**: hasil prediksi hari sebelumnya dipakai sebagai input untuk hari berikutnya.
7. Hasil ditampilkan sebagai ringkasan, tabel, dan grafik.

## Format CSV

File wajib memiliki dua kolom, yaitu `Date` dan `Close`.

| Date | Close |
|---|---|
| 2026-01-05 | 8250 |
| 2026-01-06 | 8300 |
| 2026-01-07 | 8275 |
| 2026-01-08 | 8350 |
| 2026-01-09 | 8400 |
| 2026-01-12 | 8425 |
| 2026-01-13 | 8390 |
| 2026-01-14 | 8450 |

Ketentuan:

- `Date` berisi tanggal perdagangan yang valid dan tidak duplikat.
- `Close` berisi harga penutupan berupa angka positif.
- Pemisah kolom boleh koma atau titik koma.
- Baris pembuka `sep=` didukung.
- Data akan diurutkan otomatis berdasarkan tanggal.
- Minimal 30 baris data perdagangan yang valid.
- Ukuran file maksimal 5 MB.

Template CSV juga dapat diunduh melalui tombol **Unduh Template CSV** pada halaman prediksi.

## Menjalankan Proyek

### Prasyarat

- Python 3.12
- Git
- RAM yang cukup untuk menjalankan TensorFlow, disarankan minimal 1 GB

### Langkah Instalasi

```bash
git clone <url-repository>
cd stock_prediction
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements-ml.txt
```

Di Windows, aktivasi virtual environment menggunakan:

```bash
.venv\Scripts\activate
```

Penjelasan dependensi:

- `requirements.txt`: Flask dan Gunicorn untuk aplikasi web.
- `requirements-ml.txt`: TensorFlow, NumPy, pandas, scikit-learn, Plotly, dan SciPy untuk proses prediksi.

### Menjalankan Aplikasi

```bash
python app.py
```

Buka `http://127.0.0.1:5000` di browser.

Model, scaler, dan metadata untuk saham yang telah selesai dilatih sudah disertakan di repositori, sehingga tidak perlu melakukan training ulang. TensorFlow akan memuat model saat prediksi pertama dijalankan sehingga proses awal bisa terasa lebih lama.

## Halaman Aplikasi

| URL | Keterangan |
|---|---|
| `/` | Beranda dan penjelasan singkat aplikasi |
| `/prediksi` | Form pemilihan saham, upload CSV, dan horizon |
| `/tentang` | Penjelasan metode, data, dan batasan aplikasi |
| `/hasil` | Hasil prediksi, tabel, dan grafik |
| `/download-template` | Mengunduh template CSV |
| `/proses-prediksi` | Memproses prediksi melalui `POST` |

## Model

| Komponen | Keterangan |
|---|---|
| Arsitektur | Bi-LSTM |
| Layer | Bidirectional LSTM 64, dropout 0.1, Bidirectional LSTM 32, dropout 0.1, Dense(1) |
| Fitur | Harga penutupan (`Close`) |
| Normalisasi | MinMaxScaler, rentang 0 sampai 1 |
| Panjang window | 30 periode |
| Output | Harga penutupan hasil prediksi |

## Pengujian

Jalankan test validasi:

```bash
python -m unittest discover -s tests -v
```

Untuk memeriksa prediksi BBCA 5 hari secara langsung, termasuk memuat model TensorFlow:

```bash
python -m tests.test_prediction_5days_bbca
```

## Catatan

- Hasil prediksi hanya berlaku untuk data dan model yang tersedia.
- Prediksi tidak menjamin pergerakan harga saham di masa mendatang.
- Jangan menggunakan hasil aplikasi ini sebagai dasar keputusan investasi.
