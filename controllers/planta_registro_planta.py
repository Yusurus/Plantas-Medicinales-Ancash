from flask import Blueprint, render_template

registro_bp = Blueprint('registro_bp', __name__)

@registro_bp.route('/modoadmin')
def home():
    return render_template('registro_planta.html')

@registro_bp.route('/registrar_planta', methods=['GET', 'POST'])
def registrar_planta():
    # Aquí irá la lógica real si deseas completarla
    pass
