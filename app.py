from flask import Flask
from flask_cors import CORS
from flask import session

from config.db import verificar_base_datos_rostros
from controllers.face_controller import face_bp
from controllers.user_controller import user_bp
from controllers.planta_visulizador import visualizacion_bp
from controllers.gestionPlantas.registro_planta import registro_bp
from controllers.planta_identificacion import identificacion_bp
from controllers.planta_detalles import detalles_bp
from controllers.gestionPlantas.registro_zona import registro_zona
from controllers.gestionPlantas.registro_saberes import registro_saberes
from controllers.gestionPlantas.registro_usos import registro_usos
from controllers.reportes.reportes_pdf import reporte_bp
from controllers.reportes.reporte_grafico import reportes_bp2
from controllers.visor_codigo import visorcodigo_bp
from controllers.gestionPlantas.registro_archivaciones import registro_archivaciones

app = Flask(__name__)
app.secret_key = '1234'
CORS(app)
@app.context_processor
def inject_user():
    return dict(user=session.get('usuario'))

# Registrar blueprints
app.register_blueprint(face_bp)
app.register_blueprint(user_bp)
app.register_blueprint(visualizacion_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(identificacion_bp)
app.register_blueprint(detalles_bp)
app.register_blueprint(registro_zona)
app.register_blueprint(registro_saberes)
app.register_blueprint(registro_usos)
app.register_blueprint(registro_archivaciones)
app.register_blueprint(reporte_bp)
app.register_blueprint(reportes_bp2)
app.register_blueprint(visorcodigo_bp)


if __name__ == '__main__':
    if verificar_base_datos_rostros():
        print("Iniciando servidor Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("No se puede iniciar el servidor sin la base de datos de rostros.")

'''
# ESTE CODIGO COMENTE SIRVE PARA INICIAR EL SERVIDOR DE FLASK EN HTTPS PARA QUE SI OTROS DISPOSITVOS A LA MISMA RED
# PUEDAN CONECTARSE Y PODER PRENDER LA CAMARA PARA EL RECONOCIMIENTO FACIAL
# LIBRERIA NECEARIA: cryptography y si quieres intalar todo lo relcionado a ttps es el arterior y pyOpenSSL; 
# ESTO ES LO MINIMO NECESARIO: pip install cryptography
if __name__ == '__main__':
    if verificar_base_datos_rostros():
        print("Iniciando servidor Flask con HTTPS...")
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
    else:
        print("No se puede iniciar el servidor sin la base de datos de rostros.")
'''