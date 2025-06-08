from flask import Blueprint, render_template, request

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
    # Aquí irá la lógica real si deseas completarla
    pass