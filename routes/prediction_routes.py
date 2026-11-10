from flask import Blueprint, current_app, request, render_template, redirect, url_for

from services.services_upl.stock_data_upl import (
    validate_prediction_data
)

from services.services_prediction.prediction_registry import (
    STOCK_SERVICES
)

prediction_bp = Blueprint('prediction', __name__)

def render_prediction_error(message, status, stock=None, horizon=None):
    return render_template(
        "prediction.html",
        error=message,
        selected_stock=stock,
        selected_horizon=horizon
    ), status

@prediction_bp.route('/proses-prediksi', methods=['GET'])
def redirect_prediction():
    return redirect(url_for('prediction'))

@prediction_bp.route('/proses-prediksi', methods=['POST'])
def process_prediction():

    stock = request.form.get('stock')
    csv_file = request.files.get('csv_file')
    horizon = request.form.get('horizon')

    stock_service = STOCK_SERVICES.get(stock)

    if stock_service is None:
        return render_prediction_error(
            f"Model untuk saham {stock} belum tersedia.",
            400,
            stock=stock
        )

    try:
        horizon = int(horizon)

    except (TypeError, ValueError):
        return render_prediction_error(
            "Horizon prediksi tidak valid.",
            400,
            stock=stock
        )

    predictor = stock_service["predictors"].get(horizon)

    if predictor is None:
        return render_prediction_error(
            f"Horizon {horizon} hari belum tersedia "
            f"untuk saham {stock}.",
            400,
            stock=stock,
            horizon=horizon
        )

    df, error = validate_prediction_data(csv_file)

    if error:
        return render_prediction_error(
            error,
            400,
            stock=stock,
            horizon=horizon
        )

    try:

        model, scaler, metadata = (
            stock_service["loader"]()
        )

        X_input = stock_service["preprocessor"](
            df,
            scaler,
            metadata["window_size"]
        )

        predictions = predictor(model, scaler, X_input)

        if not isinstance(predictions, list):
            predictions = [predictions]

        last_date = df["Date"].iloc[-1]

        last_close = float(
            df["Close"].iloc[-1]
        )

        historical_dates = df["Date"].dt.strftime("%Y-%m-%d").tolist()

        historical_prices = df["Close"].astype(float).tolist()

        return render_template(
            "result.html",

            stock=stock,

            stock_name=stock_service["name"],

            last_close=last_close,

            last_date=last_date.strftime("%d-%m-%Y"),

            total_data=len(df),

            horizon=horizon,

            historical_dates=historical_dates,

            historical_prices=historical_prices,

            predictions=predictions
        )

    except Exception:

        current_app.logger.exception("Error prediksi %s", stock)

        return render_prediction_error(
            "Terjadi kesalahan saat melakukan prediksi. "
            "Silakan periksa data dan konfigurasi model.",
            500,
            stock=stock,
            horizon=horizon
        )