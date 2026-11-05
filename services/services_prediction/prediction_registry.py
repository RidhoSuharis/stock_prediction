# ==========================================
# IMPORT SERVICE BBCA
# ==========================================

from services.services_prediction.bbca.model_service_bbca import (
    load_bbca_components
)

from services.services_prediction.bbca.preprocessing_service_bbca import (
    preprocess_bbca
)

from services.services_prediction.bbca.prediction_service_bbca import (
    predict_bbca,
    predict_bbca_5days
)


# ==========================================
# REGISTRASI MODEL SAHAM
# ==========================================

STOCK_SERVICES = {

    "BBCA": {
        "name": "Bank Central Asia",

        "loader": load_bbca_components,

        "preprocessor": preprocess_bbca,

        "predictors": {
            1: predict_bbca,
            5: predict_bbca_5days
        }
    },

    # Model ANTM akan didaftarkan di sini
    # Model BBRI akan didaftarkan di sini
    # Model BMRI akan didaftarkan di sini
    # Model TLKM akan didaftarkan di sini

}