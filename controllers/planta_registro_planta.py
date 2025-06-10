from flask import Blueprint, render_template, request, session
from config.db import get_connection

registro_bp = Blueprint('registro_bp', __name__)

@registro_bp.route('/Acceso')
def acceso_exitoso():
    # Obtener parámetros de la URL (query parameters)
    username = request.args.get('username', 'Usuario')
    method = request.args.get('method', 'traditional')    
    # Renderizar el template pasando los parámetros
    return render_template('AccesoExito.html', username=username, method=method)


@registro_bp.route('/modoadmin')
def home():
    return render_template('registro_planta.html')

@registro_bp.route('/registrar_planta', methods=['GET', 'POST'])
def registrar_planta():
    familias = []
    mensaje = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nomFamilia FROM familias_plantas")
        familias = [row['nomFamilia'] for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()
    
    if request.method == 'POST':
        nombreCientifico = request.form['nombreCientifico']
        nomFamilia = request.form['nomFamilia']
        nombresComunes = request.form['nombresComunes']
        imagenes = request.form['imagenes']
        idEmpleado = session['usuario']['idEmpleado']
        print(nombresComunes)
        
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('gestionar_plantas', [1, None, nombreCientifico, nomFamilia, nombresComunes, imagenes, idEmpleado])
            for result in cursor.stored_results():
                mensaje = result.fetchall()[0]['respuesta']
            conn.commit()
        except Exception as e:
            mensaje = f'Error en el servidor: {str(e)}'
        finally:
            cursor.close()
            conn.close()

    return render_template('registro_plantas.html', mensaje=mensaje, familias=familias)
    #pass