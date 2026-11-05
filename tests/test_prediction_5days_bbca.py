
import numpy as np

from services.services_prediction.bbca.model_service_bbca import (
    load_bbca_components
)

from services.services_prediction.bbca.preprocessing_service_bbca import (
    preprocess_bbca
)

from services.services_prediction.bbca.prediction_service_bbca import (
    predict_bbca_5days
)


def test_prediction_5days_bbca():

    print("\n=== TEST PREDIKSI BBCA 5 HARI ===")

    # 1. Memuat model, scaler, dan metadata
    model, scaler, metadata = load_bbca_components()

    print("Model berhasil dimuat.")
    print("Saham:", metadata["saham"])
    print("Window size:", metadata["window_size"])

    # 2. Membuat data input dummy
    # Gunakan 30 data harga Close sebagai contoh.
    # Nilai ini hanya untuk pengujian teknis.
    dummy_close = np.linspace(8000, 8500, 30)

    import pandas as pd

    df = pd.DataFrame({
        "Close": dummy_close
    })

    # 3. Preprocessing
    X_input = preprocess_bbca(
        df,
        scaler,
        metadata["window_size"]
    )

    print("Bentuk input:", X_input.shape)

    # 4. Prediksi 5 hari
    predictions = predict_bbca_5days(
        model,
        scaler,
        X_input
    )

    # 5. Pemeriksaan hasil
    assert len(predictions) == 5, (
        "Jumlah prediksi harus tepat 5."
    )

    assert all(
        np.isfinite(value) for value in predictions
    ), "Hasil prediksi mengandung nilai tidak valid."

    assert all(
        value > 0 for value in predictions
    ), "Harga prediksi harus positif."

    # 6. Menampilkan hasil
    print("\nHasil prediksi:")

    for day, price in enumerate(predictions, start=1):
        print(
            f"Hari ke-{day}: Rp {price:,.2f}"
        )

    print("\nSemua pengujian berhasil.")


if __name__ == "__main__":
    test_prediction_5days_bbca()
