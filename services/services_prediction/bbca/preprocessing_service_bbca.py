import numpy as np


def preprocess_bbca(df, scaler, window_size=30):
    """
    Melakukan preprocessing data historis BBCA
    untuk input model Bi-LSTM.
    """

    # 1. Mengambil 30 data Close terakhir
    last_data = df[["Close"]].tail(window_size)

    # 2. Memastikan jumlah data mencukupi
    if len(last_data) < window_size:
        raise ValueError(
            f"Minimal diperlukan {window_size} data Close."
        )

    # 3. Normalisasi menggunakan scaler hasil training
    scaled_data = scaler.transform(last_data)

    # 4. Mengubah bentuk menjadi tensor 3 dimensi
    X_input = scaled_data.reshape(
        1,
        window_size,
        1
    )

    return X_input