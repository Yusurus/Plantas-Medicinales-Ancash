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
        # Llamada al procedimiento almacenado para obtener los detalles de la planta
        #query = """CALL sp_info_planta_activa(%s);"""
        query = """CALL sp_obtener_info_completa_planta(%s);"""
        cursor.execute(query, (plant_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Planta no encontrada"}), 404

        resultado = {
            'idPlanta': row[0],
            'nombreCientifico': row[1],
            'linkImagen': row[2],
            'nomFamilia': row[3],
            'nombres_comunes': row[4],
            'ecoregiones': row[5],
            'regiones': row[6],
            'provincias': row[7],
            'usos_medicinales': row[8],
            'saberes_culturales': row[9],
            'aportes_expertos': row[10],
            'empleado_registro': row[11],
            'cargo_empleado': row[12],
            'datos_morfologicos': row[13]
        }
        print("Detalles de la planta obtenidos:", resultado)

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
