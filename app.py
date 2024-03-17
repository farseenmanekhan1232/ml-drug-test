from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from drug_test.util import process_mzml_file
import os

drug_test_blueprint = Blueprint("drug_test", __name__, template_folder="templates")


@drug_test_blueprint.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join("uploads", filename)
            file.save(file_path)
            prediction = process_mzml_file(file_path)
            return render_template("result.html", prediction=prediction)
    return render_template("index.html")
