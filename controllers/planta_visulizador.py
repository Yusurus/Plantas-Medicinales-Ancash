from flask import Blueprint, render_template, jsonify
from config.db import get_connection

visualizacion_bp = Blueprint('visualizacion_bp', __name__)

@visualizacion_bp.route('/')
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT p.idPlanta, 
                       p.nombreCientifico, 
                       p.linkImagen, 
                       fp.nomFamilia,
                          GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') AS nombres_comunes
                          FROM plantas p
                          INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
                          LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
                          WHERE p.idPlanta NOT IN (
                              SELECT DISTINCT fk_plantas FROM archivacionesplantas
                          )
                          GROUP BY p.idPlanta, p.nombreCientifico, p.linkImagen, fp.nomFamilia""")
        rows = cursor.fetchall()
        resultado = [{'idPlanta': r[0], 'nombreCientifico': r[1], 'linkImagen': r[2], 'nomFamilia': r[3], 'nombres_comunes': r[4] or ''} for r in rows]
        return render_template('visualizar_plantas.html', plantas=resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()