import json
import joblib

from pathlib import Path
from tensorflow.keras.models import load_model


# ==========================================
# KONFIGURASI LOKASI FILE MODEL BBCA
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = BASE_DIR / "models" / "bilstm_bbca"

MODEL_PATH = MODEL_DIR / "bilstm_BBCA.keras"
SCALER_PATH = MODEL_DIR / "scaler_BBCA.pkl"
METADATA_PATH = MODEL_DIR / "metadata_BBCA.json"


# ==========================================
# MEMUAT MODEL, SCALER, DAN METADATA
# ==========================================

def load_bbca_components():

    # Memeriksa keberadaan file
    required_files = [
        MODEL_PATH,
        SCALER_PATH,
        METADATA_PATH
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File tidak ditemukan: {file_path}"
            )

    # Memuat model Bi-LSTM
    model = load_model(
        MODEL_PATH,
        compile=False
    )

    # Memuat scaler
    scaler = joblib.load(SCALER_PATH)

    # Memuat metadata
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return model, scaler, metadata