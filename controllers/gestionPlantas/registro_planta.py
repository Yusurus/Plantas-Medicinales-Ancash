from flask import Blueprint, jsonify, render_template, request, session
from config.db import get_connection
from services.plantnet_service import identificar_por_nombre
from services.wikipedia_service import (
    get_wikipedia_plant_image,
    get_wikipedia_plant_images,
)

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
    return render_template("gestion_plantas.html")


@registro_bp.route("/registrar_planta", methods=["GET", "POST"])
@registro_bp.route("/editar_planta/<id_planta>", methods=["GET", "POST"])
def registrar_planta(id_planta=None):
    familias = []
    mensaje = None
    planta = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT nomFamilia FROM familias_plantas ORDER BY nomFamilia ASC"
        )
        familias = [row["nomFamilia"] for row in cursor.fetchall()]

        if id_planta:
            cursor.execute(
                "select * from vta_plantas2 where idPlanta = %s", (id_planta,)
            )
            planta = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if request.method == "POST":
        nombreCientifico = request.form["nombreCientifico"]
        nomFamilia = request.form["nomFamilia"]
        nombresComunes = request.form["nombresComunes"]
        imagenes = request.form["imagenes"]
        descMorfologica = request.form["descMorfologica"]
        idEmpleado = session["usuario"]["idEmpleado"]

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            ev = 2 if id_planta else 1
            cursor.callproc(
                "gestionar_plantas",
                [
                    ev,
                    id_planta,
                    nombreCientifico,
                    nomFamilia,
                    nombresComunes,
                    imagenes,
                    idEmpleado,
                    descMorfologica,
                ],
            )
            for result in cursor.stored_results():
                mensaje = result.fetchall()[0]["respuesta"]
                if mensaje.startswith("Error: Duplicate entry"):
                    mensaje = "La planta ya existe en la base de datos"
                # if mensaje == "Planta actualizada correctamente":
                #     flash(mensaje)
                #     return redirect(url_for("registro_planta.registro_planta"))
            conn.commit()
        except Exception as e:
            mensaje = f"Error en el servidor: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return render_template(
        "gestion_plantas.html",
        mensaje=mensaje,
        familias=familias,
        planta=planta,
        id_planta=id_planta,
    )


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
        wikipedia_image_url = get_wikipedia_plant_images(scientific_name)
        if wikipedia_image_url:
            final_data["imageUrls"] = wikipedia_image_url
    print(final_data["imageUrls"])
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


@registro_bp.route("/registrar_familia", methods=["POST"])
def registrar_familia():
    print(">> Se llamó a /registrar_familia")
    print(">> Headers:", request.headers)
    print(">> Body:", request.get_data(as_text=True))

    data = request.get_json()
    nombre = data.get("nombreFamilia") if data else None
    print(">> nombreFamilia:", nombre)
    if not nombre:
        return jsonify(success=False, message="Nombre de familia requerido"), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verifica si ya existe
        cursor.execute(
            "SELECT idfamiliaPlanta FROM familias_plantas WHERE nomFamilia = %s",
            (nombre,),
        )
        if cursor.fetchone():
            return jsonify(success=True, message="Ya existe")

        # Inserta la nueva familia
        print(nombre)
        cursor.execute(
            "INSERT INTO familias_plantas (nomFamilia) VALUES (%s)", (nombre,)
        )
        conn.commit()
        print(nombre)
        return jsonify(success=True, message="Familia registrada")
    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e))
    finally:
        cursor.close()
        conn.close()
