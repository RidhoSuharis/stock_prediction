import numpy as np

def predict_bbca(model, scaler, X_input):
    """
    Menjalankan prediksi harga saham BBCA
    menggunakan model Bi-LSTM.
    """

    # 1. Prediksi dalam skala normalisasi
    prediction_scaled = model.predict(
        X_input,
        verbose=0
    )

    # 2. Mengembalikan ke skala harga sebenarnya
    prediction = scaler.inverse_transform(
        prediction_scaled
    )

    # 3. Mengambil nilai prediksi
    predicted_price = float(prediction[0, 0])

    return predicted_price

"""
Prediksi harga saham untuk 5 hari perdagangan ke depan
menggunakan Recursive Multi-Step Forecasting.
"""
def predict_bbca_5days(model, scaler, X_input):
    # Salin input agar data awal tidak berubah
    current_input = X_input.copy()

    predictions_scaled = []

    for day in range(5):

        # Prediksi satu langkah ke depan
        next_prediction = model.predict(
            current_input,
            verbose=0
        )

        # Simpan hasil prediksi dalam skala normalisasi
        predictions_scaled.append(
            float(next_prediction[0, 0])
        )

        # Geser window:
        # Hapus data paling lama dan masukkan hasil prediksi
        next_value = next_prediction.reshape(1, 1, 1)

        current_input = np.concatenate(
            (
                current_input[:, 1:, :],
                next_value
            ),
            axis=1
        )

    # Kembalikan seluruh hasil prediksi ke skala harga asli
    predictions_scaled = np.array(
        predictions_scaled
    ).reshape(-1, 1)

    predictions = scaler.inverse_transform(
        predictions_scaled
    )

    return predictions.flatten().tolist()