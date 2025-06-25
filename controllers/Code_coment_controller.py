from flask import render_template, Blueprint

comendt_bd = Blueprint('comendt_bd', __name__)

@comendt_bd.route('/help_coment')
def coment_page():
    """
    Página de ayuda dinámica
    """
    return render_template('help_coment.html')