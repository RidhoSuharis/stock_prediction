
import unittest
import pandas as pd
from services.services_upl.stock_data_upl import validate_csv_columns
from services.services_upl.stock_data_upl import validate_uploaded_file


class DummyFile:
    def __init__(self, filename):
        self.filename = filename


class TestValidateUploadedFile(unittest.TestCase):

    def test_no_file(self):
        hasil, pesan = validate_uploaded_file(None)

        self.assertIsNone(hasil)
        self.assertEqual(
            pesan,
            "Silakan pilih file terlebih dahulu."
        )

    def test_empty_filename(self):
        file = DummyFile("")

        hasil, pesan = validate_uploaded_file(file)

        self.assertIsNone(hasil)
        self.assertEqual(
            pesan,
            "Silakan pilih file terlebih dahulu."
        )

    def test_valid_csv(self):
        file = DummyFile("data_saham.csv")

        hasil, pesan = validate_uploaded_file(file)

        self.assertIs(hasil, file)
        self.assertIsNone(pesan)

    def test_invalid_extension(self):
        file = DummyFile("data_saham.xlsx")

        hasil, pesan = validate_uploaded_file(file)

        self.assertIsNone(hasil)
        self.assertEqual(
            pesan,
            "Format file harus CSV."
        )
    
    def test_valid_csv_columns(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02"],
            "Close": [1500, 1520]
        })

        hasil, pesan = validate_csv_columns(df)

        self.assertTrue(hasil)
        self.assertIsNone(pesan)

    def test_missing_csv_column(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02"],
            "Open": [1480, 1500]
        })

        hasil, pesan = validate_csv_columns(df)

        self.assertFalse(hasil)
        self.assertEqual(
            pesan,
            "Kolom berikut tidak ditemukan: Close"
        )

if __name__ == "__main__":
    unittest.main()