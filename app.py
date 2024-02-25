from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("drug_test/drug_prediction_model.pkl")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict_form.html")
    elif request.method == "POST":
        mass = request.form["mass"]
        mass_proton = request.form["mass_proton"]
        input_df = pd.DataFrame([[mass, mass_proton]], columns=["Mass", "M+proton"])
        prediction = model.predict(input_df)
        return jsonify({"prediction": prediction[0]})


if __name__ == "__main__":
    app.run(debug=True)
