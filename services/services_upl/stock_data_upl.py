
import io

import pandas as pd
from werkzeug.datastructures import FileStorage


def validate_uploaded_file(
    file: FileStorage | None,
) -> tuple[FileStorage | None, str | None]:
    """
    Memeriksa keberadaan file dan ekstensi CSV.
    """
    if file is None or not file.filename:
        return None, "Silakan pilih file terlebih dahulu."

    filename = file.filename.strip()

    if "." not in filename:
        return None, "File harus memiliki ekstensi .csv."

    extension = filename.rsplit(".", 1)[1].lower()

    if extension != "csv":
        return None, "Format file harus CSV."

    return file, None


def validate_csv_columns(
    df: pd.DataFrame,
) -> tuple[bool, str | None]:
    """
    Memeriksa keberadaan kolom Date dan Close.
    """
    required_columns = ["Date", "Close"]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return False, (
            "Kolom berikut tidak ditemukan: "
            + ", ".join(missing_columns)
        )

    return True, None


def validate_prediction_data(
    file: FileStorage | None,
) -> tuple[pd.DataFrame | None, str | None]:
    """
    Memvalidasi data historis saham untuk prediksi Bi-LSTM.

    Ketentuan:
    - Format CSV
    - Kolom Date dan Close
    - Mendukung delimiter koma maupun titik koma
    - Tanggal valid dan tidak duplikat
    - Harga Close numerik dan positif
    - Minimal 30 data perdagangan valid
    """

    # 1. Validasi file
    file, error = validate_uploaded_file(file)

    if error:
        return None, error

    # 2. Membaca CSV
    try:
        raw = file.read()
        first_line = raw.split(b"\n")[0].strip().lower()
        skip = 1 if first_line.startswith(b"sep=") else 0
        df = pd.read_csv(
            io.BytesIO(raw),
            sep=None,
            engine="python",
            skiprows=skip,
        )

    except Exception:
        return None, "File CSV tidak dapat dibaca."

    # 3. Validasi kolom
    valid, error = validate_csv_columns(df)

    if not valid:
        return None, error

    # 4. Mengambil kolom yang diperlukan
    df = df[["Date", "Close"]].copy()

    # 5. Validasi tanggal
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
        dayfirst=True
    )

    if df["Date"].isna().any():
        return None, "Format tanggal tidak valid atau kosong."

    # 6. Validasi harga Close
    df["Close"] = pd.to_numeric(
        df["Close"],
        errors="coerce"
    )

    if df["Close"].isna().any():
        return None, (
            "Kolom Close mengandung nilai kosong atau bukan angka."
        )

    if (df["Close"] <= 0).any():
        return None, "Harga Close harus lebih besar dari nol."

    # 7. Validasi tanggal duplikat
    if df["Date"].duplicated().any():
        return None, "Terdapat tanggal yang duplikat."

    # 8. Mengurutkan data berdasarkan tanggal
    df = df.sort_values(
        "Date"
    ).reset_index(drop=True)

    # 9. Validasi minimal 30 data
    if len(df) < 30:
        return None, (
            f"Data historis hanya {len(df)} baris. "
            "Minimal diperlukan 30 hari perdagangan valid."
        )

    return df, None
