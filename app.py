
from flask import Flask, render_template

app = Flask(__name__)

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