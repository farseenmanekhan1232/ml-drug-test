from flask import Flask, request, send_file, render_template
from fpdf import FPDF
import pandas as pd
import joblib
import numpy as np
import base64
import struct
import io

app = Flask(__name__)


def decode_base64_and_unpack(binary_string):
    decoded_bytes = base64.b64decode(binary_string)
    return struct.unpack("<" + "d" * (len(decoded_bytes) // 8), decoded_bytes)


def load_model_and_formulas():
    model_path = "./data/molecular_prediction_model.pkl"
    formulas_path = "./data/compound_formulas.pkl"
    model = joblib.load(model_path)
    formulas = joblib.load(formulas_path)
    return model, formulas


model, formulas = load_model_and_formulas()


@app.route("/", methods=["GET"])
def upload_file():
    return render_template("upload.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    contents = file.read().decode("utf-8")
    start = contents.find("<binary>") + 8
    end = contents.find("</binary>", start)
    encoded_mz = contents[start:end].strip()

    mz_values = decode_base64_and_unpack(encoded_mz)
    data_for_prediction = pd.DataFrame(
        {
            "molecular_mass": mz_values,
            "M+proton": mz_values + 1.00784,
        }
    )

    prediction = model.predict(data_for_prediction)
    prediction_formulas = [formulas[name] for name in prediction]

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Prediction Results", ln=True, align="C")

    # Add table header
    pdf.cell(90, 10, "Drug Name", border=1)
    pdf.cell(40, 10, "Formula", border=1)
    pdf.cell(40, 10, "M/Z Value", border=1, ln=True)

    for name, formula, mz in zip(prediction, prediction_formulas, mz_values):
        pdf.cell(90, 10, name, border=1)
        pdf.cell(40, 10, formula, border=1)
        pdf.cell(40, 10, str(mz), border=1, ln=True)

    pdf_filename = "temp_prediction_results.pdf"
    pdf.output(pdf_filename)
    pdf_buffer.seek(0)

    return redirect(url_for("results", filename=pdf_filename))


@app.route("/download/<filename>")
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
