from flask import Blueprint, render_template, jsonify
from config.db import get_connection

visualizacion_bp = Blueprint("visualizacion_bp", __name__)


@visualizacion_bp.route("/")
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Llamada al procedimiento almacenado para obtener las plantas activas
        cursor.execute("""select * from vta_plantas2 order by nombreCientifico asc""")
        rows = cursor.fetchall()
        resultado = [
            {
                "idPlanta": r[0],
                "nombreCientifico": r[1],
                "linkImagen": r[2],
                "nomFamilia": r[3],
                "nombres_comunes": r[4] or "",
            }
            for r in rows
        ]
        return render_template("visualizar_plantas.html", plantas=resultado)
    except Exception as e:
        # print("Asegurece de tner todas las librerias intaladas y que tenga el archivo .env," \
        #                        " en caso de no tner el arvhivo .env solicitelo a un miembro desarollador del equipo o cree uno usted" \
        #                        "en el .env principalmente ban datos de la conexion a la Base de datos y una clave secreta para la" \
        #                        "conexion a la API Pl@nNet de reococimiento IA de las plantas, puede ir al archivo bd.py para ver" \
        #                        "que deberia ir en el archivo .env")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
