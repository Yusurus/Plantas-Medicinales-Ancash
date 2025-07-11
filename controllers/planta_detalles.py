from flask import Blueprint, jsonify, render_template
from config.db import get_connection

detalles_bp = Blueprint("detalles_bp", __name__)


@detalles_bp.route("/detalles/<int:plant_id>")
def detalles_planta(plant_id):
    return render_template("detalle_planta.html", plant_idg=plant_id)


@detalles_bp.route("/api/planta/<int:plant_id>")
def obtener_detalles_planta(plant_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # query = """CALL sp_info_planta_activa(%s);"""
        query = """CALL sp_obtener_info_completa_planta(%s);"""
        cursor.execute(query, (plant_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Planta no encontrada"}), 404

        resultado = {
            "idPlanta": row[0],
            "nombreCientifico": row[1],
            "linkImagen": row[2],
            "nomFamilia": row[3],
            "nombres_comunes": row[4],
            "ecoregiones": row[5],
            "regiones": row[6],
            "provincias": row[7],
            "usos_medicinales": row[8],
            "saberes_culturales": row[9],
            "aportes_expertos": row[10],
            "empleado_registro": row[11],
            "cargo_empleado": row[12],
            "datos_morfologicos": row[13],
        }
        # print("Detalles de la planta obtenidos:", resultado)

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@detalles_bp.route("/api/planta/<int:plant_id>/imagenes")
def obtener_imagenes_planta(plant_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Consulta para obtener todas las imágenes de la planta
        query = """SELECT linkimagen FROM linksimagenes WHERE fk_plantas = %s;"""
        cursor.execute(query, (plant_id,))
        rows = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        imagenes = []
        for row in rows:
            imagenes.append({"linkimagen": row[0]})

        print(f"Imágenes encontradas para planta {plant_id}:", len(imagenes))

        return jsonify(imagenes)

    except Exception as e:
        print(f"Error al obtener imágenes: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
