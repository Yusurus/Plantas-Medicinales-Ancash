from flask import Blueprint, jsonify, request
from config.db import get_connection

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/registrar', methods=['POST'])
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
