from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import base64
import struct
import numpy as np

app = Flask(__name__)


model_path = "./data/molecular_prediction_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)
    print(file)


def decode_base64_and_unpack(binary_string):
    """Decode base64-encoded string and unpack to floats."""
    decoded_bytes = base64.b64decode(binary_string)
    mz_values = struct.unpack("<" + "d" * (len(decoded_bytes) // 8), decoded_bytes)
    return np.array(mz_values)


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
