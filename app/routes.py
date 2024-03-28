from flask import Blueprint, render_template, request
from .util import process_mzml_file, predict_substance

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process file upload and get predictions
        file = request.files.get("file")
        if file:
            mz_values, charges = process_mzml_file(file)
            predictions = [
                predict_substance(mz, charge) for mz, charge in zip(mz_values, charges)
            ]
            return render_template("result.html", predictions=predictions)
    return render_template("index.html")
