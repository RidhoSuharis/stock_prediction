import io
import unittest

from app import app


def build_csv(rows=30):
    lines = ["Date,Close"]
    for i in range(rows):
        lines.append(f"{i + 1:02d}/01/2026,{8000 + i}")
    return "\n".join(lines).encode()


class TestPredictionErrors(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def post(self, stock="BBCA", horizon="1", csv=None):
        data = {"stock": stock, "horizon": horizon}
        if csv is not None:
            data["csv_file"] = (io.BytesIO(csv), "data.csv")
        return self.client.post(
            "/proses-prediksi",
            data=data,
            content_type="multipart/form-data"
        )

    def test_get_redirects_to_form(self):
        response = self.client.get("/proses-prediksi")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/prediksi"))

    def test_invalid_stock_renders_alert(self):
        response = self.post(stock="XXXX", csv=build_csv())
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn('data-variant="destructive"', body)
        self.assertIn("Model untuk saham XXXX belum tersedia.", body)

    def test_invalid_horizon_renders_alert(self):
        response = self.post(horizon="abc", csv=build_csv())
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Horizon prediksi tidak valid.", body)

    def test_unavailable_horizon_renders_alert(self):
        response = self.post(horizon="7", csv=build_csv())
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Horizon 7 hari belum tersedia untuk saham BBCA.", body)

    def test_missing_file_renders_alert(self):
        response = self.post()
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Silakan pilih file terlebih dahulu.", body)

    def test_insufficient_rows_renders_alert(self):
        response = self.post(csv=build_csv(rows=29))
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Data historis hanya 29 baris.", body)

    def test_error_keeps_selected_stock_and_horizon(self):
        response = self.post(stock="BBCA", horizon="5", csv=build_csv(rows=29))
        body = response.get_data(as_text=True)

        self.assertIn('value="BBCA" selected', body)
        self.assertIn('value="5" selected', body)
        self.assertNotIn('value="" disabled selected', body)


if __name__ == "__main__":
    unittest.main()
