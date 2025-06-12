from flask import Blueprint, jsonify, render_template, session, request
from config.db import get_connection

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
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
            
            
            
            
"""
#logica para acceso via usuario y contraseña
@user_bp.route('/api/login', methods=['POST'])
def login_tradicional():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if username in USUARIOS_MOCK and USUARIOS_MOCK[username] == password:
        return jsonify({'success': True, 'message': f'Bienvenido, {username}!', 'user': username})
    return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'})"""





"""@user_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    nombre, correo = data.get('nombre'), data.get('correo')

    if not nombre or not correo:
        return jsonify({'error': 'Nombre y correo son requeridos'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        conn.commit()
        return jsonify({'mensaje': 'Usuario registrado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/usuarios')
def usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, correo FROM usuarios")
        rows = cursor.fetchall()
        return jsonify([{'nombre': r[0], 'correo': r[1]} for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
"""