from flask import Blueprint, request, render_template, current_app
from .util import process_mzml_file, make_prediction

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file:
            molecular_mass = process_mzml_file(file)
            prediction = make_prediction(molecular_mass)
            return render_template("result.html", prediction=prediction)

    return render_template("index.html")
