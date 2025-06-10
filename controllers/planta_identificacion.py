from flask import Blueprint, request, jsonify, render_template, current_app, session
import os
from werkzeug.utils import secure_filename
from services.image_utils import allowed_file
from services.plantnet_service import identificar_planta

identificacion_bp = Blueprint("identificacion_bp", __name__)


@identificacion_bp.route("/iden")
def iden_home():
    return render_template("identificador.html")


@identificacion_bp.route("/identify", methods=["POST"])
def identify():
    if "image" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400

    file = request.files["image"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "static/uploads")

        for f in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error eliminando archivo anterior: {e}")

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        resultado = identificar_planta(filepath, request.form.get("organ"))

        is_logged_in = "usuario" in session and session["usuario"] is not None
        resultado["is_logged_in"] = is_logged_in
        print(f"Usuario logueado: {is_logged_in}")

        return jsonify(resultado)
    else:
        return jsonify({"error": "Tipo de archivo no permitido"}), 400
