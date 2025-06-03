from flask import Blueprint, jsonify, request, render_template, current_app
import os
from werkzeug.utils import secure_filename
from config.db import get_connection
from utils.image_utils import allowed_file
from services.plantnet_service import identificar_planta

planta_bp = Blueprint('planta_bp', __name__)

@planta_bp.route('/')
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT p.idPlanta, 
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

@planta_bp.route('/admin')
def home():
    return render_template('registro_planta.html')

@planta_bp.route('/registrar_planta', methods=['GET', 'POST'])
def registrar_planta():
    # Igual que antes, pero simplificado para no extender esta respuesta.
    pass

@planta_bp.route('/iden')
def iden_home():
    return render_template('identificador.html')

@planta_bp.route('/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({'error': 'No se subió ninguna imagen'}), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Ruta del directorio de carga
        upload_folder = os.path.join(current_app.root_path, 'static/uploads')

        # Eliminar archivos existentes en la carpeta
        for f in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error eliminando archivo anterior: {e}")

        # Guardar la nueva imagen
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Ejecutar identificación
        resultado = identificar_planta(filepath, request.form.get('organ'))

        return jsonify(resultado)
    else:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

"""
@planta_bp.route('/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({'error': 'No se proporcionó imagen'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Archivo no válido'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['IDENTIFY_UPLOAD_FOLDER'], filename)
    file.save(filepath)

    resultado = identificar_planta(filepath, request.form.get('organ', 'leaf'))
    return jsonify(resultado)
"""
