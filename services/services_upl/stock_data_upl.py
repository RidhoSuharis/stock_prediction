
import pandas as pd


def validate_uploaded_file(file):
    """
    Memeriksa keberadaan file dan ekstensi CSV.
    """
    if file is None or file.filename == "":
        return None, "Silakan pilih file terlebih dahulu."

    filename = file.filename.strip()

    if "." not in filename:
        return None, "File harus memiliki ekstensi .csv."

    extension = filename.rsplit(".", 1)[1].lower()

    if extension != "csv":
        return None, "Format file harus CSV."

    return file, None


def validate_csv_columns(df):
    """
    Memeriksa apakah CSV memiliki kolom Date dan Close.
    """
    required_columns = ["Date", "Close"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return False, (
            "Kolom berikut tidak ditemukan: "
            + ", ".join(missing_columns)
        )

    return True, None