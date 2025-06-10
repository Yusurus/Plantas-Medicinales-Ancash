from flask import Blueprint, jsonify, render_template, request, session
from config.db import get_connection
from services.plantnet_service import identificar_por_nombre
from services.wikipedia_service import get_wikipedia_plant_image

registro_bp = Blueprint("registro_bp", __name__)


@registro_bp.route("/Acceso")
def acceso_exitoso():
    # Obtener parámetros de la URL (query parameters)
    username = request.args.get("username", "Usuario")
    method = request.args.get("method", "traditional")
    # Renderizar el template pasando los parámetros
    return render_template("AccesoExito.html", username=username, method=method)


@registro_bp.route("/modoadmin")
def home():
    return render_template("registro_plantas.html")


@registro_bp.route("/registrar_planta", methods=["GET", "POST"])
def registrar_planta():
    familias = []
    mensaje = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nomFamilia FROM familias_plantas")
        familias = [row["nomFamilia"] for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

    if request.method == "POST":
        nombreCientifico = request.form["nombreCientifico"]
        nomFamilia = request.form["nomFamilia"]
        nombresComunes = request.form["nombresComunes"]
        imagenes = request.form["imagenes"]
        idEmpleado = session["usuario"]["idEmpleado"]

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc(
                "gestionar_plantas",
                [
                    1,
                    None,
                    nombreCientifico,
                    nomFamilia,
                    nombresComunes,
                    imagenes,
                    idEmpleado,
                ],
            )
            for result in cursor.stored_results():
                mensaje = result.fetchall()[0]["respuesta"]
            conn.commit()
        except Exception as e:
            mensaje = f"Error en el servidor: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return render_template("registro_plantas.html", mensaje=mensaje, familias=familias)


@registro_bp.route("/buscar_nombre", methods=["GET"])
def lookup_plant_by_scientific_name():
    scientific_name = request.args.get("scientific_name")
    if not scientific_name:
        return jsonify({"message": "Nombre científico no proporcionado"}), 400

    final_data = {
        "scientificName": scientific_name,
        "authorship": "",
        "commonNames": [],
        "genus": "",
        "family": "",
        "imageUrls": [],
    }

    plantnet_result = identificar_por_nombre(scientific_name)

    if "message" not in plantnet_result:
        final_data["scientificName"] = plantnet_result.get(
            "scientificName", scientific_name
        )
        final_data["authorship"] = plantnet_result.get("authorship", "")
        final_data["commonNames"] = plantnet_result.get("commonNames", [])
        final_data["genus"] = plantnet_result.get("genus", "")
        final_data["family"] = plantnet_result.get("family", "")
        final_data["imageUrls"] = plantnet_result.get("imageUrls", [])
    else:
        final_data["message"] = "Detalles taxonómicos no disponibles en PlantNet."

    needs_wikipedia_image = not final_data["imageUrls"] or (
        "message" in plantnet_result
        and plantnet_result["message"]
        == "No se encontraron detalles para el nombre científico."
    )

    if needs_wikipedia_image:
        wikipedia_image_url = get_wikipedia_plant_image(scientific_name)
        if wikipedia_image_url:
            final_data["imageUrls"] = [wikipedia_image_url]

    if (
        "message" in plantnet_result
        and plantnet_result["message"]
        == "No se encontraron detalles para el nombre científico."
        and not final_data["imageUrls"]
        and not final_data["family"]
        and not final_data["genus"]
    ):
        return jsonify(plantnet_result), 404
    elif (
        "message" in plantnet_result
        and plantnet_result["message"]
        != "No se encontraron detalles para el nombre científico."
    ):
        return jsonify(plantnet_result), 500
    else:
        return jsonify(final_data)
