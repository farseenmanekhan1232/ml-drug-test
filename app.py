from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import base64
import struct
import numpy as np
import joblib

app = Flask(__name__)


def decode_base64_and_unpack(binary_string):
    decoded_bytes = base64.b64decode(binary_string)
    mz_values = struct.unpack("<" + "d" * (len(decoded_bytes) // 8), decoded_bytes)
    return np.array(mz_values)


def load_model():
    model_path = "./data/molecular_prediction_model.pkl"
    model = joblib.load(model_path)
    return model


# Load your model
model = load_model()


@app.route("/", methods=["GET"])
def upload_file():
    return render_template("upload.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    try:
        model = load_model()
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

        print(model)
        prediction = model.predict(data_for_prediction)

        response = {"prediction": prediction.tolist()}
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "message": "Failed to process file or make prediction",
                }
            ),
            500,
        )

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
