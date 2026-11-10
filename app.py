
from flask import Flask, render_template
from routes.main_routes import main_bp
from routes.prediction_routes import prediction_bp

app = Flask(__name__, static_folder="public/static")
app.register_blueprint(main_bp)
app.register_blueprint(prediction_bp)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prediksi")
def prediction():
    return render_template("prediction.html")

@app.route("/tentang")
def about():
    return render_template("about.html")

@app.route("/hasil")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)