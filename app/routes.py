from flask import render_template, request, redirect, url_for
from app import app
from .models import load_model
from .utils import handle_mzml_upload, mz_to_molecular_mass


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        mz_values, charges = handle_mzml_upload(file)
        model = load_model()
        predictions = []
        for mz, charge in zip(mz_values, charges):
            mass = mz_to_molecular_mass(mz, charge)
            prediction = model.predict([mass])[
                0
            ]  # Assuming model expects a list of masses
            predictions.append((mass, prediction))
        return render_template("result.html", predictions=predictions)
