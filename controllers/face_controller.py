from flask import Blueprint, request, jsonify, render_template, session, redirect
from services.image_utils import procesar_imagen_base64
from services.deepface_service import reconocer_rostro
from config.db import get_connection
face_bp = Blueprint('face_bp', __name__)

USUARIOS_MOCK = {'admin': 'password123', 'usuario': '12345', 'test': 'test'}
@face_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@face_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('accesoLogin.html')

    elif request.method == 'POST':
        print('post de acceso login')
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Llamada al procedimiento almacenado
            cursor.callproc('obtener_datos_login', [username, password])

            # Recuperar el resultado del procedimiento
            for result in cursor.stored_results():
                usuario = result.fetchone()
            
            if usuario:
                session['usuario'] = {
                    'idUsuario': usuario['idUsuario'],
                    'usuario': usuario['usuario'],
                    'idEmpleado': usuario['idEmpleado'],
                    'correo': usuario['correo'],
                    'idPersona': usuario['idPersona'],
                    'DNI': usuario['DNI'],
                    'nombres': usuario['nombres'],
                    'apellido1': usuario['apellido1'],
                    'apellido2': usuario['apellido2'],
                    'telefono': usuario['telefono'],
                    'direccion': usuario['direccion'],
                    'categoria': usuario['categoria']}
                return jsonify({
                    'success': True,
                    'message': 'Acceso concedido',
                    'user': usuario
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Credenciales inválidas'
                }), 401

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

#logica para acceso via usuario y contraseña
@face_bp.route('/api/login', methods=['POST'])
def login_tradicional():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if username in USUARIOS_MOCK and USUARIOS_MOCK[username] == password:
        return jsonify({'success': True, 'message': f'Bienvenido, {username}!', 'user': username})
    return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'})

#logica para acceso via reconocimiento facial
@face_bp.route('/api/verify-face', methods=['POST'])
def verificar_rostro():
    data = request.get_json()
    imagen_base64 = data.get('image')
    if not imagen_base64:
        return jsonify({'success': False, 'message': 'No se recibió imagen'})

    imagen_cv = procesar_imagen_base64(imagen_base64)
    if imagen_cv is None:
        return jsonify({'success': False, 'message': 'Error procesando la imagen'})

    resultado = reconocer_rostro(imagen_cv)
    return jsonify(resultado)
