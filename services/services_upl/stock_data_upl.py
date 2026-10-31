from __future__ import annotations

from typing import Protocol, TypeVar

import pandas as pd


class UploadedFile(Protocol):
    filename: str | None


_FileT = TypeVar("_FileT", bound=UploadedFile)


def validate_uploaded_file(
    file: _FileT | None,
) -> tuple[_FileT | None, str | None]:
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
    Memeriksa apakah CSV memiliki kolom Date dan Close.
    """
    required_columns: list[str] = ["Date", "Close"]

    missing_columns: list[str] = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        return False, ("Kolom berikut tidak ditemukan: " + ", ".join(missing_columns))

    return True, None
