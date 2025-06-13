from flask import Blueprint, request, jsonify, session, redirect
from services.image_utils import procesar_imagen_base64
from services.deepface_service import reconocer_rostro

face_bp = Blueprint('face_bp', __name__)

"""USUARIOS_MOCK = {'admin': 'password123', 'usuario': '12345', 'test': 'test'}"""

@face_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

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
