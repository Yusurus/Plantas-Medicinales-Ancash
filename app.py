from flask import Flask
from flask_cors import CORS
from flask import session

from config.db import verificar_base_datos_rostros
from controllers.face_controller import face_bp
from controllers.user_controller import user_bp
from controllers.planta_visulizador import visualizacion_bp
from controllers.planta_registro_planta import registro_bp
from controllers.planta_identificacion import identificacion_bp
from controllers.planta_detalles import detalles_bp

#---------
from controllers.registrar_zona import registro_zona
#----------

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

#----
app.register_blueprint(registro_zona)
#----

if __name__ == '__main__':
    if verificar_base_datos_rostros():
        print("Iniciando servidor Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("No se puede iniciar el servidor sin la base de datos de rostros.")
