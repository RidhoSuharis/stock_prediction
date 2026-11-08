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

## Deploy dengan Docker

Bagian ini untuk deploy production di VPS Ubuntu 24.04. Container menjalankan aplikasi dengan Gunicorn di port `8000`, dan hanya dapat diakses dari `127.0.0.1` sehingga lalu lintas publik harus melewati Nginx di host.

### Prasyarat VPS

- Docker Engine dan Docker Compose plugin.
- Nginx dan Certbot di host.
- Repositori sudah di-clone, misalnya di `/opt/stockpredict`.

### Instalasi Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Logout lalu login kembali agar grup `docker` berlaku, kemudian cek dengan `docker run --rm hello-world`.

### Buka Port Firewall

Di panel VPS (IDCloudHost), buka port `22` (SSH), `80` (HTTP), dan `443` (HTTPS). Tanpa port `80` dan `443`, Nginx tidak dapat diakses dari internet. Jika memakai ufw di host:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Build dan Jalankan

```bash
cd /opt/stockpredict
docker compose build
docker compose up -d
docker compose ps
```

Status service harus `healthy`. Cek halaman dari host:

```bash
curl -I http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/prediksi
curl -I http://127.0.0.1:8000/tentang
curl -I http://127.0.0.1:8000/hasil
```

### Update Kode

```bash
cd /opt/stockpredict
git pull
docker compose up -d --build
```

### Lihat Log

```bash
docker compose logs -f web
docker compose logs --tail 200 web
```

### Ganti Versi

Untuk kembali ke versi lain dari git tag (setelah tag dibuat, misalnya `v1.0.0`, dengan `git tag`):

```bash
cd /opt/stockpredict
git fetch --tags
git checkout v1.0.0
docker compose up -d --build
```

Untuk menjalankan image yang sudah di-build dengan tag tertentu, atur `STOCKPREDICT_IMAGE` di file `.env` pada folder proyek:

```bash
STOCKPREDICT_IMAGE=<registry-user>/stockpredict:1.0.0
```

Lalu jalankan `docker compose up -d`. Compose memakai image tersebut tanpa build ulang.

### Catatan Build di VPS 2 GB RAM

Instalasi TensorFlow membutuhkan memori besar saat `docker compose build`. Pada VPS 2 GB RAM, tambahkan swap 2 GB sebelum build:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Jika VPS tetap kehabisan memori (OOM), build image di komputer lokal lalu kirim ke registry:

```bash
docker build --platform linux/amd64 -t <registry-user>/stockpredict:1.0.0 .
docker push <registry-user>/stockpredict:1.0.0
```

Di VPS, tarik image tersebut dan atur `STOCKPREDICT_IMAGE` seperti pada bagian Ganti Versi:

```bash
docker pull <registry-user>/stockpredict:1.0.0
docker compose up -d
```

### Konfigurasi Nginx di Host

Simpan sebagai `/etc/nginx/sites-available/stockpredict`:

```nginx
server {
    listen 80;
    server_name stockpredict.example.com;

    client_max_body_size 5M;

    location /static/ {
        alias /opt/stockpredict/public/static/;
        expires 7d;
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

Aktifkan dan uji konfigurasi:

```bash
sudo ln -s /etc/nginx/sites-available/stockpredict /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### HTTPS dengan Certbot

Ganti `stockpredict.example.com` dengan domain yang sudah diarahkan ke IP VPS:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d stockpredict.example.com
sudo certbot renew --dry-run
```

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
